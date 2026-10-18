"""Offline parametric cable parking bracket; mm. X forward, Y lateral, Z up.
Run with fantom_bracket/.venv/bin/python. Original curved interface in reference STEP.
"""
from pathlib import Path
import json, hashlib, struct
from collections import Counter
from kernel import *
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports'; OUT.mkdir(exist_ok=True)
TOP=130.621595736871
GRIP_WIDTH=12.0
COMB_X=(-110.0,-10.0); COMB_Y=(-42.0,0.0)
SHELF_BOTTOM=128.0; SHELF_TOP=134.0
SLOT_Y=-23.0
# name, X position, clear slot width, assumed cable diameter, assumed plug shoulder diameter
SLOTS=[('Extra large 1',-101,9.5,8.0,13.0),('Extra large 2',-83,9.5,8.0,13.0),
       ('TRS 1',-65,8.5,7.0,12.0),('TRS 2',-49,8.5,7.0,12.0),
       ('USB thick',-35,5.0,4.0,8.0),('USB medium',-25,4.0,3.2,7.0),('USB slim',-15,3.2,2.5,6.0)]

def box(x0,x1,y0,y1,z0,z1):return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)
def flat(p):
    b=p.bounding_box();return p.moved(Pos(-b.min.X,-b.min.Y,-b.min.Z))
def xy_prism(points,z0,z1):
    p=BRepBuilderAPI_MakePolygon()
    for x,y in points:p.Add(gp_Pnt(x,y,z0))
    p.Close();return Shape(BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(p.Wire()).Face(),gp_Vec(0,0,z1-z0)).Shape())
def all_round(p,r):
    f=BRepFilletAPI_MakeFillet(p.s);ex=TopExp_Explorer(p.s,TopAbs_EDGE)
    while ex.More():f.Add(r,TopoDS.Edge_s(ex.Current()));ex.Next()
    f.Build();assert f.IsDone();return Shape(f.Shape())
ref=import_step(ROOT/'source/bracket_reference.step')
proven=ref & box(-25,190,-15,0,-10,TOP)
proven-=box(169.99,180.01,-16,1,98,101.121595736871)
grip=proven & box(-25,190,-GRIP_WIDTH,0,-10,TOP+1)
assert abs(grip.volume-proven.volume*GRIP_WIDTH/15)<.01
comb=box(*COMB_X,*COMB_Y,SHELF_BOTTOM,SHELF_TOP)
# Round vertical plan corners then all remaining small edges, entirely before joining grip.
# Round edges parallel to Z on the blank via rotating the existing edge helper.
comb=round_y_edges(comb.rotate(Axis.X,90),2).rotate(Axis.X,-90)
for name,x,w,d,shoulder in SLOTS:
    cutter=Pos(x,SLOT_Y,(SHELF_BOTTOM+SHELF_TOP)/2)*Cylinder(w/2,10)
    cutter+=box(x-w/2,x+w/2,COMB_Y[0]-2,SLOT_Y,SHELF_BOTTOM-2,SHELF_TOP+2)
    cutter+=xy_prism([(x-w/2-1,-43),(x+w/2+1,-43),(x+w/2,-40),(x-w/2,-40)],SHELF_BOTTOM-2,SHELF_TOP+2)
    comb-=cutter
comb=all_round(comb,.6)
p=grip+comb
assert p.is_valid and len(p.solids())==1
assert (grip-p).volume<.001 # original interface completely preserved
# All slot centerlines remain free down to floor; plug envelopes clear frame and each other.
for name,x,w,d,shoulder in SLOTS:
    cable=Pos(x,SLOT_Y,70)*Cylinder(d/2,160)
    assert (p & cable).volume<.001, name
    plug=Pos(x,SLOT_Y,145)*Cylinder(shoulder/2,20)
    assert (p & plug).volume<.001, name
