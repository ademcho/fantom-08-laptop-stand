from pathlib import Path
import base64, re
R=Path(__file__).resolve().parents[1]
for i,b in enumerate(re.findall('base64,([^\"]+)',(R/'previews/cad-views.svg').read_text())):
    (R/f'previews/cad-view-{i+1}.png').write_bytes(base64.b64decode(b))
img=base64.b64encode((R/'previews/cad-view-1.png').read_bytes()).decode()
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1500" viewBox="0 0 1500 1500">','<rect width="1500" height="1500" fill="#f4f6f4"/>','<g font-family="Arial,sans-serif" fill="#203343">','<text x="50" y="60" font-size="32" font-weight="bold">FANTOM-08 / cable parking bracket R2</text>','<text x="50" y="95" font-size="20">Dimensions in mm · preserved 170 opening / 12 arm / 17.5 hook · R1 grip fit tested</text>',f'<image x="35" y="150" width="810" height="715" href="data:image/png;base64,{img}"/>']
def t(x,y,txt,size=19):s.append(f'<text x="{x}" y="{y}" font-size="{size}">{txt}</text>')
def line(x,y,X,Y):s.append(f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="#344b56" stroke-width="1.5"/>')
t(900,155,'COMB / TOP VIEW',22)
# Dimensioned top view, same X/Y layout as CAD.
def X(v):return 870+(v+110)*5
def Y(v):return 250-v*5
s.append('<rect x="870" y="250" width="500" height="210" rx="10" fill="#247f88"/>')
for x,w,txt in [(-101,9.5,'9.5'),(-83,9.5,'9.5'),(-65,8.5,'8.5'),(-49,8.5,'8.5'),(-35,5,'5'),(-25,4,'4'),(-15,3.2,'3.2')]:
 s.append(f'<path d="M{X(x-w/2)},{Y(-43)} L{X(x-w/2)},{Y(-23)} A{w*2.5},{w*2.5} 0 0 1 {X(x+w/2)},{Y(-23)} L{X(x+w/2)},{Y(-43)} Z" fill="#f4f6f4"/>')
 t(X(x)-12,495,txt,17)
line(870,218,1370,218);line(870,208,870,240);line(1370,208,1370,240);t(1090,208,'100')
line(1400,250,1400,460);line(1380,250,1410,250);line(1380,460,1410,460);t(1415,360,'42')
t(870,535,'NEW ×2        TRS ×2         USB ×3',20)
t(870,575,'TRS: 7 → 8.5 mm (+1.5 mm)',22)
t(870,610,'Two extra 9.5 mm slots at far end',21)
t(870,645,'Seat depth: 7 → 19 mm',22)
t(870,680,'Open mouth flares 1 mm per side',20)
t(870,715,'6 mm shelf / 0.6 mm edge rounds',20)
t(870,750,'12 mm grip width preserved',20)
t(870,795,'Cable hangs below; body rests above.',20)
t(870,830,'Deeper seats increase travel to escape',18)
t(870,855,'when lifted or pulled toward the mouth.',18)
t(50,900,'PRINT FLAT: STL lies flat, rotated 45° in plane; envelope 228.1 × 216.0 × 42 mm.',22)
t(50,942,'CLEARANCE: 110 mm rearward comb reach / 30 mm sideways beyond the grip; check the larger envelope.',20)
t(50,978,'Shoulder assumptions: ≥12 mm on 8.5 slots; ≥13 mm on 9.5 slots. Slim bodies can fall through.',20)
t(50,1020,'CAD view is actual model. Top schematic omits small edge rounds and mouth flare. No keyboard model supplied.',18)
t(50,1060,'R1 grip worked. R2 cable fit, retention and strength remain untested; open slots are not locks.',18)
s.append('</g></svg>');(R/'previews/dimensioned-preview.svg').write_text(''.join(s))
