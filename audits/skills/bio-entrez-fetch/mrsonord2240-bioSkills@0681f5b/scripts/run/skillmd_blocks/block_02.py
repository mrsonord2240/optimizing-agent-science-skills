def fetch_genbank(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='gb', retmode='text')
    record = SeqIO.read(h, 'genbank'); h.close()
    return record

gb = fetch_genbank('NM_007294.4')
for feat in gb.features:
    if feat.type == 'CDS':
        print(feat.location, feat.qualifiers.get('product', ['?'])[0])
