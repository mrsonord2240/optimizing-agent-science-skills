'''Input 4 (Edge) -- regression of pre-fix Input 4, checking the SOFTENED wording against live data.
Prompt (usage-guide.md's own current worked example): "My esearch for 'MARCH1 AND human' returns
a big pile of loosely-related hits ... re-run with MARCHF1[Gene Name]."
Checks whether the new usage-guide.md wording ("big pile of loosely-related hits") matches
live reality, vs the old ("no hits") wording that the pre-fix audit flagged as false.
'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

h = Entrez.esearch(db='gene', term='MARCH1 AND human', retmax=0)
r = Entrez.read(h); h.close()
print(f'=== Original query: MARCH1 AND human ===')
print(f'Count: {r["Count"]}')
print(f'QueryTranslation: {r["QueryTranslation"]}')
count_orig = int(r['Count'])
time.sleep(DELAY)

h = Entrez.esearch(db='gene', term='MARCHF1[Gene Name] AND Homo sapiens[Organism]', retmax=0)
r2 = Entrez.read(h); h.close()
print(f'\n=== Field-qualified retry ===')
print(f'Count: {r2["Count"]}')
count_new = int(r2['Count'])

# The usage-guide now claims "a big pile of loosely-related hits", not "no hits" (old claim).
print(f'\nold usage-guide claim was "no hits" (Count==0): {count_orig == 0}')
print(f'new usage-guide claim is "a big pile of loosely-related hits" (Count large, >>1): {count_orig > 100}')
assert count_orig > 100, f'new wording claims a big pile; got {count_orig}'
assert count_new < count_orig, 'field-qualified retry should narrow the result'
print('ASSERT OK: new wording matches live reality; old "no hits" wording would NOT have')
