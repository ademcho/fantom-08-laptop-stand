from pathlib import Path
import zipfile,struct,json,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1]
base=R.parent/'fantom-cable-holder-R1/exports/cable-holder-print.3mf'
d=(R/'exports/cable-holder-print.stl').read_bytes();n=struct.unpack_from('<I',d,80)[0];vs=[];ids={};ts=[]
for i in range(n):
 v=struct.unpack_from('<12fH',d,84+i*50);tri=[]
 for j in (3,6,9):
  p=tuple(v[j:j+3])
  if p not in ids:ids[p]=len(vs);vs.append(p)
  tri.append(ids[p])
 ts.append(tri)
bb=[max(p[i] for p in vs) for i in range(3)];dx=(256-bb[0])/2;dy=(256-bb[1])/2
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',ns)
E.register_namespace('p','http://schemas.microsoft.com/3dmanufacturing/production/2015/06')
E.register_namespace('BambuStudio','http://schemas.bambulab.com/package/2021')
mesh=f'<?xml version="1.0"?><model unit="millimeter" xmlns="{ns}"><resources><object id="1" type="model"><mesh><vertices>'+''.join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x,y,z in vs)+'</vertices><triangles>'+''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in ts)+'</triangles></mesh></object></resources></model>'
with zipfile.ZipFile(base) as z,zipfile.ZipFile(R/'exports/Fantom-cable-holder-R2-PETG.3mf','w',zipfile.ZIP_DEFLATED) as out:
 for name in ['[Content_Types].xml','_rels/.rels','3D/_rels/3dmodel.model.rels']:
  out.writestr(name,z.read(name))
 root=E.fromstring(z.read('3D/3dmodel.model'))
 for m in list(root):
  if m.tag.endswith('metadata') and m.attrib.get('name') not in ['Application','BambuStudio:3mfVersion']:root.remove(m)
 root.find(f'{{{ns}}}build/{{{ns}}}item').set('transform',f'1 0 0 0 1 0 0 0 1 {dx} {dy} 0')
 out.writestr('3D/3dmodel.model',E.tostring(root));out.writestr('3D/Objects/object_1.model',mesh)
 c=json.loads(z.read('Metadata/project_settings.config'));c.update(wall_loops='4',sparse_infill_density='30%',top_shell_layers='5',bottom_shell_layers='5',enable_support='0',layer_height='0.2')
 assert c['filament_type'][0]=='PETG' and 'PETG' in c['filament_settings_id'][0]
 out.writestr('Metadata/project_settings.config',json.dumps(c,indent=2))
 out.writestr('Metadata/model_settings.config',f'''<?xml version="1.0"?><config><object id="2"><metadata key="name" value="Fantom cable holder R2 PETG"/><metadata key="extruder" value="1"/><part id="1" subtype="normal_part"><metadata key="name" value="Fantom cable holder R2"/><metadata key="source_file" value="cable-holder-print.stl"/><mesh_stat face_count="{n}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/></part></object><plate><metadata key="plater_id" value="1"/><metadata key="plater_name" value="R2 cable holder PETG"/><model_instance><metadata key="object_id" value="2"/><metadata key="instance_id" value="0"/><metadata key="identify_id" value="1"/></model_instance></plate></config>''')
print('Created PETG project; object filament=1; profile='+c['filament_settings_id'][0]);print('Centered mesh XY bounds:',dx,dx+bb[0],dy,dy+bb[1])
