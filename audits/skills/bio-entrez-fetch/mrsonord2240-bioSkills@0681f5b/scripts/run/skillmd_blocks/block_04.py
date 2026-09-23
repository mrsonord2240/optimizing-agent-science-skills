def cds_proteins(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='fasta_cds_aa', retmode='text')
    return list(SeqIO.parse(h, 'fasta'))

proteins = cds_proteins('NC_000913.3')  # E. coli K-12 genome
print(f'{len(proteins)} CDS-translated proteins')
