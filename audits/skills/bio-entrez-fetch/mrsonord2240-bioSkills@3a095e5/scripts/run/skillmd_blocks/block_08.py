def lineage(txid):
    h = Entrez.efetch(db='taxonomy', id=str(txid), retmode='xml')
    record = Entrez.read(h)[0]; h.close()
    return record['Lineage'], record['ScientificName']
