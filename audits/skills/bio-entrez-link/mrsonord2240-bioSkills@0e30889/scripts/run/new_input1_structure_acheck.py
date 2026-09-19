'''RE-AUDIT NEW INPUT 1 (beyond fixer's scope): verify the acheck LinkName/MenuTag
fix generalizes to a db pair the fix log never tested (gene/nucleotide/pubmed only).
Realistic prompt: "Before I build a structure-annotation pipeline, show me every
linkname NCBI exposes for a PDB/MMDB structure record via cmd=acheck."'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34


def discover_links(dbfrom, source_id):
    h = Entrez.elink(dbfrom=dbfrom, id=source_id, cmd='acheck')
    r = Entrez.read(h); h.close()
    info = r[0]['IdCheckList']['IdLinkSet'][0]['LinkInfo']
    return [(i['LinkName'], i['DbTo'], i.get('MenuTag', '<none>')) for i in info]


# A real PDB-MMDB structure UID linked from TP53 (from chain_links.py's own output).
h = Entrez.elink(dbfrom='gene', db='protein', id='7157', linkname='gene_protein_refseq')
r = Entrez.read(h); h.close()
proteins = [l['Id'] for l in r[0]['LinkSetDb'][0]['Link'][:5]] if r[0]['LinkSetDb'] else []
time.sleep(DELAY)
h = Entrez.elink(dbfrom='protein', db='structure', id=','.join(proteins))
r = Entrez.read(h); h.close()
structure_uid = None
for ls in r:
    if ls['LinkSetDb']:
        structure_uid = ls['LinkSetDb'][0]['Link'][0]['Id']
        break
print(f'Using structure UID: {structure_uid}')
time.sleep(DELAY)

print('=== Structure UID acheck (db pair not covered by the fix log) ===')
missing_menutag = []
names = discover_links('structure', structure_uid)
for name, target, label in names:
    if label == '<none>':
        missing_menutag.append(name)
    print(f'  {name:<42} -> {target:<14} ({label})')
print(f'\nTotal linknames: {len(names)}; missing MenuTag: {missing_menutag}')
print('No KeyError raised -- LinkName/MenuTag fix generalizes beyond gene/nucleotide/pubmed.')

time.sleep(DELAY)
print('\n=== dbSNP acheck (another untested db pair) ===')
names2 = discover_links('snp', '7412')  # rs7412, APOE variant
missing2 = [n for n, t, l in names2 if l == '<none>']
for name, target, label in names2:
    print(f'  {name:<42} -> {target:<14} ({label})')
print(f'\nTotal linknames: {len(names2)}; missing MenuTag: {missing2}')
