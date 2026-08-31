#!/usr/bin/env python3
"""Fully printable cross brace: telescoping square tube, plugs into the same 20.4mm
sockets on the brace mount plates as the 2020 extrusion. No fasteners - once both
brackets are clamped to the keyboard the beam is captive; the 40mm+ telescope overlap
resists racking. Lighter duty than the extrusion, which is fine here.

SET SPAN FIRST: measure socket floor to socket floor between the two mounted brace
plates (= inner plate face to inner plate face + 2*10mm socket depth is handled below;
just measure plate face to plate face and put it in SPAN).

Pieces by span: <=225 one solid rod; <=425 outer tube + plugged inner rod;
<=625 two outer tubes bridged by an inner rod. All print lying flat, no supports:
the tube bore has a 45-degree roof instead of a flat bridge (insert rods roof-up).
"""
from build123d import *

SPAN = 400.0        # mm, plate face to plate face -- MEASURE AND SET
SOCKET, PLUG = 10.0, 12.0
SEG, OVLP = 240.0   , 40.0    # max printable piece, min telescope overlap
OD, WALL = 20.0, 2.2          # outer tube: fits the 20.4 socket
CLR = 0.3                     # per-side sliding clearance rod-in-bore

def house(w, h):              # flat-bottom pentagon, 45-degree roof
    return Polygon((-w/2, 0), (w/2, 0), (w/2, h), (0, h + w/2), (-w/2, h), align=None)

BORE_W, BORE_WALL_H = OD - 2*WALL, 8.5            # bore floor sits at y=WALL
ROD_W, ROD_WALL_H = BORE_W - 2*CLR, BORE_WALL_H - CLR

def lay(p):                   # length along X, flat bottom at y=0 for the slicer
    return p.rotate(Axis.Y, 90)

def outer(L):
    sq = Rectangle(OD, OD, align=(Align.CENTER, Align.MIN))
    bore = Pos(0, WALL) * house(BORE_W, BORE_WALL_H)
    return lay(extrude(Plane.XY * (sq - bore), amount=L))

def rod(L, plug=False):
    r = extrude(Plane.XY * (Pos(0, WALL) * house(ROD_W, ROD_WALL_H)), amount=L)
    if plug:
        r += extrude(Plane.XY * Rectangle(OD, OD, align=(Align.CENTER, Align.MIN)), amount=PLUG)
    return lay(r)

T = SPAN + 2 * SOCKET         # total beam length, tip to tip
parts = {}
if T <= SEG:
    parts['brace_rod'] = lay(extrude(Plane.XY * Rectangle(OD, OD, align=(Align.CENTER, Align.MIN)), amount=T))
elif T <= 2 * SEG - OVLP - PLUG + SEG * 0:  # outer + plugged inner
    inner = T - SEG + OVLP
    assert inner <= SEG, f'span too long for 2 pieces (inner {inner})'
    parts['brace_outer'] = outer(SEG)
    parts['brace_inner'] = rod(inner, plug=True)
    print(f'2-piece: outer {SEG:.0f} + inner {inner:.0f} (incl {PLUG:.0f} plug), overlap {OVLP:.0f}')
else:                          # outer + bridging rod + outer
    L = min(SEG, T / 2)
    mid = T - 2 * L + 2 * OVLP
    assert mid <= SEG, f'span too long even for 3 pieces (mid {mid})'
    parts['brace_outer'] = outer(L)
    parts['brace_mid'] = rod(mid)
    print(f'3-piece: 2x outer {L:.0f} + mid rod {mid:.0f}, overlap {OVLP:.0f} each end')

for name, p in parts.items():
    b = p.bounding_box()
    assert b.size.X <= 250 and len(p.solids()) == 1, (name, b)
    print(f'{name}: {b.size.X:.0f} x {b.size.Y:.0f} x {b.size.Z:.0f} mm')
    export_stl(p, f'exports/{name}.stl')
export_step(Compound(children=[p.moved(Location((0, 0, i * 30))) for i, (n, p) in enumerate(parts.items())],
                     label='Printed brace'), 'exports/brace_beam.step')
print('ok  (print 2x brace_outer for the 3-piece config)')
