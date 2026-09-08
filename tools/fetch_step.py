#!/usr/bin/env python3
"""Pull the Part Studio as STEP into exports/bracket_current.step (translation API, polled)."""
import sys, time, os
sys.path.insert(0, os.path.dirname(__file__)); import onshape

OUT = sys.argv[1] if len(sys.argv) > 1 else 'exports/bracket_current.step'
t = onshape.call('POST', '/partstudios/d/{d}/w/{w}/e/{e}/translations',
                 body={'formatName': 'STEP', 'storeInDocument': False})
for _ in range(60):
    s = onshape.call('GET', f'/translations/{t["id"]}')
    if s['requestState'] == 'DONE': break
    assert s['requestState'] != 'FAILED', s.get('failureReason')
    time.sleep(2)
else:
    sys.exit('translation timed out')
data = onshape.call('GET', f'/documents/d/{{d}}/externaldata/{s["resultExternalDataIds"][0]}', accept='application/octet-stream')
open(OUT, 'wb').write(data)
print('wrote', OUT, len(data), 'bytes')
