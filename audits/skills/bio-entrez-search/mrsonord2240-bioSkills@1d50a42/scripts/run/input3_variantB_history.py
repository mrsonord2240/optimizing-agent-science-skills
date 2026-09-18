'''Input 3 (Variant B) -- regression of pre-fix Input 3, new term (human RefSeq protein, not mRNA).
Prompt: "Find every RefSeq protein for Homo sapiens. Use the history server so downstream
EFetch can pull in chunks without re-sending IDs."
Uses SKILL.md block 08 (history-server pattern), adapted db/term but structure verbatim.
'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

h = Entrez.esearch(db='protein',
                   term='Homo sapiens[ORGN] AND srcdb_refseq[PROP]',
                   usehistory='y', retmax=0)
r = Entrez.read(h); h.close()
webenv, query_key, count = r['WebEnv'], r['QueryKey'], int(r['Count'])
print(f'{count} proteins queued on history server; WebEnv len={len(webenv)}, QueryKey={query_key}')
assert count > 9999, 'expected a large count justifying history-server use'
assert webenv and query_key
print('ASSERT OK')
