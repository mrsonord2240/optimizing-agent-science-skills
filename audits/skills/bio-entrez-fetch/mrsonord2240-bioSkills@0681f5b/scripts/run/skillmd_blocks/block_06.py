h = Entrez.esearch(db='nucleotide', term='Homo sapiens[ORGN] AND srcdb_refseq[PROP] AND biomol_mrna[PROP]',
                   usehistory='y', retmax=0)
r = Entrez.read(h); h.close()
total = int(r['Count'])

with open('out.fasta', 'w') as out:
    for start in range(0, total, 500):
        h = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text',
                          retstart=start, retmax=500,
                          webenv=r['WebEnv'], query_key=r['QueryKey'])
        out.write(h.read()); h.close()
        time.sleep(0.1 if Entrez.api_key else 0.34)
