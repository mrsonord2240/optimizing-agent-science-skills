'''Regression check for Input 7 (clinical guardrail), on a gene NOT used in the
original audit (BRCA1) or the fix log's own verification (also BRCA1) -- TP53 --
to check the new SKILL.md guardrail text generalizes rather than being BRCA1-specific.'''
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

h = Entrez.elink(dbfrom='gene', db='clinvar', id='7157', linkname='gene_clinvar')
r = Entrez.read(h); h.close()
records = r[0]['LinkSetDb'][0]['Link'] if r[0]['LinkSetDb'] else []
print(f'gene_clinvar for TP53 (7157): {len(records)} linked ClinVar records')
print(f'First 5 UIDs: {[l["Id"] for l in records[:5]]}')
