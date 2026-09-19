from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
h = Entrez.elink(dbfrom='gene', db='clinvar', id='672', linkname='gene_clinvar')
r = Entrez.read(h); h.close()
ids = [l['Id'] for l in r[0]['LinkSetDb'][0]['Link']] if r[0]['LinkSetDb'] else []
print(f'gene_clinvar for BRCA1 (672): {len(ids)} linked ClinVar records')
print(f'First 5 UIDs: {ids[:5]}')
