"""
Input 1 (Canonical, regression of pre-fix Input 1 -- unaffected by the fix, re-verified here):
"Fetch the GenBank record for NM_007294.4 and tell me the CDS count, sequence length, and the
product of the first CDS feature."

This is SKILL.md's own "Required Setup" (block_01) + "Single sequence by accession" (block_02)
fenced code blocks, concatenated VERBATIM in document order (the extraction method in
extract_skillmd_blocks.py), with only the placeholder email swapped for the audit identifier.
No hand-transcription.
"""
from Bio import Entrez, SeqIO

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'


def fetch_genbank(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='gb', retmode='text')
    record = SeqIO.read(h, 'genbank'); h.close()
    return record


gb = fetch_genbank('NM_007294.4')
for feat in gb.features:
    if feat.type == 'CDS':
        print(feat.location, feat.qualifiers.get('product', ['?'])[0])

# Extra assertions beyond the raw block's own print, checked against the tooling pass's cached
# reference F:\OpenScience\audit-envs\database-access\public-data\entrez-fetch\NM_007294.4.gb
print(f'\nACCESSION={gb.id}')
print(f'LENGTH={len(gb.seq)}')
cds = [f for f in gb.features if f.type == 'CDS']
print(f'CDS_COUNT={len(cds)}')
print(f'FIRST_PRODUCT={cds[0].qualifiers.get("product", ["?"])[0] if cds else None}')
