def sra_runinfo(uids):
    h = Entrez.efetch(db='sra', id=','.join(uids), rettype='runinfo', retmode='text')
    raw = h.read(); h.close()
    # db='sra' returns bytes here despite retmode='text' (Biopython 1.88) -- decode first.
    text = raw.decode() if isinstance(raw, bytes) else raw
    lines = text.strip().split('\n')
    header = lines[0].split(',')
    return [dict(zip(header, row.split(','))) for row in lines[1:]]
