from pathlib import Path
import re,sys,json
import numpy as np
from render_base import png
R=Path(__file__).resolve().parents[1]
lines=(R/'diagnostics/UNVERIFIED-offline-output.gcode').read_text().splitlines()
x=y=0.; layer=0;feature='';relative=True;last_e=0;pts=[];chosen={1:[],60:[],120:[],160:[],210:[]};arcs=0
for line in lines:
 if line.startswith('; CHANGE_LAYER'):layer+=1
 if line.startswith('; FEATURE:'):feature=line.split(':',1)[1].strip()
 if line=='M83':relative=True
 if line=='M82':relative=False
 if line.startswith(('G0 ','G1 ','G2 ','G3 ')):
  vals={k:float(v) for k,v in re.findall(r'([XYE])(-?(?:\d*\.\d+|\d+))',line.split(';')[0])}
  X=vals.get('X',x);Y=vals.get('Y',y);ev=vals.get('E',0 if relative else last_e);de=ev if relative else ev-last_e
  if layer and de>0 and feature!='Custom' and ('X' in vals or 'Y' in vals):
   pts.extend([(x,y),(X,Y)])
   if layer in chosen:chosen[layer].append((x,y,X,Y))
   if line.startswith(('G2 ','G3 ')):arcs+=1
  x,y=X,Y
  if 'E' in vals:last_e=ev
bounds=[min(p[i] for p in pts) for i in range(2)]+[max(p[i] for p in pts) for i in range(2)]
assert min(bounds[:2])>=0 and max(bounds[2:])<=256
for k,segments in chosen.items():
 im=np.full((800,800,3),245,np.uint8)
 for x,y,X,Y in segments:
  a=np.array([x,256-y])*3+16;b=np.array([X,256-Y])*3+16
  for q in np.linspace(a,b,max(2,int(np.linalg.norm(b-a)*2))):
   u,v=np.rint(q).astype(int)
   im[max(0,v-1):min(800,v+2),max(0,u-1):min(800,u+2)]=[36,127,136]
 (R/f'previews/toolpath-layer-{k}.png').write_bytes(png(im))
report={'provisional_offline_estimate':'1h 56m 48s / 58.99 g / 19.311 m','gcode_filament_index':1,'material_profile':'Generic PETG @BBL X2D 0.4 nozzle','nozzle_temperature_C':255,'object_extrusion_XY_bounds_mm':bounds,'layers':layer,'arc_segments':arcs,'status':'CLI aborted after generating G-code; NOT certified or submitted; GUI validation and final A1 mapping required'}
(R/'diagnostics/toolpath-check.json').write_text(json.dumps(report,indent=2));print(report)
