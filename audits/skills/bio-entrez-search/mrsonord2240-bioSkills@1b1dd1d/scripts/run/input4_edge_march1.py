'''Input 4 (Edge) -- regression, MARCH1 ambiguous gene symbol vs usage-guide.md's current wording.'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

h = Entrez.esearch(db='gene', term='MARCH1 AND human', retmax=0)
r = Entrez.read(h); h.close()
print('=== Original query: MARCH1 AND human ===')
print(f'Count: {r["Count"]}')
print(f'QueryTranslation: {r["QueryTranslation"]}')
count_orig = int(r['Count'])
time.sleep(DELAY)

h = Entrez.esearch(db='gene', term='MARCHF1[Gene Name] AND Homo sapiens[Organism]', retmax=0)
r2 = Entrez.read(h); h.close()
print('\n=== Field-qualified retry ===')
print(f'Count: {r2["Count"]}')
count_new = int(r2['Count'])

print(f'\nold usage-guide claim was "no hits" (Count==0): {count_orig == 0}')
print(f'new usage-guide claim is "a big pile of loosely-related hits" (Count large, >>1): {count_orig > 100}')
assert count_orig > 100, f'new wording claims a big pile; got {count_orig}'
assert count_new < count_orig, 'field-qualified retry should narrow the result'
print('ASSERT OK: new wording matches live reality')
