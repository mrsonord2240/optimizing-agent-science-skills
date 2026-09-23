def pubmed_full(pmid):
    h = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    records = Entrez.read(h); h.close()
    article = records['PubmedArticle'][0]
    citation = article['MedlineCitation']
    mesh = [m['DescriptorName'] for m in citation.get('MeshHeadingList', [])]
    title = citation['Article']['ArticleTitle']
    # ArticleIdList entries are StringElement (a str subclass with .attributes), not
    # {'#text': ...} dicts, on Biopython 1.88 -- id['#text'] raises TypeError. Use str(id).
    ids = article.get('PubmedData', {}).get('ArticleIdList', [])
    pmc_id = next((str(i) for i in ids if i.attributes.get('IdType') == 'pmc'), None)
    return {'pmid': pmid, 'title': title, 'mesh': mesh, 'pmc_id': pmc_id}
