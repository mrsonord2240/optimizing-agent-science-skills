def stream_all_ids(db, term, batch_size=10000):
    h = Entrez.esearch(db=db, term=term, retmax=0)
    total = int(Entrez.read(h)['Count']); h.close()
    delay = 0.1 if Entrez.api_key else 0.34
    for start in range(0, total, batch_size):
        h = Entrez.esearch(db=db, term=term, retstart=start, retmax=batch_size)
        r = Entrez.read(h); h.close()
        for uid in r['IdList']:
            yield uid
        time.sleep(delay)
