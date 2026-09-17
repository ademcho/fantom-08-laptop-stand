#!/usr/bin/env python3
"""Split the Fantom bracket into two printable halves with a half-lap joint.

Input : exports/bracket_current.step (pulled from Onshape, single 15mm extrude)
Output: mirrored A/B halves, USB bottom B, and exports/bracket_split.step.
Shortens the source profile's downward keybed hook during generation.

Part-studio coords: X = forward (toward keys), Z = up, Y = thickness (-15..0).
Joint: half-lap on the post between Z=LAP_LO and Z=LAP_HI. Bottom piece keeps the
back half (Y<-7.5) of the lap, top piece keeps the front half. Two M4 bolts through Y
with hex nut pockets on the back face of the bottom piece.
"""
from math import sqrt
from build123d import *

LAP_LO, LAP_HI = 142.0, 228.0   # post is 20mm wide here; arm top is at 130.6 (R45 fillet ends at 175.6), left fillet starts at 232
GAP = 0.3                        # shoulder clearance so the halves seat
MID = -7.5                       # thickness mid-plane
BOLT_X, BOLT_Z = -10.0, (154.0, 216.0)   # post centreline; sections are 26mm / 22mm wide here
HOLE_D, NUT_AF, NUT_DEPTH = 4.4, 7.3, 3.5  # M4 clearance, M4 nut 7.0 AF + play
HOOK_SHORTEN = 2.5               # raise the key-facing hook tip; keep the arm and 170 mm opening
assert 0 <= HOOK_SHORTEN <= 3

part = import_step('exports/bracket_current.step')
bb = part.bounding_box()
assert abs(bb.min.Y + 15) < 0.01 and abs(bb.max.Y) < 0.01, bb   # thickness along Y as expected
v0 = part.volume

BIG = 1000
def box(x0, x1, y0, y1, z0, z1):
    return Box(x1 - x0, y1 - y0, z1 - z0).moved(Location(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)))

# Locate the 10 x 15 mm downward-facing hook tip in the unmodified source.
# This is applied after every Onshape fetch, so regeneration retains the fix.
tips = [f for f in part.faces() if f.bounding_box().min.X > 100
        and f.bounding_box().max.Z < 140 and f.bounding_box().size.Z < 1e-6
        and abs(f.area - 150) < .001]
assert len(tips) == 1, 'Source hook profile changed; review the shortening cut'
tip = tips[0].bounding_box()
assert abs(tip.min.X-170) < .001 and abs(tip.max.X-180) < .001
hook_cut = box(tip.min.X-.01, tip.max.X+.01, -16, 1,
               tip.min.Z-1, tip.min.Z+HOOK_SHORTEN)
original = part
part -= hook_cut
assert part.is_valid and len(part.solids()) == 1
assert abs(original.volume-part.volume-150*HOOK_SHORTEN) < .001
hook_after = part & box(tip.min.X, tip.max.X, -16, 1, tip.min.Z-1, tip.min.Z+20)
assert abs(hook_after.bounding_box().min.Z-tip.min.Z-HOOK_SHORTEN) < .001
print(f'Hook tip raised {HOOK_SHORTEN:.1f} mm: Z {tip.min.Z:.3f} -> {tip.min.Z+HOOK_SHORTEN:.3f}')

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
    assert p.is_valid and len(p.solids()) == 1
removed = v0 - bottom.volume - top.volume
print(f'original {v0/1000:.1f} cm3, removed by holes/pockets/gap {removed/1000:.2f} cm3')
assert 0 < removed < 5000

export_stl(bottom, 'exports/bracket_bottom_A.stl')
export_stl(top, 'exports/bracket_top_A.stl')
# Set B is mirrored across the thickness mid-plane so its nut pockets face outward
# when the two brackets stand facing each other (brace plates go on the plain inner faces).
# A halves only mate with A, B with B - the lap handedness mirrors too.
mirr = Plane((0, MID, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
bottom_b, top_b = mirror(bottom, about=mirr), mirror(top, about=mirr)
export_stl(bottom_b, 'exports/bracket_bottom_B.stl')
export_stl(top_b, 'exports/bracket_top_B.stl')

# --- USB bypass for the bracket that lands on the rear-panel USB cluster (player's right = B).
# The post is cut away over the port band and rerouted as a hump on the plain (inner) face,
# which is the face that points up when printing pocket-face-down. The cutout has a 45 deg
# gable roof so nothing bridges. Only one side can carry the bypass on a flat print, so the
# void clears the ports fully on the pocket side (open to the bed) and by USB_HALF_W + 4 mm
# beyond the mid-plane on the hump side.
KB_BOT, KB_TOP = 23.1, 118.6                   # case bottom (tooth tips) / case top (arm underside)
USB_LO, USB_HI, USB_MARGIN = 54.0, 28.0, 6.0   # measured: case bottom -> port bottom, case top -> port top
USB_HALF_W, LEG_T, PILLAR = 14.0, 8.0, 12.0    # half of the 28 mm cluster (buffer included), hump leg, pillar height
Z0, Z1 = KB_BOT + USB_LO - USB_MARGIN, KB_TOP - USB_HI + USB_MARGIN
Y_CEIL = MID + USB_HALF_W + 4.0                # void ceiling above the plain face (y=0)
APEX = Y_CEIL + (Z1 - Z0) / 2                  # 45 deg gable
hump = box(-20, 0, 0, APEX + LEG_T, Z0 - PILLAR, Z1 + PILLAR)
void = extrude(Plane.YZ.offset(-25) * Polygon((-16, Z0), (Y_CEIL, Z0), (APEX, (Z0 + Z1) / 2), (Y_CEIL, Z1), (-16, Z1), align=None), amount=30)
bottom_usb = bottom + hump - void
ports = box(-20, 0, MID - USB_HALF_W, MID + USB_HALF_W, KB_BOT + USB_LO, KB_TOP - USB_HI)   # measured cluster envelope
assert len(bottom_usb.solids()) == 1
assert bottom_usb.is_valid
def vol(x): return 0.0 if x is None else x.volume   # build123d returns None for an empty intersection
assert vol(bottom_usb & ports) < 1e-6, 'hump intersects the port envelope'
assert vol(bottom_usb & box(-20, 0, -20, 10, Z0, Z1)) < 1e-6, 'void not clear to +10 over the band'
bb = bottom_usb.bounding_box()
print(f'bottom_B_usb: window z {Z0:.1f}..{Z1:.1f}, void ceiling y=+{Y_CEIL:.1f}, hump to y=+{bb.max.Y:.1f}, vol {bottom_usb.volume/1000:.1f} cm3')
export_stl(mirror(bottom_usb, about=mirr), 'exports/bracket_bottom_B_usb.stl')
export_step(mirror(bottom_usb, about=mirr), 'exports/bracket_bottom_B_usb.step')
export_step(Compound(children=[bottom, top], label='Fantom Stand split'), 'exports/bracket_split.step')
print('ok')
