"""OmniPath license-filter probe: does license=commercial change rows or sources?"""
import io
import sys
import time

sys.dont_write_bytecode = True
import pandas as pd
import requests

OMNI = 'https://omnipathdb.org'


def get(params):
    r = requests.get(f'{OMNI}/interactions', params=params, timeout=90)
    time.sleep(1)
    return r, pd.read_csv(io.StringIO(r.text), sep='\t')


base = {'partners': 'TP53', 'genesymbols': 1, 'types': 'post_translational', 'fields': 'sources,references,curation_effort,n_resources'}
r, d = get({**base, 'license': 'academic'})
print('columns:', list(d.columns))
print('academic rows', len(d))
srcs = {}
for lic in ('academic', 'commercial', 'ignore', 'bogus'):
    r, d = get({**base, 'license': lic})
    s = set()
    if 'sources' in d.columns:
        for v in d['sources'].dropna():
            s.update(x.split('_')[0] for x in str(v).split(';'))
    srcs[lic] = s
    print(f'license={lic}: HTTP {r.status_code} rows={len(d) if r.ok else r.text[:80]} n_sources={len(s)}')
print('sources only in academic (not in commercial):', sorted(srcs['academic'] - srcs['commercial']))
r = requests.get(f'{OMNI}/about', params={'format': 'text'}, timeout=60)
print('about:', r.status_code, r.text[:120].replace('\n', ' '))
r = requests.get(f'{OMNI}/queries/interactions', params={'format': 'json'}, timeout=60)
print('license arg documented:', 'license' in r.text, r.text[:200].replace('\n', ' '))
