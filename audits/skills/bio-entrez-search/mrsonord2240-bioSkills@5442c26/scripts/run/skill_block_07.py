h = Entrez.esearch(db='nucleotide',
                   term='Homo sapiens[ORGN] AND srcdb_refseq[PROP] AND biomol_mrna[PROP]',
                   usehistory='y', retmax=0)
r = Entrez.read(h); h.close()
webenv, query_key, count = r['WebEnv'], r['QueryKey'], int(r['Count'])
print(f'{count} mRNAs queued on history server; use webenv/query_key with efetch')
