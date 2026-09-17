"""
Input 3 (Variant B) - "Find every RefSeq mRNA for Homo sapiens. The total is large -- use
the history server (usehistory='y') so downstream EFetch can pull in chunks without
re-sending IDs."

Follows SKILL.md "History server for downstream EFetch" pattern.
"""
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'

h = Entrez.esearch(db='nucleotide',
                    term='Homo sapiens[ORGN] AND srcdb_refseq[PROP] AND biomol_mrna[PROP]',
                    usehistory='y', retmax=0)
r = Entrez.read(h)
h.close()
webenv, query_key, count = r['WebEnv'], r['QueryKey'], int(r['Count'])
print(f'{count} mRNAs queued on history server; WebEnv len={len(webenv)}, QueryKey={query_key}')

assert count > 9999, 'this query is expected to exceed the documented 9,999 non-history cap'
assert webenv, 'WebEnv must be returned for usehistory=y'
assert query_key, 'QueryKey must be returned for usehistory=y'
print('ASSERT OK: count exceeds 9999 (the scenario history-server is meant to solve), WebEnv/QueryKey present')
