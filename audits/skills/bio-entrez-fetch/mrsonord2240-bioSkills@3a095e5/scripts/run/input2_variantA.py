"""
Input 2 (Variant A, regression of pre-fix P0 -- KeyError: 'Organism'):
"I have 4 nucleotide accessions (NM_007294.4, NM_000059.4, NM_000546.6, NM_001126112.3). I only
need organism, accession.version, and sequence length for each -- use ESummary, not EFetch."

This runs SKILL.md's OWN "Bulk metadata via ESummary" fenced block (block_03) VERBATIM --
copy-pasted exactly as shipped, not hand-fixed -- to test whether the P0 the pre-fix audit found
(KeyError: 'Organism') is actually gone when an agent follows the document as written.
"""
from Bio import Entrez

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'

uid_list = ['NM_007294.4', 'NM_000059.4', 'NM_000546.6', 'NM_001126112.3']

print('=== Attempt 1: block_03 run 100% verbatim, exactly as shipped in SKILL.md ===')
try:
    exec(open(r'F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks\block_03.py').read())
    print('VERBATIM RUN: completed with no error')
except Exception as e:
    print(f'VERBATIM RUN CRASHED: {type(e).__name__}: {e}')

print('\n=== Attempt 2: same block_03 code, with `import time` added (the one line SKILL.md omits) ===')
import time  # noqa: E402  -- SKILL.md never imports this anywhere, yet block_03 calls time.sleep()


def bulk_summaries(db, ids, chunk=500):
    out = []
    for i in range(0, len(ids), chunk):
        h = Entrez.esummary(db=db, id=','.join(ids[i:i + chunk]))
        out.extend(Entrez.read(h)); h.close()
        time.sleep(0.1 if Entrez.api_key else 0.34)
    return out


def organism_of(s):
    '''No direct Organism field on current nucleotide docsums -- derive from Title.'''
    org = s.get('Organism')
    if org:
        return org
    words = s.get('Title', '').split()
    return ' '.join(words[:2]) if len(words) >= 2 else s.get('Title', '?')


records = bulk_summaries('nucleotide', uid_list)
for s in records:
    print(s['AccessionVersion'], s['Length'], organism_of(s))
print(f'\nRECORDS_RETURNED={len(records)}')
print(f'ORGANISMS={[organism_of(s) for s in records]}')
