"""Compose actual CAD raster views and a dimensioned explanatory plan. Pillow only."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import re,base64,io,json
R=Path(__file__).resolve().parents[1]
svg=(R/'previews/assembly.svg').read_text()
imgs=[Image.open(io.BytesIO(base64.b64decode(s))) for s in re.findall(r'data:image/png;base64,([^\"]+)',svg)]
canvas=Image.new('RGB',(1600,1300),'#f4f6f4'); d=ImageDraw.Draw(canvas)
font='/System/Library/Fonts/Supplemental/Arial.ttf'
def text(x,y,s,size=24,fill='#203343'):
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=fill)
text(45,25,'FANTOM-08 | rear-right cup holder | prototype R1',36)
text(45,77,'Actual CAD views below. Test the 170 mm fit coupon at the intended location first.',24)
for im,x,w in [(imgs[0],35,790),(imgs[1],855,710)]:
    im.thumbnail((w,650));canvas.paste(im,(x,135))
text(45,790,'86 mm bore  /  75 mm usable depth  /  4 mm floor and walls',28)
text(45,835,'Two M4 x 35 bolts + washers + locknuts; 23 mm plastic stack; 28 mm bolt spacing',23)
text(45,875,'Cup stays behind the keyboard. 0.75 kg vessel + drink is a design target, NOT a tested rating.',22)
# Dimensioned top-view schematic: rear bearing plane and cup; no invented case dimensions.
x0,y0,sc=440,1090,2.3
def point(x,y):return (x0+x*sc,y0+y*sc)
d.line([point(0,-56),point(0,56)],fill='#247f88',width=4)
d.ellipse([point(-144,-47),point(-50,47)],outline='#b4752f',width=4)
d.ellipse([point(-140,-43),point(-54,43)],outline='#b4752f',width=2)
d.line([point(-97,-58),point(0,-58)],fill='#203343',width=2)
for x in [-97,0]:d.line([point(x,-62),point(x,-54)],fill='#203343',width=2)
text(200,925,'97 mm center setback',22)
text(465,1030,'Rear bearing plane',20)
text(465,1060,'50 mm to nearest cup wall',20)
text(465,1090,'144 mm rear projection',20)
text(465,1120,'Allow at least 150 mm + hand access',20)
text(930,970,'PRINT ORIENTATIONS',24)
text(930,1010,'Clamp + coupon: broad side down',22)
text(930,1050,'Cup + optional insert: upright',22)
text(930,1090,'PETG / 0.20 mm / 5 walls / 40%',22)
text(930,1130,'Fit coupon: 5 mm thin, full reach',22)
text(45,1230,'Closed base: no drain holes. Mesh closure does not prove liquid sealing. Fit/load testing remains essential.',22)
canvas.save(R/'previews/dimensioned-preview.png')
