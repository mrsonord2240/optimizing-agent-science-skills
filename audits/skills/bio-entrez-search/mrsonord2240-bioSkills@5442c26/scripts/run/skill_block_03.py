CURATED_DBS = ['pubmed', 'pmc', 'nucleotide', 'protein', 'gene', 'sra', 'gds', 'bioproject', 'biosample', 'clinvar']

def cross_db_counts(term, dbs=CURATED_DBS):
    counts = {}
    for db in dbs:
        h = Entrez.esearch(db=db, term=term, retmax=0)
        r = Entrez.read(h); h.close()
        counts[db] = int(r['Count'])
        time.sleep(0.34)
    return counts
