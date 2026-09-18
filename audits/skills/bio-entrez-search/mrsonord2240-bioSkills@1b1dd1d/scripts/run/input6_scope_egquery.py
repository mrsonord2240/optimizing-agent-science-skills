'''Input 6 (Scope Boundary) -- regression, runs global_query.py's own functions with a new term
(PTEN, not the SKILL.md example's CRISPR), independently re-checks the egquery.fcgi redirect claim.
'''
import runpy, time
from Bio import Entrez
import urllib.request, urllib.error

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

mod = runpy.run_path('global_query_copy.py', run_name='not_main')
confirm_egquery_broken = mod['confirm_egquery_broken']
cross_db_counts = mod['cross_db_counts']
CURATED_DBS = mod['CURATED_DBS']

term = 'PTEN'
print(f'=== Step 1: confirm Entrez.egquery() unavailable, term={term!r} ===')
result = confirm_egquery_broken(term)
assert result is None, 'expected AttributeError path (egquery still missing)'
time.sleep(DELAY)

print(f'\n=== Step 2: cross-database counts for {term!r} via ESearch loop ===')
counts = cross_db_counts(term, dbs=CURATED_DBS)
for db in sorted(counts, key=counts.get, reverse=True):
    print(f'  {db:<15} {counts[db]:>10,}')
assert sum(1 for c in counts.values() if c > 0) >= 8, 'expected most curated dbs nonzero for a real gene symbol'
time.sleep(DELAY)

print('\n=== Step 3: drill into gene db for canonical Gene UID ===')
h = Entrez.esearch(db='gene', term='PTEN[Gene Name] AND Homo sapiens[Organism]', retmax=5)
r = Entrez.read(h); h.close()
print('Gene UIDs:', r['IdList'])
print('QueryTranslation:', r['QueryTranslation'])
assert '5728' in r['IdList'], 'expected real NCBI Gene ID for human PTEN (5728)'
time.sleep(DELAY)

print('\n=== Independent check: does egquery.fcgi really redirect to an unresolvable host? ===')
url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term={term}'
req = urllib.request.Request(url, headers={'User-Agent': 'audit-tooling'})
try:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            print(f'  Redirect: HTTP {code} -> {newurl}')
            raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)
    opener = urllib.request.build_opener(NoRedirect)
    resp = opener.open(req, timeout=15)
    print(f'  No redirect intercepted; final status {resp.status}, body[:300]={resp.read(300)}')
except urllib.error.HTTPError as e:
    print(f'  Caught redirect as HTTPError: {e.code} {e.reason}')
except Exception as e:
    print(f'  Exception during fetch: {type(e).__name__}: {e}')

import socket
target_host = 'ext-http-eutils.linkerd.ncbi.nlm.nih.gov'
try:
    addr = socket.gethostbyname(target_host)
    print(f'  UNEXPECTED: {target_host} resolved to {addr}')
except socket.gaierror as e:
    print(f'  Confirmed: {target_host} does NOT resolve here ({e})')
