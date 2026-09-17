"""
Input 4 (Variant B): "Pull the full PubMed XML for PMID 35412348 -- I need the title, journal,
MeSH term count, grant count, and PMC ID (not just the abstract)."

Follows SKILL.md 'Pull PubMed with structured MeSH' pattern (pubmed_full()), extended with the
PMC-ID extraction shown in examples/fetch_pubmed.py, since the user explicitly asked for PMC ID.
"""
from Bio import Entrez

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'


def pubmed_full(pmid):
    h = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    records = Entrez.read(h)
    h.close()
    article = records['PubmedArticle'][0]
    citation = article['MedlineCitation']
    mesh = [m['DescriptorName'] for m in citation.get('MeshHeadingList', [])]
    title = citation['Article']['ArticleTitle']
    journal = citation['Article']['Journal']['Title']
    grants = citation.get('Article', {}).get('GrantList', [])
    # PMC ID extraction exactly as shipped in examples/fetch_pubmed.py
    pmc_id = next((id['#text'] for id in article.get('PubmedData', {}).get('ArticleIdList', [])
                   if hasattr(id, 'attributes') and id.attributes.get('IdType') == 'pmc'), None)
    return {'pmid': pmid, 'title': title, 'journal': journal, 'mesh': mesh,
            'grants': grants, 'pmc_id': pmc_id}


result = pubmed_full('35412348')
print(f"Title: {result['title']}")
print(f"Journal: {result['journal']}")
print(f"MeSH terms: {len(result['mesh'])}")
print(f"Grants: {len(result['grants'])}")
print(f"PMC ID: {result['pmc_id'] or 'not in PMC'}")
