"""
Input 2 (Variant A): "I have 4 nucleotide accessions (NM_007294.4, NM_000059.4, NM_000546.6,
NM_001126112.3). I only need organism, accession.version, and sequence length for each --
use ESummary, not EFetch, since I don't need the sequence content."

Follows SKILL.md 'Bulk metadata via ESummary' pattern (bulk_summaries()) verbatim, and the
usage-guide.md 'Choosing ESummary over EFetch' example prompt almost word for word.
"""
import time
from Bio import Entrez

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'


def bulk_summaries(db, ids, chunk=500):
    out = []
    for i in range(0, len(ids), chunk):
        h = Entrez.esummary(db=db, id=','.join(ids[i:i + chunk]))
        out.extend(Entrez.read(h))
        h.close()
        time.sleep(0.34)
    return out


uid_list = ['NM_007294.4', 'NM_000059.4', 'NM_000546.6', 'NM_001126112.3']
records = bulk_summaries('nucleotide', uid_list)
for s in records:
    print(f'{s["AccessionVersion"]:<18} {s["Length"]:>8} nt   {s["Organism"]}')
