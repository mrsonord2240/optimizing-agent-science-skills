'''Input 1 (Canonical) -- regression of prior re-audit Input 1.
Prompt: "Search PubMed for 2024 papers on tumor-mutational-burden in non-small-cell lung cancer.
Print the QueryTranslation, then return the count and first 20 PMIDs."
Uses the block defining search_ncbi, extracted programmatically from the shipped SKILL.md.
'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

for block_path in __import__('pathlib').Path('.').glob('skill_block_*.py'):
    block = block_path.read_text(encoding='utf-8')
    if 'def search_ncbi(' in block:
        exec(block)
        break
else:
    raise AssertionError('could not find search_ncbi in source-extracted blocks')

term = 'tumor mutational burden[TIAB] AND non-small-cell lung cancer[TIAB] AND 2024[PDAT]'
ids, count, translation = search_ncbi('pubmed', term, max_results=20)
print(f'Count: {count}')
print(f'Translation: {translation}')
print(f'Returned {len(ids)} PMIDs (capped at 20): {ids[:5]} ...')
assert count > 0, 'expected nonzero hits'
assert len(ids) <= 20
assert translation, 'expected non-empty QueryTranslation'
print('ASSERT OK')
