'''Input 6 (Scope Boundary) -- run the Skill's own examples/global_query.py (copied here, not
imported from the fork worktree) with a NEW term (not the fixer's "CRISPR").
Prompt: "I have the gene symbol PTEN. Show which NCBI databases contain records mentioning it,
then drill into the gene database with a field-qualified search to get the canonical Gene UID."
Also independently re-checks the fixer's claim that egquery.fcgi 301-redirects to an
unresolvable internal hostname, and checks CURATED_DBS honesty against the full EInfo db list.
'''
import runpy, sys, time
from Bio import Entrez
import urllib.request, urllib.error

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

# --- Step 1: run global_query.py's own functions directly (not __main__), with a new term ---
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
assert sum(1 for c in counts.values() if c > 0) >= 8, 'expected most curated dbs to have nonzero hits for a real gene symbol'
time.sleep(DELAY)

print('\n=== Step 3: drill into gene db for canonical Gene UID ===')
h = Entrez.esearch(db='gene', term='PTEN[Gene Name] AND Homo sapiens[Organism]', retmax=5)
r = Entrez.read(h); h.close()
print('Gene UIDs:', r['IdList'])
print('QueryTranslation:', r['QueryTranslation'])
assert '5728' in r['IdList'], 'expected real NCBI Gene ID for human PTEN (5728) in results'
time.sleep(DELAY)

# --- Independent verification of egquery.fcgi redirect claim (NOT trusting the fix log) ---
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

# Try resolving the internal hostname the fixer claims it redirects to
import socket
target_host = 'ext-http-eutils.linkerd.ncbi.nlm.nih.gov'
try:
    addr = socket.gethostbyname(target_host)
    print(f'  UNEXPECTED: {target_host} resolved to {addr}')
except socket.gaierror as e:
    print(f'  Confirmed: {target_host} does NOT resolve here ({e})')

# --- CURATED_DBS honesty check: how many total Entrez databases exist vs how many are curated? ---
print('\n=== CURATED_DBS coverage check ===')
h = Entrez.einfo()
r_all = Entrez.read(h); h.close()
all_dbs = r_all['DbList']
print(f'Total live Entrez databases (EInfo): {len(all_dbs)}')
print(f'CURATED_DBS covers: {len(CURATED_DBS)} of {len(all_dbs)}')
missing = sorted(set(all_dbs) - set(CURATED_DBS))
print(f'Databases NOT covered by CURATED_DBS ({len(missing)}): {missing}')
