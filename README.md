# Fantom-08 laptop bracket

Clip-on laptop stand for a Roland Fantom-08. Print two; they hook over the rear panel
and under the case bottom at the two clear spots on the panel. Laptop sits on the 15° tray.

Design lives in Onshape: `Part Studio 1` is the source profile (one sketch + 15 mm extrude).
`Fantom Stand - Bracket 1.2 split` is the generated two-piece version.

## Print

Bracket is 286 mm tall — too big for a 256 mm bed — so it's split on the post with an 86 mm
half-lap joint.

| file | size (mm) | lay on bed |
|---|---|---|
| `exports/bracket_bottom.stl` | 199 × 221 × 15 | nut-pocket face down |
| `exports/bracket_top.stl` | 213 × 144 × 15 | bolt-head face down |

Flat, no supports. PETG, 4+ walls, 30 %+ infill. Layers run along the post and tray, which
is the strong direction; never print these standing up.

## Hardware (per bracket)

- 2 × M4 × 20 pan head (M4 × 16–25 all work; a longer bolt just sticks out the back)
- 2 × M4 hex nut, drops into the hex pocket on the bottom piece

Assemble: slide the tongues together, bolts through from the top piece's face, nuts in the
pockets, tighten. Glue is optional — the bolts carry the load.

## Regenerate after editing the profile

```
python3 tools/onshape.py GET /partstudios/d/{d}/w/{w}/e/{e}/translations ...   # or export STEP from Onshape by hand
.venv/bin/python tools/split.py       # -> exports/bracket_{bottom,top}.stl + bracket_split.step
```

`tools/onshape.py` is a tiny authenticated GET/POST wrapper (creds in `~/.config/onshape/credentials.env`).
`tools/split.py` holds the joint parameters (lap span, bolt positions, clearances) at the top.
