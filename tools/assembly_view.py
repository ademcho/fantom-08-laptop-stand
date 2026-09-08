#!/usr/bin/env python3
"""Assembled scene of every part: two brackets (A + mirrored B), two brace plates,
telescoping printed brace. SPAN is a placeholder until the real bracket spacing is
measured. Exports exports/full_assembly.step; uploading it to Onshape auto-creates
an Assembly tab. Coordinates: X forward, Y along the keyboard, Z up.
"""
from build123d import *

SPAN, SOCKET, OVLP = 242.6, 10.0, 40.0   # keep in sync with tools/brace_beam.py
MID = -7.5

def solids_by_z(shape):  # (bottom, top) of the split bracket
    a, b = shape.solids()
    return (a, b) if a.bounding_box().min.Z < b.bounding_box().min.Z else (b, a)

bot_a, top_a = solids_by_z(import_step('exports/bracket_split.step'))
plate = import_step('exports/brace_mount.step').solid()
outer = import_step('exports/brace_outer.stl') if False else None  # STLs are meshes; re-import STEP instead
beam = import_step('exports/brace_beam.step')
outer, inner = beam.solids()
if outer.bounding_box().size.X < inner.bounding_box().size.X:
    outer, inner = inner, outer

# --- bracket A at origin (plain face y=0), bracket B mirrored, offset along Y
mirr = Plane((0, MID, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
Y_B = SPAN + 40 + 15          # plate(20) + span + plate(20), bracket B back face
bot_b = mirror(bot_a, about=mirr).moved(Location((0, Y_B, 0)))
top_b = mirror(top_a, about=mirr).moved(Location((0, Y_B, 0)))

# --- plates: A side sits at identity by construction; B side rotated 180 about vertical
plate_a = import_step('exports/brace_mount.step').solid()  # independent import: the STEP writer
# aliases products that share an underlying shape and silently drops one
plate_b = plate.rotate(Axis((-10, 0, 185), (0, 0, 1)), 180).moved(Location((0, SPAN + 40, 0)))

def place_beam(p, y_tip, tip_at_min, flip=False):
    p = p.rotate(Axis.X, 90).rotate(Axis.Z, 90)
    if flip:
        p = p.rotate(Axis.Z, 180)   # move the plug to the far end; roof stays up
    b = p.bounding_box()
    assert b.size.Y > 40 and b.size.Y > b.size.X, b   # length now along Y (inner rod is short at small spans)
    dy = y_tip - (b.min.Y if tip_at_min else b.max.Y)
    return p.moved(Location((-10 - (b.min.X + b.max.X) / 2, dy, 185 - (b.min.Z + b.max.Z) / 2)))

outer = place_beam(outer, SOCKET, True)                    # tip in socket A floor (y=10)
inner = place_beam(inner, SPAN + 2 * SOCKET + 10, False, flip=True)   # plug tip in socket B floor (y=430)

parts = {'Bracket A bottom (clamp)': bot_a, 'Bracket A top (tray)': top_a,
         'Bracket B bottom (clamp)': bot_b, 'Bracket B top (tray)': top_b,
         'Brace plate A': plate_a, 'Brace plate B': plate_b,
         'Brace outer tube': outer, 'Brace inner rod': inner}
for (na, pa), (nb, pb) in [(('Brace outer tube', outer), ('Brace inner rod', inner)),
                           (('Brace outer tube', outer), ('Brace plate A', plate_a)),
                           (('Brace inner rod', inner), ('Brace plate B', plate_b)),
                           (('Brace plate A', plate_a), ('Bracket A top (tray)', top_a))]:
    r = pa & pb
    v = 0 if r is None else r.volume
    assert v < 1, f'{na} intersects {nb}: {v:.1f}mm3'
# Onshape's STEP import ignores lazy child placements - bake world coords into geometry
def bake(q):
    b0 = q.bounding_box()
    q.relocate(Location())  # bake: keep global position, zero the placement
    b1 = q.bounding_box()
    assert (b1.min - b0.min).length < 0.01, (b0, b1)
    assert q.location.position.length < 1e-6, q.location
    return q
parts = {n: bake(p) for n, p in parts.items()}
for name, p in parts.items():
    p.label = name
scene = Compound(children=list(parts.values()), label='Fantom Stand assembly')
b = scene.bounding_box()
print(f'scene: X {b.size.X:.0f} Y {b.size.Y:.0f} Z {b.size.Z:.0f} mm, {len(scene.solids())} solids')
export_step(scene, 'exports/full_assembly.step')
n = len(import_step('exports/full_assembly.step').solids())
assert n == 8, f'STEP round-trip lost parts: {n}/8'
print('ok, round-trip 8/8')
