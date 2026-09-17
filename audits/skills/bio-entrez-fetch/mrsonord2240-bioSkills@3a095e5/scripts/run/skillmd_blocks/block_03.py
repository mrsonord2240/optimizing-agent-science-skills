def bulk_summaries(db, ids, chunk=500):
    out = []
    for i in range(0, len(ids), chunk):
        h = Entrez.esummary(db=db, id=','.join(ids[i:i+chunk]))
        out.extend(Entrez.read(h)); h.close()
        time.sleep(0.1 if Entrez.api_key else 0.34)
    return out

def organism_of(s):
    '''No direct Organism field on current nucleotide docsums -- derive from Title.'''
    org = s.get('Organism')
    if org:
        return org
    words = s.get('Title', '').split()
    return ' '.join(words[:2]) if len(words) >= 2 else s.get('Title', '?')

records = bulk_summaries('nucleotide', uid_list)
for s in records:
    print(s['AccessionVersion'], s['Length'], organism_of(s))
