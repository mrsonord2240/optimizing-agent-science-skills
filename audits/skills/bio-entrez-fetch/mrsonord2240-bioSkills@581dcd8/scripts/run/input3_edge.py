"""
Input 3 (Edge): "Download all CDS translations from RefSeq NC_000913.3 (E. coli K-12) using
rettype='fasta_cds_aa'. Don't walk the GenBank features manually -- let NCBI extract and
translate server-side. I want to know how many proteins came back and the length of the
first one." (usage-guide.md 'One-shot CDS extraction' example, boundary case: whole-genome
record with thousands of CDS in a single EFetch call.)
"""
from Bio import Entrez, SeqIO

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'


def cds_proteins(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='fasta_cds_aa', retmode='text')
    records = list(SeqIO.parse(h, 'fasta'))
    h.close()
    return records


proteins = cds_proteins('NC_000913.3')
print(f'{len(proteins)} CDS-translated proteins')
if proteins:
    print(f'First: {proteins[0].id}  length={len(proteins[0].seq)}')
    print(f'First 60 aa: {str(proteins[0].seq)[:60]}')
