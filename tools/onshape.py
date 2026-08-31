#!/usr/bin/env python3
"""Tiny Onshape API helper. Creds from ~/.config/onshape/credentials.env.
Usage: onshape.py GET <path> [--out file] [k=v ...]   (path after /api/v6)
       onshape.py POST <path> --json '<json>'
"""
import os, sys, json, base64, urllib.request, urllib.parse
env = {}
for line in open(os.path.expanduser('~/.config/onshape/credentials.env')):
    line = line.strip()
    if line and not line.startswith('#') and '=' in line:
        k, v = line.split('=', 1); env[k] = v
BASE = env.get('ONSHAPE_BASE', 'https://cad.onshape.com')
AUTH = base64.b64encode(f"{env['ONSHAPE_ACCESS_KEY']}:{env['ONSHAPE_SECRET_KEY']}".encode()).decode()
D, W, E = '9a86687b513359acbe40631b', '344edab5271dd58bfe62b805', 'b5608a2bb5ea31c3b7cfe764'

def call(method, path, params=None, body=None, accept='application/json'):
    path = path.replace('{d}', D).replace('{w}', W).replace('{e}', E)
    url = BASE + '/api/v6' + path + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Basic ' + AUTH, 'Accept': accept, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        data = r.read()
        return json.loads(data) if 'json' in r.headers.get('Content-Type', '') else data

if __name__ == '__main__':
    method, path = sys.argv[1], sys.argv[2]
    out = None; params = {}; body = None; accept = 'application/json'
    args = sys.argv[3:]
    while args:
        a = args.pop(0)
        if a == '--out': out = args.pop(0)
        elif a == '--json': body = json.loads(args.pop(0))
        elif a == '--accept': accept = args.pop(0)
        elif '=' in a: k, v = a.split('=', 1); params[k] = v
    res = call(method, path, params, body, accept)
    if out:
        open(out, 'wb').write(res if isinstance(res, bytes) else json.dumps(res, indent=1).encode()); print('wrote', out, len(res) if isinstance(res, bytes) else '')
    else:
        print(json.dumps(res, indent=1) if not isinstance(res, bytes) else res[:2000])
