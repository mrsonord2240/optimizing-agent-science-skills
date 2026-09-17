"""
Input 1 (Canonical) - "Search PubMed for 2024 papers on tumor-mutational-burden in
non-small-cell lung cancer. Print the QueryTranslation so I can lock the exact
field-qualified rewrite into my code, then return the count and first 20 PMIDs."

Follows SKILL.md "Inspect the translation before trusting a query" pattern +
"Single search with explicit retmax" pattern.
"""
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'
DELAY = 0.34


def search_ncbi(db, term, max_results=100):
    handle = Entrez.esearch(db=db, term=term, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    count = int(record['Count'])
    if count > max_results:
        print(f'WARNING: {count} matched, returning first {max_results}; use history server for full set')
    return record['IdList'], count, record['QueryTranslation']


term = 'tumor mutational burden[TIAB] AND non-small-cell lung cancer[TIAB] AND 2024[PDAT]'
ids, count, translation = search_ncbi('pubmed', term, max_results=20)

print(f'Query: {term}')
print(f'Count: {count}')
print(f'QueryTranslation: {translation}')
print(f'First {len(ids)} PMIDs: {ids}')
assert count > 0, 'expected nonzero hits for a real, well-populated 2024 topic'
assert len(ids) <= 20, 'retmax=20 must not be exceeded'
assert isinstance(translation, str) and len(translation) > 0, 'QueryTranslation must be present'
print('ASSERT OK: count>0, len(ids)<=20, translation present')
