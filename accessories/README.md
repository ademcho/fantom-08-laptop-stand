# FANTOM-08 cup and cable holders

| Design | Status | Files |
|---|---|---|
| [Cup holder R2](fantom-cup-holder-R2/) | Physically printed successfully per Abe | Source, reference STEP, STL/STEP parts and assembly, fit coupon, can insert, two unsliced Bambu projects, CAD previews and validation |
| [Cup holder R1](fantom-cup-holder-R1/) | Archived earlier revision | Source, STL/STEP, per-part 3MFs, CAD previews and validation |
| [Cable holder R2](fantom-cable-holder-R2/) | GUI slice checked; print start unconfirmed | Source, STL/STEP, earlier offline project and latest checked saved project, CAD previews and validation |
| [Cable holder R1](fantom-cable-holder-R1/) | Works, but TRS seats tight per Abe | Source, STL/STEP, saved project, CAD previews and validation |

R2 cable geometry: two 8.5 mm TRS seats, two additional 9.5 mm end seats, 19 mm seat-center recess depth, unchanged proven 12 mm grip. USB seats remain 5 / 4 / 3.2 mm. Source parameters and exported validation agree.

The later cable GUI check reported Generic PETG, black PETG / AMS A1 on X2D, 210 layers, 1 h 57 m and 58.99 g. These are recorded session observations, not statistics recoverable from the saved file. Archive inspection of `Fantom-cable-holder-R2-PETG-checked.3mf` confirms Generic PETG @BBL X2D 0.4 nozzle, first-filament PETG assignment and 79,576 mesh faces, but **no cached G-code or embedded slice statistics**. Re-slice when reopening and verify the actual AMS mapping before any future print. No print start is confirmed, and no printer was operated for publication.

Each revision retains its original source/export/previews layout. CAD generation needs the Python OpenCascade environment used by the original project; render scripts have their own dependencies. Run scripts from the corresponding revision directory. R2 cable project preparation reads the retained sibling R1 project. The optional cable toolpath diagnostic script requires locally generated diagnostic G-code, which is deliberately not distributed.

Original CAD validation reports are historical generation evidence, not fresh physical tests. [Artifact provenance](artifact-provenance.json) records original SHA-256 hashes; model and project binaries are unchanged. READMEs have updated status and portable command paths. All included 3MF ZIP archives were integrity checked before publication.

Excluded: diagnostic/failed slicing output and logs, unverified standalone G-code, diagnostic toolpath images, duplicate delivery ZIPs, upload/session metadata, and the unrelated preserved pre-R2 Bambu session. Existing music-rest and bracket working-tree changes are outside this update.

Models and code remain under the repository’s CC BY 4.0 license.
