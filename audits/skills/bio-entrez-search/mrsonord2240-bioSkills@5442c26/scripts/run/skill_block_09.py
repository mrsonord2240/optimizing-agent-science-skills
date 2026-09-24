def list_fields(db):
    h = Entrez.einfo(db=db); r = Entrez.read(h); h.close()
    # Biopython 1.88 wraps DbInfo as a one-element list, not a dict -- index [0] first.
    return [(f['Name'], f['FullName'], f['Description']) for f in r['DbInfo'][0]['FieldList']]
