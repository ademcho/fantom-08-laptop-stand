#!/usr/bin/env python3
"""Split the Fantom bracket into two printable halves with a half-lap joint.

Input : exports/bracket_current.step (pulled from Onshape, single 15mm extrude)
Output: exports/bracket_bottom.stl, exports/bracket_top.stl, exports/bracket_split.step

Part-studio coords: X = forward (toward keys), Z = up, Y = thickness (-15..0).
Joint: half-lap on the post between Z=LAP_LO and Z=LAP_HI. Bottom piece keeps the
back half (Y<-7.5) of the lap, top piece keeps the front half. Two M4 bolts through Y
with hex nut pockets on the back face of the bottom piece.
"""
from math import sqrt
from build123d import *

LAP_LO, LAP_HI = 142.0, 228.0   # post is 20mm wide here; arm top is at 138.6, left fillet starts at 232
GAP = 0.3                        # shoulder clearance so the halves seat
MID = -7.5                       # thickness mid-plane
BOLT_X, BOLT_Z = -10.0, (154.0, 216.0)   # post centreline; sections are 31mm / 22mm wide here
HOLE_D, NUT_AF, NUT_DEPTH = 4.4, 7.3, 3.5  # M4 clearance, M4 nut 7.0 AF + play

part = import_step('exports/bracket_current.step')
bb = part.bounding_box()
assert abs(bb.min.Y + 15) < 0.01 and abs(bb.max.Y) < 0.01, bb   # thickness along Y as expected
v0 = part.volume

BIG = 1000
def box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)))

POST_XMAX = 60  # lap only spans the post; the tray lip (x>145) dips below LAP_HI and stays with the top piece
bottom = part & (box(-BIG, BIG, -BIG, BIG, -BIG, LAP_LO) + box(-BIG, POST_XMAX, -BIG, MID, LAP_LO, LAP_HI - GAP))
top    = part & (box(-BIG, BIG, -BIG, BIG, LAP_HI, BIG) + box(-BIG, POST_XMAX, MID, BIG, LAP_LO + GAP, LAP_HI)
                 + box(POST_XMAX, BIG, -BIG, BIG, LAP_LO, LAP_HI))

for z in BOLT_Z:
    hole = Cylinder(HOLE_D / 2, 40, rotation=(90, 0, 0)).moved(Location((BOLT_X, MID, z)))
    bottom -= hole; top -= hole
    # hex pocket, flats facing ±X so the narrow post keeps its walls
    hexagon = RegularPolygon(NUT_AF / sqrt(3), 6, rotation=30)  # circumradius from across-flats
    pocket = extrude(Plane.XZ.offset(15 - NUT_DEPTH) * hexagon, amount=NUT_DEPTH + 1)  # Plane.XZ normal is -Y: offset 11.5 -> y=-11.5, extrude toward -Y
    pocket = pocket.moved(Location((BOLT_X, 0, z)))
    assert pocket.bounding_box().min.Y < -15 and abs(pocket.bounding_box().max.Y + 11.5) < 0.01, pocket.bounding_box()
    bottom -= pocket

# self-checks
for name, p in (('bottom', bottom), ('top', top)):
    b = p.bounding_box()
    print(f'{name}: X {b.size.X:6.1f}  Y {b.size.Y:5.1f}  Z {b.size.Z:6.1f}  vol {p.volume/1000:.1f} cm3  solids {len(p.solids())}')
    assert b.size.X <= 250 and b.size.Z <= 250, 'does not fit X2D bed'
    assert len(p.solids()) == 1
removed = v0 - bottom.volume - top.volume
print(f'original {v0/1000:.1f} cm3, removed by holes/pockets/gap {removed/1000:.2f} cm3')
assert 0 < removed < 5000

export_stl(bottom, 'exports/bracket_bottom.stl')
export_stl(top, 'exports/bracket_top.stl')
export_step(Compound(children=[bottom, top], label='Fantom Stand split'), 'exports/bracket_split.step')
print('ok')
