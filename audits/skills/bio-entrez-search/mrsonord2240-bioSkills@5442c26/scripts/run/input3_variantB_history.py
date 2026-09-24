'''Input 3 (Variant B) -- regression, history-server queue, human RefSeq protein set.'''
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