for a,b in zip(SLOTS,SLOTS[1:]):assert abs(a[1]-b[1])>(a[4]+b[4])/2
# Added material remains behind rear plane; no added intrusion into keyboard X >= 0.
assert (comb & box(0,190,-50,10,0,160)).volume<.001
printpart=flat(p.rotate(Axis.X,-90).rotate(Axis.Z,45)) # y=0 broad flat face on build plate
export_step(p,OUT/'cable-holder-installed.step')
export_step(printpart,OUT/'cable-holder-print.step')
export_stl(printpart,OUT/'cable-holder-print.stl',tolerance=.025,angular_tolerance=.12)
# OCC fillet tessellation can contain triangles collapsed by STL float32 rounding.
# Remove only collapsed triangles; the following closed-edge check must still pass.
fpath=OUT/'cable-holder-print.stl';data=fpath.read_bytes();raw_n=struct.unpack_from('<I',data,80)[0]
records=[]
for i in range(raw_n):
    rec=data[84+50*i:134+50*i];v=struct.unpack('<12fH',rec)
    pts=[tuple(round(t,5) for t in v[j:j+3]) for j in (3,6,9)]
    if len(set(pts))==3:records.append(rec)
n=len(records);data=data[:80]+struct.pack('<I',n)+b''.join(records);fpath.write_bytes(data)
edges=Counter();adj={};signed=0
for i in range(n):
    vals=struct.unpack_from('<12fH',data,84+50*i);pts=[tuple(round(v,5) for v in vals[j:j+3]) for j in (3,6,9)]
    assert len(set(pts))==3
    a,b,c=pts;signed+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    for j in range(3):
        key=tuple(sorted((pts[j],pts[(j+1)%3])));edges[key]+=1;adj.setdefault(key,[]).append(i)
assert set(edges.values())=={2}
neighbors=[set() for _ in range(n)]
for a,b in adj.values():neighbors[a].add(b);neighbors[b].add(a)
visited={0};todo=[0]
while todo:
    for j in neighbors[todo.pop()]-visited:visited.add(j);todo.append(j)
assert len(visited)==n and signed>0
roundtrip=import_step(OUT/'cable-holder-print.step');assert roundtrip.is_valid and len(roundtrip.solids())==1
b=printpart.bounding_box();assert b.size.X<256 and b.size.Y<256 and abs(b.min.Z)<.001
report={'parameters':{'grip_width_mm':GRIP_WIDTH,'opening_mm':170,'arm_mm':12,'hook_drop_mm':17.5,'comb_x_mm':COMB_X,'comb_y_mm':COMB_Y,'shelf_z_mm':[SHELF_BOTTOM,SHELF_TOP],'slot_center_y_mm':SLOT_Y,'slots_name_x_width_cable_shoulder_mm':SLOTS},'reference_sha256':hashlib.sha256((ROOT/'source/bracket_reference.step').read_bytes()).hexdigest(),'print_bounds_mm':list(b.size),'volume_cm3':p.volume/1000,'solid_PETG_mass_at_1_27_g_cm3':p.volume/1000*1.27,'slicer_estimate':None,'in_plane_rotation_deg':45,'slot_seat_depth_from_open_edge_mm':19,'cad_valid':p.is_valid,'solid_count':1,'step_roundtrip_valid':True,'mesh_triangles':n,'collapsed_STL_triangles_removed':raw_n-n,'watertight_edges':True,'mesh_connected_components':1,'positive_signed_mesh_volume_mm3':signed,'interface_removed_volume_mm3':(grip-p).volume,'assumed_cable_and_plug_envelope_intersections_mm3':0,'added_material_forward_of_rear_plane_mm3':0,'physical_opposite_side_fit_verified':False,'strength_validated':False,'port_clearance_verified':False}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
from render_base import draw
draw([('bracket',p,'#247f88')],ROOT/'previews/cad-views.svg')
f=ROOT/'previews/cad-views.svg';s=f.read_text().replace('Fantom-08 · lift-off plywood music rest','FANTOM-08 · cable parking bracket R2').replace('Actual exported CAD · 460 × 320 mm board · 65° reading angle · lift-off rail mounts','12 mm grip · 170 mm opening · open slots: 9.5 / 9.5 / 8.5 / 8.5 / 5 / 4 / 3.2 mm').replace('Wood: backboard and ledge · teal: two one-piece mounts · gray: existing stand','One piece · 100 × 42 × 6 mm comb · preserved contact profile · cable slots outside rear spine').replace('Mirrored mounts, flat faces outward. Original channel fit retained. Verify assembled stability and book load. Board fasteners omitted.','R1 fit worked; R2 cable clearance and retention remain to be tested. CAD views omit the instrument; no load rating claimed.');f.write_text(s)
print(json.dumps(report,indent=2))
