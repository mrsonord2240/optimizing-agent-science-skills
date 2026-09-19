'''Corrected discover_links.py: LinkName not Name; MenuTag guarded with .get() since
some LinkInfo entries omit it entirely (per TOOLS.md notes for this env).'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34


def discover_links(dbfrom, source_id):
    h = Entrez.elink(dbfrom=dbfrom, id=source_id, cmd='acheck')
    r = Entrez.read(h); h.close()
    info = r[0]['IdCheckList']['IdLinkSet'][0]['LinkInfo']
    return [(i['LinkName'], i['DbTo'], i.get('MenuTag', '<none>')) for i in info]


print('=== Gene 672 (BRCA1): all available link tables ===')
gene_links = discover_links('gene', '672')
for name, target, label in gene_links:
    print(f'  {name:<42} -> {target:<14} ({label})')
print(f'Total linknames: {len(gene_links)}')
time.sleep(DELAY)

print('\n=== Nucleotide UID 31322957 (NM_007294.4): link tables ===')
nuc_links = discover_links('nucleotide', '31322957')
missing_menutag = [n for n, t, l in nuc_links if l == '<none>']
for name, target, label in nuc_links:
    print(f'  {name:<42} -> {target:<14} ({label})')
print(f'Total linknames: {len(nuc_links)}; missing MenuTag: {missing_menutag}')
time.sleep(DELAY)

print('\n=== PubMed 35412348: link tables ===')
pm_links = discover_links('pubmed', '35412348')
has_pubmed_gene = [n for n, t, l in pm_links if 'pubmed_gene' in n]
for name, target, label in pm_links:
    print(f'  {name:<42} -> {target:<14} ({label})')
print(f'Total linknames: {len(pm_links)}; pubmed_gene* entries present: {has_pubmed_gene}')
