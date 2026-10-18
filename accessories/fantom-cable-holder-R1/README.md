# Publication status — 2026-10-18

Abe reports R1 works, but its TRS seats are tight. Retained for revision history and as the profile input for R2. Use [R2](../fantom-cable-holder-R2/) for enlarged, deeper seats.

See [artifact inventory and verification](../README.md). Remaining notes are retained design-session documentation; current status above takes precedence.

# FANTOM-08 cable parking bracket R1

One-piece prototype for two unplugged TRS monitor leads and three USB leads. The compact comb has open sideways drop-in slots: support each plug above the shelf and slide its cable into the rounded seat. No connector threading, screws or assembly. Lift the plug and slide the cable out to reconnect. Open slots are convenient parking, not locks against sideways pulls.

## Preserved interface

Copied Abe Demcho's original reference STEP and R2 kernel into this independent folder. Original projects were not edited. Same X/Z contact geometry, 170 mm keyboard opening, 12 mm arm height and corrected 17.5 mm hook drop as the successful cup-holder grip. Only lateral contact width is reduced from 40 to **12 mm** (70% narrower). This is NOT the music-rest 15.6 mm channel. The narrower bracket will resist sideways rocking less well; no strength or load rating is claimed.

Comb: 62 × 30 × 6 mm, rounded plan corners and 0.6 mm small edge rounds, projecting at most 72 mm behind the keyboard rear plane and 18 mm sideways beyond the grip. Slot seats lie outside the spine so the cables can hang down. Extra comb material does not project forward of the rear plane. Slot mouths have a 1 mm flare per side. No lip forces a cable to bend over a sharp edge; keep slack hanging naturally below and follow each cable maker's bend-radius requirement. Do not coil a taut cable around the bracket or let heavy cable runs pull on it.

## Cable assumptions (measure yours)

| Slot, rear-most first | Clear width | Assumed cable OD | Assumed plug shoulder |
|---|---:|---:|---:|
| TRS 1 | 7.0 mm | 6.0 mm | 12 mm |
| TRS 2 | 7.0 mm | 6.0 mm | 12 mm |
| USB thick | 5.0 mm | 4.0 mm | 8 mm |
| USB medium | 4.0 mm | 3.2 mm | 7 mm |
| USB slim | 3.2 mm | 2.5 mm | 6 mm |

The 7 mm slots support TRS plug BODY shoulders, not the 6.35 mm metal shafts. Keep the cable below and the plug body above. Cable should slide loosely; adjust slot width to actual OD plus roughly 0.6–1.0 mm before printing if needed. The smallest plug-body dimension across a slot, in any orientation it can rotate into, must exceed its opening with useful bearing on both sides (target at least 1 mm each side). Slim USB-C or tapered connectors may fall through even when the cable fits: use another slot only if cable clearance AND body support work. Otherwise change that slot or use a separate removable stop collar on the cable; never wedge or crush the jacket. Supplied assumed round body envelopes clear one another, but unusually wide or right-angle plugs need measurement.

## Critical fitting information still needed

The printed cup holder's success confirms its location, not the opposite side. There is no measured opposite-side keyboard/port model. This R1 is a reviewable prototype, **not verified to clear those ports**.

Before printing, identify a straight mounting strip at least 12 mm wide and check the entire rear spine, upper arm, front hook and under-case foot against the case. Supply a ruler photo or measurements locating nearby jacks, switches, inserted plug bodies and their cable exits relative to that strip, plus clearance for fingers to reconnect. A port-free line through the full rear spine is required; no port bypass was guessed. The other project's measured USB window belongs to a specific original mount and was not transplanted here. If a port occupies this strip, relocate the mount or revise a measured bypass before use.

Also confirm 72 mm rear clearance plus hand room, 18 mm lateral comb clearance, local 170 mm rear-to-lip opening and same case contact heights/radii, clearance to keys in both positions, actual cable ODs and plug shoulders. Comb top is Z=134 mm in the source coordinates, about 15.4 mm above the original arm underside. For this handed layout choose a position where the slot mouths face an accessible clear side; if the opposite handed comb is needed, mirror the whole part laterally in CAD/slicer without scaling.

## Print and use

- Use `exports/cable-holder-print.stl` at 100%, in its supplied flat orientation. The Y=0 side is on the bed; layers follow the gripping profile. Do not stand the clamp up. Bounding box: **252 × 127.378 × 30 mm**. A 256 mm square plate has only 2 mm nominal margin on each end of the long axis when centered: verify exclusions, purge/calibration paths and skirt/brim in preview; rotate in the bed plane if needed, never scale to fit.
- PETG starting point: 0.4 mm nozzle, 0.20 mm layers, 4 walls, 25–30% infill, 5 top/bottom layers. These are proposed settings, not a sliced recipe. Supports are not expected: grip is an extruded profile and slots open toward the top in print orientation. The small 0.6 mm rounds create minor local overhangs. Inspect layer preview and adhesion before printing.
- Remove strings, sharp edges and elephant-foot flare without reshaping the proven contacts. Test unloaded at the chosen location; do not force the hook or add thick padding. Check keys, controls and all connected cables. Confirm each plug stays above its slot and can be removed easily. Stop if it rocks, slips or flexes excessively. This is cable parking only, not a handle or a support for heavy cable bundles.

## Checks and material estimate

OpenCascade: valid one-solid body, valid one-solid STEP round-trip. Grip volume scales exactly 12/15 from the original 15 mm reference; zero grip material removed by the comb. STL: 60,188 triangles, every welded edge has two incident faces, one connected component and positive signed volume. Forty float32-collapsed fillet triangles were removed before these checks; the resulting mesh is closed. Mesh and CAD volumes differ by less than 0.001%. Assumed cable paths and plug body envelopes have zero model intersection; neighboring assumed plug bodies clear. This does not verify the instrument or actual cables.

CAD volume **68.357 cm³**, equivalent to **86.8 g at 1.27 g/cm³ if fully solid**, excluding print extras. This is not a slicer prediction. The prior cup-holder plate was sliced at 342.21 g, but a like-for-like material comparison is unavailable: isolated offline Bambu Studio CLI rejected the saved project profile as incompatible. No successful slice, ready-to-print 3MF, filament/time estimate or structural validation is claimed. The actual saved profile was read: Bambu Lab X2D 0.4 nozzle, 256 × 256 bed, Generic PETG, Textured PEI, 0.20 mm, 5 walls / 40% infill. GUI/device state was untouched and no print job was sent.

## Editable source and outputs

`source/generate.py` contains dimensions and cable assumptions; `kernel.py` is the copied installed-OpenCascade adapter; `bracket_reference.step` retains the curved interface. Regenerate offline:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/generate.py
python3 source/make_dimensions.py
```

The dimension script extracts updated rendered PNGs from `previews/cad-views.svg` automatically. STEP files include installed and print coordinates. `exports/validation.json` records checks. `previews/dimensioned-preview.svg` combines actual CAD with a dimensioned top schematic; `cad-views.svg` and PNGs show actual geometry.

Attribution: remix of Abe Demcho's FANTOM-08 bracket, CC BY 4.0. Original local project the parent repository; reference copied from the successful cup-holder R2 source. No original files or user edits changed.
