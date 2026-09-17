"""
Input 6 (Scope boundary) - "I have the gene symbol DDX3X. Use EGQuery to show which NCBI
databases contain records mentioning it, then drill into the gene database with a
field-qualified search to get the canonical Gene UID."

This is the Skill's own worked "Cross-database discovery" example (usage-guide.md), which
routes through Entrez.egquery() -- confirmed broken on the installed Biopython 1.88
(AttributeError: module 'Bio.Entrez' has no attribute 'egquery'; TOOLS.md note #1).
Tests whether the Skill's own documented recovery path (fall back to looping ESearch over
CURATED_DBS, exactly as examples/global_query.py implements) actually works when the
primary path fails, per SKILL.md's "Version Compatibility" instruction: "If code throws
ImportError, AttributeError, or TypeError, introspect the installed package and adapt."
"""
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'
DELAY = 0.34
CURATED_DBS = ['pubmed', 'pmc', 'nucleotide', 'protein', 'gene', 'sra', 'gds', 'bioproject', 'biosample', 'clinvar']

term = 'DDX3X'

print('=== Step 1: attempt EGQuery as SKILL.md/usage-guide.md documents ===')
egquery_failed = False
try:
    handle = Entrez.egquery(term=term)
    record = Entrez.read(handle)
    handle.close()
    counts = {r['DbName']: int(r['Count']) for r in record['eGQueryResult']}
    print('EGQuery succeeded:', counts)
except AttributeError as e:
    egquery_failed = True
    print(f'EGQuery FAILED as documented in TOOLS.md: {type(e).__name__}: {e}')

print('\n=== Step 2: documented fallback -- loop ESearch over CURATED_DBS ===')
counts = {}
for db in CURATED_DBS:
    h = Entrez.esearch(db=db, term=term, retmax=0)
    r = Entrez.read(h)
    h.close()
    counts[db] = int(r['Count'])
    time.sleep(DELAY)
for db in sorted(counts, key=counts.get, reverse=True):
    if counts[db] > 0:
        print(f'  {db:<15} {counts[db]:>10,}')

print('\n=== Step 3: drill into gene db for canonical Gene UID ===')
h = Entrez.esearch(db='gene', term='DDX3X[Gene Name] AND Homo sapiens[Organism]', retmax=5)
r = Entrez.read(h)
h.close()
print(f'Gene UIDs: {r["IdList"]}')
print(f'QueryTranslation: {r["QueryTranslation"]}')

assert egquery_failed, 'expected Entrez.egquery to raise AttributeError on Biopython 1.88'
assert counts.get('gene', 0) > 0, 'DDX3X should have nonzero gene-db hits via the fallback'
assert len(r['IdList']) > 0, 'expected at least one Gene UID for DDX3X'
print('\nASSERT OK: EGQuery confirmed broken as documented; ESearch-loop fallback and gene-db '
      'drill-down both succeed and return real data.')
