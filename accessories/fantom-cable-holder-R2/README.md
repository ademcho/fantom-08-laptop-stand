# Publication status — 2026-10-18

Latest saved project: [Fantom-cable-holder-R2-PETG-checked.3mf](exports/Fantom-cable-holder-R2-PETG-checked.3mf). The later GUI check reported Generic PETG, black PETG mapped to AMS A1 on X2D, 210 layers, 1 h 57 m and 58.99 g. **Print start was not confirmed.** Archive inspection confirms the PETG preset, first-filament assignment and model; this saved 3MF has no cached G-code or embedded slice statistics, so re-slice on reopening. The earlier `Fantom-cable-holder-R2-PETG.3mf` remains the unsliced offline export. The historical offline attempt described below predates the GUI check; diagnostic G-code, logs and toolpath images are excluded.

See [artifact inventory and verification](../README.md). Remaining notes are retained design-session documentation; current status above takes precedence.

# FANTOM-08 cable parking bracket R2

R1 was printed and mostly works; its TRS slots pinched Abe's leads. R2 preserves the tested grip and opens/deepens the parking comb. R1 files and the original project are untouched.

## Changes

- Two existing TRS seats and entry channels grow from **7 to 8.5 mm** (+1.5 mm / 21%). Assumed cable OD up to about 7 mm leaves 1.5 mm diametral slack.
- Two new **9.5 mm** parking slots at the far end accept assumed cable OD up to about 8 mm, again with 1.5 mm slack.
- All seat centers are **19 mm inside the open edge**, versus 7 mm on R1. The rounded end reaches another half-slot-width into the shelf. The cable must travel about 12 mm farther toward the mouth to escape.
- USB clear widths remain **5 / 4 / 3.2 mm**, for assumed 4 / 3.2 / 2.5 mm leads. These now also have deeper entries.
- Straight open channels remain at full seat width, with an additional 1 mm mouth flare per side. A deeper rounded U was chosen instead of a pinching throat or dogleg that would require feeding a thick jacket around a narrow bend. There is no positive lock: an outward tug can still remove a cable. Deeper travel may help with small bumps, but retention has not been physically tested.
- Comb is **100 × 42 × 6 mm**, with 2 mm plan corners and 0.6 mm edge rounds. Tested grip remains **12 mm wide / 170 mm opening / 12 mm arm / 17.5 mm hook**. No fit scaling. This is not the music-rest channel.

## How it supports the plug

Hold the connector above the shelf, slip its cable sideways through a slot mouth, move it to the round end, and let the connector BODY shoulder rest on top while the cable hangs below. Lift the connector and slide outward to remove it. Do not force a tight cable, wrap it sharply around an edge, or hang heavy bundled cable runs from the bracket.

The model assumes a plug shoulder of at least **12 mm across the 8.5 mm TRS slot** and **13 mm across the new 9.5 mm slot**. This provides about 1.75 mm nominal bearing per side before edge rounding. Measure the smallest dimension a body can present if it rotates, not its largest width. Slim/tapered bodies can slip through; the 6.35 mm metal TRS shaft is not the retaining shoulder. Use the smallest freely fitting slot with reliable body support. Slim USB bodies may still need a removable stop collar. The assumed USB shoulder diameters are 8 / 7 / 6 mm respectively. No actual cable measurements were provided, so these are testable assumptions rather than fit guarantees.

## Printing and current status

Use `exports/cable-holder-print.stl` at **100%**. It already lies on the broad side and is rotated **45° in the bed plane**. Envelope is **228.061 × 215.968 × 42 mm**, fitting a 256 mm plate with nominal centered model margins of 13.97 and 20.02 mm. Do not auto-orient upright or scale the proven fit. Flat geometry builds the gripping profile in the layer plane; deeper channels open progressively upward in this orientation.

PETG: 0.4 mm nozzle, 0.20 mm layers, four walls, 30% infill, five top/bottom layers, no supports expected. Smooth any strings or first-layer flare without reshaping contact faces. Check the larger installed envelope: 110 mm behind the rear bearing plane and 30 mm sideways beyond the 12 mm grip. Abe previously confirmed no ports at his position; R2's larger comb still needs unobstructed hand/cable room.

`exports/Fantom-cable-holder-R2-PETG.3mf` is an **unsliced offline project**, centered at full scale. Its object is assigned to filament 1, whose actual embedded slicing preset is **Generic PETG @BBL X2D 0.4 nozzle**, density 1.27, 255°C nozzle. Other saved profile filaments exist but are not assigned to this object. This is separate from the required final AMS mapping: verify **black PETG / AMS A1**, not PLA/A2, in Bambu's Send dialog before submitting.

An isolated offline Bambu Studio attempt generated 210 layers and a **provisional** estimate of **1 h 56 m 48 s / 58.99 g / 19.311 m**, then aborted (exit 134; log reported invalid T commands during processing). It did not produce a confirmed sliced project. Therefore these figures are not a verified print job estimate. The unverified G-code is retained only under local `diagnostics/` and deliberately excluded from the delivery ZIP. Re-slice in the GUI and inspect the actual layer preview, calibration/purge paths and any warnings. Do not print the diagnostic G-code.

**Not queued or sent.** Desktop UI control is unavailable in this execution session, so current idle/clear printer state, physical filament identity in A1 and final Send mapping could not be rechecked. No GUI/device state was changed. No active job was cancelled or replaced. The next operator must complete those checks and send once, without retrying an uncertain submission.

## Verification

- OpenCascade valid one-solid model; valid one-solid STEP round-trip.
- 79,576 STL triangles; every welded edge has two incident faces, one connected component and positive signed volume. 56 triangles collapsed by STL float32 export were removed, then closure was checked.
- Grip retains all original material and the 12/15 width volume relation to the reference profile. Contact geometry was not reshaped.
- Assumed straight cable paths and connector body envelopes have zero solid intersections; adjacent assumed connector bodies clear each other.
- Added comb material stays behind the rear plane. Nominal web between adjacent slots is at least 5.5 mm at the seats (at least 3.5 mm allowing the full mouth flares); narrowest outer tip is 2.4 mm before the small edge rounding. No structural strength or load rating is claimed.
- CAD volume **77.404 cm³**, about 13.2% more than R1 despite two additional slots and greater depth. Fully solid PETG equivalent is 98.3 g; this is separate from the provisional slicer estimate.
- Generated toolpath images were inspected for layers 1, 120 and 210. They show the full grip first layer and separated comb-finger sections above its base, as expected. Diagnostic preview uses chords for arcs; reported XY bounds cover extrusion endpoints, not certified swept nozzle paths. It is not a substitute for the final GUI preview.

## Source and deliverables

`source/generate.py`: parameters, CAD creation, 45° print orientation, STL/STEP checks. `source/kernel.py` and `source/bracket_reference.step`: copied original interface tools/data. `source/make_dimensions.py`: dimensioned SVG and CAD PNG extraction. `source/prepare_project.py`: build the unsliced PETG 3MF from R1's saved profile. `source/check_toolpath.py`: optional diagnostic G-code preview; requires the local diagnostic output excluded from the ZIP.

Run from this folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/generate.py
python3 source/make_dimensions.py
python3 source/prepare_project.py
```

The project-preparation script expects the sibling R1 folder on this Mini. The CAD generator itself is self-contained except for the installed OpenCascade environment. Dimensioned PNG was rendered with macOS Quick Look and visually checked.

Remix of Abe Demcho's FANTOM-08 bracket, CC BY 4.0. Original the parent repository; copied reference SHA-256 recorded in `exports/validation.json`. Physical R1 feedback does not validate R2 cable retention, fatigue or load capacity.
