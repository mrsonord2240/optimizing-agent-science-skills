'''Input 11 (NEW) -- live regression of exact-node taxonomy guidance.

Prompt: "Compare a taxonomy-walked Mammalia search with the exact-node form. Confirm that
`:noexp`, rather than `:exp`, is the form that removes descendant expansion."
'''
import time
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

counts = {}
for term in ('Mammalia[ORGN]', 'Mammalia[ORGN:exp]', 'Mammalia[ORGN:noexp]'):
    handle = Entrez.esearch(db='nucleotide', term=term, retmax=0)
    record = Entrez.read(handle)
    handle.close()
    counts[term] = int(record['Count'])
    print(f'{term}: {counts[term]:,}; translation={record["QueryTranslation"]!r}')
    time.sleep(0.34)

assert counts['Mammalia[ORGN]'] == counts['Mammalia[ORGN:exp]'], ':exp should retain expansion'
assert counts['Mammalia[ORGN:noexp]'] < counts['Mammalia[ORGN]'], ':noexp should narrow to the exact node'
print('ASSERT OK: exact-node guidance uses :noexp and is live-verified')
