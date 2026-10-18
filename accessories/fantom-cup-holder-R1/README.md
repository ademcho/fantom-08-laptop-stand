# Publication status — 2026-10-18

Archived R1; use [R2](../fantom-cup-holder-R2/) for the latest cup holder. Historical prototype notes below describe the original design session.

See [artifact inventory and verification](../README.md). Remaining notes are retained design-session documentation; current status above takes precedence.

# FANTOM-08 rear-right cup holder — prototype R1

Remix of Abe Demcho's CC BY 4.0 FANTOM-08 laptop/music-stand keyboard clamp.
Original local project: the parent repository.
Original working files and edits were not changed. This folder is independent.

## Print the coupon first

`exports/fit_coupon_170mm.stl` is a **5 mm thin full-reach profile**, not a load-bearing bracket. It must span the full 170 mm opening to test the rear wall, top panel, front lip and under-case foot together. A physically shorter span would not verify those relationships.

The earlier +1 mm coupon won on 2026-09-06; that correction is already in the copied source (170 mm opening). Do not add another millimeter. The latest 2.5 mm hook-tip shortening is applied, leaving a 17.5 mm hook drop. Music-rest saddle coupons fit a 15.6 mm laptop rail; those are NOT the keyboard gripping geometry.

Test unloaded on the straight far-right rear panel, slightly inboard of the rounded extreme corner and clear of connections. Photos support plausibility only: the right-side cross-section has NOT been measured or proven. Seat the foot and upper arm gently; check lip capture, no rocking, all nearby keys up/down, controls, cables and removal. Do not force a tight fit. The full-thickness part will be stiffer than the coupon. If it fails, measure rear bearing plane to front lip, top-to-under-case contact height, local corner radii and available straight width before revising.

## Design dimensions

- Cup: **86 mm internal diameter × 75 mm usable depth**, 4 mm walls, 4 mm closed floor; 94 mm outside diameter.
- Intended vessels: full 16 US fl oz standard can; glasses whose **entire lower 75 mm** fits inside 86 mm with clearance. Flared or handled glasses require checking. A can is loose in this universal well: print `optional_can_insert_70mm.stl` (70 mm bore, 65 mm support height, 84 mm rib envelope) or use a removable closed-cell foam sleeve; avoid top-heavy narrow-base stemware.
- Design target: **0.75 kg maximum combined vessel and contents**, not a validated rating. Full 16 oz liquid alone is roughly 0.47 kg; weigh heavier glasses.
- Cup center is 97 mm behind the keyboard's rear bearing plane; nearest outer wall is 50 mm behind it. Allow **at least 150 mm rear clearance**, plus hand access and clearance for the vessel overhang.
- Gravity moment from the target beverage mass is approximately **0.71 N·m**, before holder mass or dynamic bumps. The retained under-case foot, 15 mm bracket, broad cup fin and two separated bolts resist that moment; no stress simulation or load validation is claimed.

## Printing

Print at 100% in the supplied orientations. Starting settings: PETG, 0.4 mm nozzle, 0.20 mm layers, 5 perimeters, 35–40% infill, 6 top/bottom layers. Dry filament and tune adhesion first. Coupon: 3 walls, 15% infill is sufficient for unloaded fit only.

Bracket and coupon lie on a broad flat side, with layers following the gripping profile; do not stand the clamp upright. Cup stands on its closed floor. Its fin has a 45° underside; inspect the two small horizontal bolt-hole bridges and use local support if your printer requires it. No support should fill the drinking well. Separate pieces keep the bracket's strength-oriented print and the cup's sealed floor practical on a 256 mm bed. A combined part would span about 324 mm and require a less favorable orientation/support.

Mesh watertightness is a topology check, **not proof of a leakproof FDM print**. Leak-check off the instrument. Use a removable waterproof liner or coaster to catch condensation; account for its thickness in the available bore. No drain holes are provided. Do not use printed surfaces as a drinking vessel.

## Assembly and cautious first use

1. After the coupon passes, print the bracket and cup and remove sharp edges/first-layer flare. Keep contact geometry intact.
2. Mate the cup's 8 mm fin to the bracket's rear ear, flat face to flat face. Insert **two M4 × 35 mm bolts**, with washers under heads and nuts, and two M4 locknuts. The plastic stack is 23 mm; verify nut engagement and actual hardware length. Tighten snugly without crushing the plastic. Nuts are external, not captive. Adhesive is unnecessary.
3. Contact faces must be smooth and clean. Use very thin removable protective film only if the coupon leaves adequate clearance; thick padding changes the fit. No pad allowance was added to the recovered opening. Ensure the under-case teeth do not mark the case; stop if they do.
4. Test first on a rigid dummy profile/bench, with secured dry weights in steps to 0.75 kg. Check sustained creep, bolt slip, cracks, fin separation and gentle incidental bumps; inspect after unloading. These checks do not establish a certified rating. Do not use if rocking, permanent movement or whitening occurs.
5. Mount empty at the verified right-side location. Check full-thickness seating again. Keep the beverage wholly behind the instrument; never use the holder as a handle. Remove drinks before moving the keyboard and avoid unattended sustained loads.

Roland cautions against liquid containers on the unit. This is an untested, non-Roland-approved accessory; a rear cup can still spill onto electronics if bumped. Prefer a lidded vessel; a separate floor-standing holder keeps liquids off the instrument entirely.

## Reproduce

Run the existing installed environment (no installation required):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/generate.py
```

Parameters are at the top of `source/generate.py`; the copied source STEP preserves the curved gripping profile. Exports include oriented STLs, individual STEP solids, assembly STEP and validation JSON. Visuals depict CAD geometry, not a structural simulation or exact keyboard model.

## Digital verification

All four parts passed CAD validity, one-solid checks, STEP round-trip, closed STL edge incidence and one connected mesh component. The assembly has zero volumetric interference. Bambu Studio 02.08.02.61 sliced all four at 0.20 mm / five walls / 40% infill with no object warnings. Indicative estimates: bracket 73 g / 1 h 51 min, cup 143 g / 3 h 9 min, optional insert 38 g / 1 h 21 min; coupon 24 g / 42 min at those same heavier settings.

The CLI emitted `Invalid T command` diagnostics while parsing the inherited X2D machine start sequence, although all slice result codes were success. **No machine G-code is delivered.** Import the STLs in your slicer, select your actual printer/filament and re-slice. Digital checks do not establish physical fit, fatigue strength, leakproofness or a safe load rating.
