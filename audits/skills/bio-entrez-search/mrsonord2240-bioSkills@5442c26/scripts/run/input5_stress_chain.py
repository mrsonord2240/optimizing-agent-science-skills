'''Input 5 (Stress) -- regression, chained history-server intersection + spell-check.'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

print('=== Part A: history-server chained intersection ===')
h1 = Entrez.esearch(db='pubmed', term='TP53 AND colorectal cancer', usehistory='y', retmax=0)
r1 = Entrez.read(h1); h1.close()
time.sleep(DELAY)

h2 = Entrez.esearch(db='pubmed', term='review[PT] AND 2023[PDAT]', usehistory='y', WebEnv=r1['WebEnv'], retmax=0)
r2 = Entrez.read(h2); h2.close()
time.sleep(DELAY)

intersect_term = f'#{r1["QueryKey"]} AND #{r2["QueryKey"]}'
h3 = Entrez.esearch(db='pubmed', term=intersect_term, usehistory='y', WebEnv=r1['WebEnv'], retmax=0)
r3 = Entrez.read(h3); h3.close()
print(f'TP53 AND colorectal cancer: {r1["Count"]}')
print(f'review[PT] AND 2023[PDAT]: {r2["Count"]}')
print(f'Intersection: {r3["Count"]}')
time.sleep(DELAY)

print('\n=== Part B: spell-check ===')
h = Entrez.espell(db='pubmed', term='colen carsinoma')
r = Entrez.read(h); h.close()
print('Original: colen carsinoma')
print(f'Corrected: {r["CorrectedQuery"]}')

assert int(r3['Count']) <= int(r1['Count']) and int(r3['Count']) <= int(r2['Count'])
assert 'carcinoma' in r['CorrectedQuery'].lower() or 'cancer' in r['CorrectedQuery'].lower()
print('ASSERT OK')
