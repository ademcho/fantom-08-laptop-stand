"""Abe's FANTOM-08 rear cup holder prototype. Dimensions in mm.
Run with the original fantom_bracket .venv Python. No network or original edits.
X forward, Y sideways, Z up. Keyboard rear bearing plane X=0.
"""
from pathlib import Path
import json, hashlib, struct
from collections import Counter
from kernel import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports'
ID=86.0; DEPTH=75.0; WALL=4.0; FLOOR=4.0
CUP_X=-97.0; CUP_Y=-7.5; BASE_Z=45.0
FRAME_T=15.0; FIN_T=8.0; HOLE_D=4.5
HOLES=[(-30,75),(-30,103)] # X,Z; bolts run along Y
TOP=130.621595736871

def box(x0,x1,y0,y1,z0,z1):
    return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)

def slab(points,y0,y1):
    return extrude(Plane.XZ.offset(-y1)*Polygon(*points,align=None),amount=y1-y0)

def flat(p):
    b=p.bounding_box(); return p.moved(Location((-b.min.X,-b.min.Y,-b.min.Z)))

reference=import_step(ROOT/'source/bracket_reference.step')
# Remove laptop upright above arm; retain complete keyboard clamp below.
grip=reference & box(-25,190,-15,0,-10,TOP)
# Latest documented key-clearance correction; no opening change.
grip-=box(169.99,180.01,-16,1,98,101.121595736871)
assert grip.is_valid and len(grip.solids())==1
# Added rear mounting ear entirely behind rear contact plane.
ear=box(-46,-16,-15,0,60,116)
ear=round_y_edges(ear,4)
frame=grip+ear
outer=Pos(CUP_X,CUP_Y,BASE_Z+(DEPTH+FLOOR)/2)*Cylinder(ID/2+WALL,DEPTH+FLOOR)
inner=Pos(CUP_X,CUP_Y,BASE_Z+FLOOR+(DEPTH+1)/2)*Cylinder(ID/2,DEPTH+1)
cup=outer-inner
# 45-degree underside at fin nose; extra material joins cup wall along its height.
fin=slab([(-63,45),(-44,45),(-20,69),(-20,116),(-63,116)],0,FIN_T)
# Fillet fin's exposed forward vertical corner in its XZ outline.
fin=round_y_edges(fin,4,only=(-20,116))
cup+=fin
# Recut cavity: the fin may overlap wall but may not intrude into drinking space.
cup-=inner
for x,z in HOLES:
    cutter=Pos(x,-3,z)*Cylinder(HOLE_D/2,40,rotation=(90,0,0))
    frame-=cutter; cup-=cutter
# 5 mm thin, full-reach fit coupon. No historical '+1' naming ambiguity.
coupon=grip & box(-25,190,-5,0,-10,TOP+1)
parts={'fit_coupon_170mm':flat(coupon.rotate(Axis.X,90)),
       'bracket_170mm':flat(frame.rotate(Axis.X,90)),
       'cup_86x75mm':flat(cup)}
# Optional can-centering insert: 70 mm bore, 2 mm shell, three 3 mm ribs.
# 84 mm rib envelope leaves 1 mm radial clearance in the 86 mm cup.
insert=Cylinder(37,65)-Cylinder(35,67)
for a in (0,120,240):
    insert+=box(36,42,-1.5,1.5,-32.5,32.5).rotate(Axis.Z,a)
parts['optional_can_insert_70mm']=flat(insert)
report={'parameters':{'cup_inner_diameter_mm':ID,'cup_depth_mm':DEPTH,'cup_wall_mm':WALL,'cup_floor_mm':FLOOR,'opening_mm':170,'hook_drop_mm':17.5,'target_vessel_plus_drink_kg':.75,'cup_center_behind_rear_mm':-CUP_X,'cup_wall_clearance_behind_rear_mm':-CUP_X-ID/2-WALL,'beverage_gravity_torque_Nm':.75*9.81*(-CUP_X/1000)},'source_sha256':hashlib.sha256((ROOT/'source/bracket_reference.step').read_bytes()).hexdigest(),'parts':{},'physical_fit_or_load_validated':False}
for name,p in parts.items():
    assert p.is_valid and len(p.solids())==1,name
    b=p.bounding_box(); assert max(b.size.X,b.size.Y,b.size.Z)<250
    export_stl(p,OUT/(name+'.stl'),tolerance=.025,angular_tolerance=.12)
    export_step(p,OUT/(name+'.step'))
    data=(OUT/(name+'.stl')).read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    edges=Counter(); adjacency={}; vertices=set(); triangles=[]
    for i in range(n):
        vals=struct.unpack_from('<12fH',data,84+50*i)
        pts=[tuple(round(v,5) for v in vals[j:j+3]) for j in (3,6,9)]
        assert len(set(pts))==3
        triangles.append(pts); vertices.update(pts)
        for j in range(3):
            key=tuple(sorted((pts[j],pts[(j+1)%3])))
            edges[key]+=1; adjacency.setdefault(key,[]).append(i)
    assert set(edges.values())=={2},name
    neighbors=[set() for _ in range(n)]
    for a,btri in adjacency.values(): neighbors[a].add(btri); neighbors[btri].add(a)
    todo=[0]; visited={0}
    while todo:
        for j in neighbors[todo.pop()]-visited: visited.add(j); todo.append(j)
    assert len(visited)==n, f'{name}: disconnected mesh'
    report['parts'][name]={'dimensions_mm':[round(v,3) for v in b.size],'volume_cm3':round(p.volume/1000,2),'triangles':n,'valid_cad':True,'cad_solids':1,'watertight_edges':True,'mesh_connected_components':1,'step_solids':len(import_step(OUT/(name+'.step')).solids())}
    print(name,report['parts'][name],flush=True)
assert (frame & cup).volume<.001
assembly=Compound(children=[frame,cup],label='Fantom cup holder untested prototype')
export_step(assembly,OUT/'assembly.step')
report['assembly_interference_mm3']=0
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
# CAD render, adapting the existing project renderer (same tessellation method).
from render_base import draw
draw([('bracket',frame,'#247f88'),('cup',cup,'#d58b41')],ROOT/'previews/assembly.svg')
p=ROOT/'previews/assembly.svg'; s=p.read_text()
s=s.replace('Fantom-08 · lift-off plywood music rest','FANTOM-08 · rear-right cup holder prototype').replace('Actual exported CAD · 460 × 320 mm board · 65° reading angle · lift-off rail mounts','86 mm bore · 75 mm usable depth · 170 mm proven-location clamp opening').replace('Wood: backboard and ledge · teal: two one-piece mounts · gray: existing stand','Teal: keyboard clamp · amber: contained cup · two M4 through-bolts (omitted)').replace('Mirrored mounts, flat faces outward. Original channel fit retained. Verify assembled stability and book load. Board fasteners omitted.','Print coupon FIRST at far-right position. Geometry checked; physical fit and load capacity NOT validated.')
p.write_text(s)
print('Complete',flush=True)
