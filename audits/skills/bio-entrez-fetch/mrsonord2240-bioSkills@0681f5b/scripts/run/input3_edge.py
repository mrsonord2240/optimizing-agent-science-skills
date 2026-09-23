"""
Input 3 (Edge, regression of pre-fix Input 3 -- unaffected by the fix, re-verified here):
"Download all CDS translations from RefSeq NC_000913.3 (E. coli K-12) using
rettype='fasta_cds_aa'. I want to know how many proteins came back and the length of the first
one."

SKILL.md's own "Extract CDS in one round-trip" fenced block (block_04), verbatim.
"""
from Bio import Entrez, SeqIO

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'


def cds_proteins(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='fasta_cds_aa', retmode='text')
    return list(SeqIO.parse(h, 'fasta'))


proteins = cds_proteins('NC_000913.3')  # E. coli K-12 genome
print(f'{len(proteins)} CDS-translated proteins')
print(f'FIRST_ID={proteins[0].id}')
print(f'FIRST_LEN={len(proteins[0].seq)}')
