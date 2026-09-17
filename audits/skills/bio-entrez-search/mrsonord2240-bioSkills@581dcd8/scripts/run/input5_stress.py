"""
Input 5 (Stress / multi-part) - "Find PubMed records about 'BRCA1 AND breast cancer', then
on the same WebEnv search 'review[PT] AND 2024[PDAT]'. Intersect QueryKey #1 AND #2 to get
2024 reviews about BRCA1 in breast cancer. Also, I might have misspelled a term somewhere --
check 'breast canser' for me while you're at it."

Multi-part: history-server chaining/intersection (SKILL.md "History server semantics" +
worked chaining example) AND an unrelated spell-check call in the same turn.
"""
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'
DELAY = 0.34

# Part A: chained history-server intersection
h1 = Entrez.esearch(db='pubmed', term='BRCA1 AND breast cancer', usehistory='y', retmax=0)
r1 = Entrez.read(h1)
h1.close()
webenv = r1['WebEnv']
time.sleep(DELAY)

h2 = Entrez.esearch(db='pubmed', term='review[PT] AND 2024[PDAT]', usehistory='y', WebEnv=webenv, retmax=0)
r2 = Entrez.read(h2)
h2.close()
time.sleep(DELAY)

intersect_term = f'#{r1["QueryKey"]} AND #{r2["QueryKey"]}'
h3 = Entrez.esearch(db='pubmed', term=intersect_term, usehistory='y', WebEnv=webenv, retmax=0)
r3 = Entrez.read(h3)
h3.close()
time.sleep(DELAY)

print('=== Part A: history-server chained intersection ===')
print(f'BRCA1 AND breast cancer: {r1["Count"]}')
print(f'review[PT] AND 2024[PDAT]: {r2["Count"]}')
print(f'Intersection (2024 reviews about BRCA1/breast cancer): {r3["Count"]}')

assert int(r3['Count']) <= int(r1['Count']), 'intersection cannot exceed either input set'
assert int(r3['Count']) <= int(r2['Count']), 'intersection cannot exceed either input set'

# Part B: unrelated spell-check in the same request
h4 = Entrez.espell(db='pubmed', term='breast canser')
r4 = Entrez.read(h4)
h4.close()
print('\n=== Part B: spell-check ===')
print(f'Original: breast canser')
print(f'Corrected: {r4["CorrectedQuery"]}')
assert 'cancer' in r4['CorrectedQuery'], 'expected canser -> cancer correction'
print('\nASSERT OK: intersection <= both parents; spell correction contains "cancer"')
