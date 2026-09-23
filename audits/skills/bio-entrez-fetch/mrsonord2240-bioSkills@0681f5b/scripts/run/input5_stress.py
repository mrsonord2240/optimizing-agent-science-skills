"""
Input 5 (Stress, regression of pre-fix P0 -- TypeError: bytes vs str):
"Convert these SRA UIDs to SRR run accessions plus Bases/Spots/AvgLength metrics using EFetch
with rettype='runinfo'. Parse the CSV and print as a table."

SKILL.md's own inline "SRA UID -> SRR accession + run metrics" fenced block (block_07), verbatim.
UIDs resolved the same way the pre-fix audit did: ESearch db='sra' for a couple of real runs
(out-of-scope setup step, entrez-search's job, not entrez-fetch's).
"""
from Bio import Entrez
import time

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'


def sra_runinfo(uids):
    h = Entrez.efetch(db='sra', id=','.join(uids), rettype='runinfo', retmode='text')
    raw = h.read(); h.close()
    # db='sra' returns bytes here despite retmode='text' (Biopython 1.88) -- decode first.
    text = raw.decode() if isinstance(raw, bytes) else raw
    lines = text.strip().split('\n')
    header = lines[0].split(',')
    return [dict(zip(header, row.split(','))) for row in lines[1:]]


# out-of-scope setup: resolve a couple of real SRA UIDs via ESearch (entrez-search's job)
h = Entrez.esearch(db='sra', term='SRR000001[Accession] OR SRR000002[Accession]', retmax=5)
sr = Entrez.read(h); h.close()
uids = sr['IdList']
print(f'[setup] Resolved SRA UIDs: {uids}')
time.sleep(0.34)

rows = sra_runinfo(uids)
print(f'\nROWS_RETURNED={len(rows)}')
for r in rows:
    print({k: r.get(k) for k in ('Run', 'spots', 'bases', 'avgLength') if k in r})
