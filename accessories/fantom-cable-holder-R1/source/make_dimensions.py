from pathlib import Path
import base64, re
R=Path(__file__).resolve().parents[1]
for i,b in enumerate(re.findall('base64,([^\"]+)',(R/'previews/cad-views.svg').read_text())):
    (R/f'previews/cad-view-{i+1}.png').write_bytes(base64.b64decode(b))
img=base64.b64encode((R/'previews/cad-view-1.png').read_bytes()).decode()
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 1500 1100">','<rect width="1500" height="1100" fill="#f4f6f4"/>','<g font-family="Arial,sans-serif" fill="#203343">','<text x="50" y="60" font-size="32" font-weight="bold">FANTOM-08 / cable parking bracket R1</text>','<text x="50" y="95" font-size="20">Dimensions in mm · preserved 170 opening / 12 arm / 17.5 hook · mounting fit pending</text>',f'<image x="35" y="150" width="810" height="715" href="data:image/png;base64,{img}"/>']
def t(x,y,txt,size=19):s.append(f'<text x="{x}" y="{y}" font-size="{size}">{txt}</text>')
def line(x,y,X,Y):s.append(f'<path d="M{x},{y} L{X},{Y}" fill="none" stroke="#344b56" stroke-width="1.5"/>')
t(900,155,'COMB / TOP VIEW',22)
# Coordinates: 6 pixels per mm, x=-72 at 900, y=0 at 250.
def X(v):return 900+(v+72)*6
def Y(v):return 250-v*6
s.append('<rect x="900" y="250" width="372" height="180" rx="12" fill="#247f88"/>')
for x,w,txt in [(-63,7,'7'),(-48,7,'7'),(-35,5,'5'),(-25,4,'4'),(-15,3.2,'3.2')]:
 s.append(f'<path d="M{X(x-w/2)},{Y(-31)} L{X(x-w/2)},{Y(-23)} A{w*3},{w*3} 0 0 1 {X(x+w/2)},{Y(-23)} L{X(x+w/2)},{Y(-31)} Z" fill="#f4f6f4"/>')
 t(X(x)-12,475,txt)
line(900,218,1272,218);line(900,208,900,240);line(1272,208,1272,240);t(1065,208,'62')
line(1300,250,1300,430);line(1280,250,1310,250);line(1280,430,1310,430);t(1315,345,'30')
t(900,510,'Slot widths; 1 mm mouth flare / side',17)
t(900,545,'6 mm shelf · 0.6 mm edge rounds',18)
t(900,578,'12 mm clamp width (40 mm on cup R2)',18)
t(900,611,'Slot seats 7 mm inside open edge',18)
t(900,644,'Seat centers: 15 / 13 / 10 / 10 pitch',18)
t(900,677,'72 mm maximum rearward projection',18)
t(900,710,'18 mm lateral overhang beyond grip',18)
t(900,753,'TRS ×2 / USB ×3',23)
t(900,786,'Seat cable sideways; plug rests above.',18)
t(900,816,'Lift plug, slide cable outward to remove.',18)
t(50,900,'PRINT FLAT: supplied STL has Y=0 side on bed; envelope 252 × 127.4 × 30 mm.',22)
t(50,942,'PORT CHECK: rear grip occupies a 12 mm wide strip. Comb adds no material forward of the rear plane.',20)
t(50,978,'Confirm local case profile, free rear strip, port plugs + finger access, cable diameters and plug shoulders.',20)
t(50,1020,'CAD view is actual model. Top schematic omits small edge rounds and mouth flare. No keyboard model supplied.',18)
t(50,1060,'Prototype: physical fit, port clearance, fatigue and load capacity remain unverified.',18)
s.append('</g></svg>');(R/'previews/dimensioned-preview.svg').write_text(''.join(s))
