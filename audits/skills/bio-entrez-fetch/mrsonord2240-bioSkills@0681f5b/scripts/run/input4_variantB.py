"""
Input 4 (Variant B, regression of pre-fix P0 -- TypeError: string indices must be integers):
"Pull the full PubMed XML for PMID 35412348 -- I need the title, journal, MeSH term count, grant
count, and PMC ID."

SKILL.md's own "Pull PubMed with structured MeSH" fenced block (block_05), verbatim -- now
includes pmc_id in its return value.
"""
from Bio import Entrez

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'


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


result = pubmed_full('35412348')
print(result)
print(f"\nPMID={result['pmid']}")
print(f"TITLE={result['title']}")
print(f"MESH_COUNT={len(result['mesh'])}")
print(f"PMC_ID={result['pmc_id']}")
