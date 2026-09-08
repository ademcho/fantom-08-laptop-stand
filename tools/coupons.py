#!/usr/bin/env python3
"""Fit-test coupons for the clamp opening (rear wall to keybed lip, nominal 170mm after the +1 coupon).

Each coupon is a 5mm-thin slice of the bottom bracket's clamp profile - foot, post,
arm, lip - trimmed below the lap joint, with the lip shifted outboard by DELTA
(cut mid-arm at x=150, outboard piece translated, gap bridged). Post/foot/joint
geometry untouched, so the winning DELTA transfers straight to the real part.
Engraved label on the face. Print flat, low walls/infill.
"""
from build123d import *

DELTAS = [1.0, 1.5, 2.0, 2.5]
THICK, ZTOP, XCUT = 5.0, 150.0, 150.0
ARM_LO, ARM_HI = 118.62, 130.62      # arm underside / top

def box(x0, x1, y0, y1, z0, z1):
    return Box(x1-x0, y1-y0, z1-z0).moved(Location(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)))

a, b = import_step('exports/bracket_split.step').solids()
bottom = a if a.bounding_box().min.Z < b.bounding_box().min.Z else b

base = bottom & box(-100, 400, -THICK, 0, -100, ZTOP)   # thin slice, no lap/bolt zone
inboard = base & box(-100, XCUT, -100, 100, -100, 400)
outboard = base & box(XCUT, 400, -100, 100, -100, 400)

for d in DELTAS:
    c = inboard + outboard.moved(Location((d, 0, 0))) + box(XCUT-5, XCUT+5+d, -THICK, 0, ARM_LO, ARM_HI)
    txt = Pos(55, 128) * Text(f'+{d}', font_size=9)     # on Plane.XZ: local y -> world Z
    c -= extrude(Plane.XZ * txt, amount=1.0)            # engrave 1mm into the y=0 face
    bb = c.bounding_box()
    opening = 170.0 + d
    assert len(c.solids()) == 1 and abs(bb.max.X - (180.0 + d)) < 0.01, (d, bb)
    name = f'exports/coupon_plus{d:.1f}mm.stl'
    export_stl(c, name)
    print(f'{name}: opening {opening:.1f}mm, {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f}mm, {c.volume/1000:.0f}cm3')
