# Fantom-08 laptop bracket

Clip-on laptop stand for a Roland Fantom-08. Print two brackets; they hook over the rear
panel and under the case bottom at the two clear spots on the panel. Laptop sits on the
15° tray. An optional cross brace (a 2020 aluminum extrusion between the brackets) stiffens
the pair side-to-side.

Design lives in Onshape: `Part Studio 1` is the source profile (one sketch + 15 mm extrude).
`Fantom Stand - Bracket 1.2 split` and `Fantom Stand - Brace mount` are generated.

## Print

The bracket is 286 mm tall — too big for a 256 mm bed — so it's split on the post with an
86 mm half-lap joint. Print one **A** set and one **B** set (B is mirrored so that, with the
brackets facing each other, both keep their nut pockets on the outer face and a flat inner
face for the brace plate). A halves only mate with A, B with B — the lap is handed.

| file | size (mm) | qty | lay on bed |
|---|---|---|---|
| `exports/bracket_bottom_A.stl` / `_B` | 199 × 221 × 15 | 1 each | nut-pocket face down |
| `exports/bracket_top_A.stl` / `_B` | 213 × 144 × 15 | 1 each | plain face down (tongue step up) |
| `exports/brace_mount.stl` | 28 × 90 × 20 | 2 | flat back down |

Flat, no supports. PETG, 4+ walls, 30 %+ infill. Layers run along the post and tray, which
is the strong direction; never print these standing up.

## Hardware

- 4 × M4 pan head, **×20 without brace / ×25–30 with brace** (2 per bracket; they are the
  lap-joint bolts, and with the brace the same bolts also hold the brace plates)
- 4 × M4 hex nut — drops into the hex pocket on the bracket's outer face
- 1 × 2020 aluminum extrusion (European standard, 6 mm slot), cut to span between the
  brackets + 2 × 14 mm socket engagement (cut a few mm short of max; the sockets are 10 mm deep)
- optional: 2 × M5 × 16 pan head, self-tapped into the extrusion's ~4.2 mm center bore
  through the back of each brace plate (the extrusion is already captive once both brackets
  are mounted; the screws only matter if you want the frame rigid off the keyboard)

Example Amazon (US) sources, checked 2026-08-30: M4 assortment kit with nuts+washers
[B08FQRWWCM](https://www.amazon.com/dp/B08FQRWWCM) ~$9 · 2020 extrusion 2×1000 mm
[B08934HPRR](https://www.amazon.com/dp/B08934HPRR) ~$30 (or ZYLtech
[B07Z787MB8](https://www.amazon.com/dp/B07Z787MB8)) · M5×16
[B009TE2OMU](https://www.amazon.com/dp/B009TE2OMU). Any European-standard 2020 with a
6 mm slot works; if the M5 spins in the bore, tap it M5 or use thread-locker.

## Assembly

1. Slide each bracket's tongues together (A with A, B with B).
2. Braceless: M4×20 from the plain face, nut in the hex pocket, tighten. Done.
3. With brace: screw the extrusion into the two brace plates first (optional M5s through
   the plate backs), then bolt each plate over a bracket's inner face — M4×25 through
   plate + bracket, head sunk in the plate's counterbore, nut in the bracket's hex pocket.

## Regenerate after editing the profile

```
.venv/bin/python tools/split.py    # needs a fresh exports/bracket_current.step from Onshape
.venv/bin/python tools/brace.py
```

`tools/onshape.py` is a tiny authenticated GET/POST wrapper (creds in
`~/.config/onshape/credentials.env`). Joint and brace parameters (lap span, bolt positions,
clearances, socket size) sit at the top of `split.py` / `brace.py`; bolt positions must match
between the two.
