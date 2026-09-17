"""
Input 1 (Canonical): "Fetch the GenBank record for NM_007294.4 and tell me the CDS count,
sequence length, and the product of the first CDS feature."

Follows SKILL.md 'Single sequence by accession' pattern verbatim (fetch_genbank()).
"""
from Bio import Entrez, SeqIO

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'


def fetch_genbank(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='gb', retmode='text')
    record = SeqIO.read(h, 'genbank')
    h.close()
    return record


gb = fetch_genbank('NM_007294.4')
cds_features = [f for f in gb.features if f.type == 'CDS']
print(f'Accession: {gb.id}')
print(f'Description: {gb.description}')
print(f'Length: {len(gb.seq)} nt')
print(f'CDS feature count: {len(cds_features)}')
if cds_features:
    first = cds_features[0]
    print(f'First CDS location: {first.location}')
    print(f'First CDS product: {first.qualifiers.get("product", ["?"])[0]}')
