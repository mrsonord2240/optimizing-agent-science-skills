"""Do the sources returned under license=commercial include resources whose own license is non-commercial?"""
import io, sys, time
sys.dont_write_bytecode = True
import pandas as pd, requests
OMNI = 'https://omnipathdb.org'
r = requests.get(f'{OMNI}/resources', params={'format': 'json'}, timeout=90)
res = r.json()
print('resources HTTP', r.status_code, type(res).__name__, len(res))
first = res[0] if isinstance(res, list) else list(res.values())[0]
print('keys of one resource:', sorted(first)[:30] if isinstance(first, dict) else first)
time.sleep(1)
r = requests.get(f'{OMNI}/interactions', params={'partners': 'TP53', 'genesymbols': 1, 'types': 'post_translational', 'license': 'commercial', 'fields': 'sources'}, timeout=90)
d = pd.read_csv(io.StringIO(r.text), sep='\t')
used = set()
for v in d['sources'].dropna():
    used.update(x.split('_')[0] for x in str(v).split(';'))
lic = {}
items = res if isinstance(res, list) else list(res.values())
for x in items:
    if isinstance(x, dict):
        name = x.get('name') or x.get('resource')
        lic[name] = (x.get('license') or {}).get('purpose') if isinstance(x.get('license'), dict) else x.get('license')
noncomm = {n: l for n, l in lic.items() if n in used and l and str(l).lower() not in ('commercial', 'for_profit', 'forprofit', 'ignore')}
print('sources used under license=commercial:', sorted(used))
print('of these, resource-level license purpose not commercial:', noncomm)
print('license purpose values seen:', sorted({str(v) for v in lic.values()}))
