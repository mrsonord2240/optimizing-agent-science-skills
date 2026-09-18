'''Input 1 (Canonical) -- regression of pre-fix Input 1.
Prompt: "Search PubMed for 2024 papers on tumor-mutational-burden in non-small-cell lung cancer.
Print the QueryTranslation, then return the count and first 20 PMIDs."
Uses SKILL.md block 06 (search_ncbi), extracted verbatim from the shipped SKILL.md.
'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

# --- verbatim from skill_block_06.py (SKILL.md "Single search with explicit retmax") ---
exec(open('skill_block_06.py', encoding='utf-8').read())
# defines search_ncbi(db, term, max_results=100)

term = 'tumor mutational burden[TIAB] AND non-small-cell lung cancer[TIAB] AND 2024[PDAT]'
ids, count, translation = search_ncbi('pubmed', term, max_results=20)
print(f'Count: {count}')
print(f'Translation: {translation}')
print(f'Returned {len(ids)} PMIDs (capped at 20): {ids[:5]} ...')
assert count > 0, 'expected nonzero hits'
assert len(ids) <= 20
assert translation, 'expected non-empty QueryTranslation'
print('ASSERT OK')
