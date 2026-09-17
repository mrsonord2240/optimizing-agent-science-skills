"""
Input 5 (Stress): "Convert these SRA UIDs to SRR run accessions plus Bases/Spots/AvgLength
metrics using EFetch with rettype='runinfo'. Parse the CSV and print as a table."

Follows SKILL.md 'SRA UID -> SRR accession + run metrics' pattern (sra_runinfo()) verbatim.
UIDs resolved from real SRR accessions (SRR000001, SRR000002) via a one-off ESearch, then
passed into the Skill's own documented EFetch code pattern -- the ESearch step itself is
setup, not part of this Skill's scope, matching how a real multi-step research session would
hand this Skill a UID list obtained elsewhere.
"""
from Bio import Entrez
import time

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'

# --- setup: resolve UIDs for two known SRR accessions (not part of entrez-fetch's own scope) ---
h = Entrez.esearch(db='sra', term='SRR000001 OR SRR000002', retmax=5)
setup = Entrez.read(h)
h.close()
uids = setup['IdList']
print(f'Resolved UIDs (setup step): {uids}')
time.sleep(0.34)


def sra_runinfo(uids):
    h = Entrez.efetch(db='sra', id=','.join(uids), rettype='runinfo', retmode='text')
    text = h.read()
    h.close()
    lines = text.strip().split('\n')
    header = lines[0].split(',')
    return [dict(zip(header, row.split(','))) for row in lines[1:]]


rows = sra_runinfo(uids)
for row in rows:
    print(row.get('Run', '?'), row.get('bases', row.get('Bases', '?')),
          row.get('spots', row.get('Spots', '?')))
