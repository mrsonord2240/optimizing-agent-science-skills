# Corrected-access variant, to confirm rest of pubmed_full() works once PMC-ID extraction is fixed.
from Bio import Entrez
Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'

h = Entrez.efetch(db='pubmed', id='35412348', retmode='xml')
records = Entrez.read(h); h.close()
article = records['PubmedArticle'][0]
citation = article['MedlineCitation']
mesh = [m['DescriptorName'] for m in citation.get('MeshHeadingList', [])]
title = citation['Article']['ArticleTitle']
journal = citation['Article']['Journal']['Title']
grants = citation.get('Article', {}).get('GrantList', [])
pmc_id = next((str(i) for i in article.get('PubmedData', {}).get('ArticleIdList', [])
               if i.attributes.get('IdType') == 'pmc'), None)
print(f'Title: {title}')
print(f'Journal: {journal}')
print(f'MeSH terms: {len(mesh)}')
print(f'Grants: {len(grants)}')
print(f'PMC ID: {pmc_id}')
