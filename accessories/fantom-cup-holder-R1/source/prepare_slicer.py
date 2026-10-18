from pathlib import Path
import json,struct,zipfile
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'source/slice_settings.json').read_text())
cfg['from']='project'
cfg.pop('type',None)
for path in (ROOT/'exports').glob('*.stl'):
    data=path.read_bytes();n=struct.unpack_from('<I',data,80)[0];verts=[];lookup={};tris=[]
    for i in range(n):
        vals=struct.unpack_from('<12fH',data,84+50*i);t=[]
        for j in (3,6,9):
            pt=tuple(vals[j:j+3])
            if pt not in lookup:lookup[pt]=len(verts);verts.append(pt)
            t.append(lookup[pt])
        tris.append(t)
    mx=[max(v[k] for v in verts) for k in range(3)]
    vv=''.join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x,y,z in verts)
    tt=''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in tris)
    xml=f'''<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><metadata name="Application">BambuStudio-02.08.02.61</metadata><resources><object id="1" type="model"><mesh><vertices>{vv}</vertices><triangles>{tt}</triangles></mesh></object></resources><build><item objectid="1" transform="1 0 0 0 1 0 0 0 1 {128-mx[0]/2} {128-mx[1]/2} 0"/></build></model>'''
    with zipfile.ZipFile(ROOT/'slicer-check'/(path.stem+'.3mf'),'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('3D/3dmodel.model',xml)
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('Metadata/project_settings.config',json.dumps(cfg))
        z.writestr('Metadata/model_settings.config',f'<config><object id="1"><metadata key="name" value="{path.stem}"/><metadata key="extruder" value="1"/><part id="1" subtype="normal_part"><metadata key="name" value="{path.stem}"/></part></object><plate><metadata key="plater_id" value="1"/><model_instance><metadata key="object_id" value="1"/><metadata key="instance_id" value="0"/><metadata key="identify_id" value="1"/></model_instance></plate></config>')
