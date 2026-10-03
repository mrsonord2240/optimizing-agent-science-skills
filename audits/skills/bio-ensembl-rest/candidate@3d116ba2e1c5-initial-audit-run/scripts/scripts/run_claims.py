"""Doc-claim probes for bio-ensembl-rest: divisions, endpoint table, species-name rule, archives, POST batch."""
import os
import sys
import time

sys.dont_write_bytecode = True
import requests

H = {'Accept': 'application/json'}
B = 'https://rest.ensembl.org'


def get(url, **kw):
    try:
        r = requests.get(url, headers=H, timeout=40, **kw)
        body = r.text[:230].replace('\n', ' ')
        return r.status_code, body
    except Exception as e:  # noqa
        return 'EXC', f'{type(e).__name__}: {str(e)[:150]}'
    finally:
        time.sleep(0.1)


def show(label, res):
    print(f'--- {label}\n    {res}')


r = requests.get(f'{B}/info/divisions', headers=H, timeout=40).json()
show('/info/divisions', r)
time.sleep(0.1)
r = requests.get(f'{B}/info/species', params={'division': 'EnsemblPlants'}, headers=H, timeout=60).json()
show('/info/species?division=EnsemblPlants count + arabidopsis', (len(r['species']), [s['name'] for s in r['species'] if 'arabidopsis' in s['name']]))
time.sleep(0.1)
show('lookup arabidopsis_thaliana NAC001', get(f'{B}/lookup/symbol/arabidopsis_thaliana/NAC001'))
show('rest.ensemblgenomes.org DNS', get('https://rest.ensemblgenomes.org/info/ping'))
show('Homo_sapiens capitalised', get(f'{B}/lookup/symbol/Homo_sapiens/BRCA1'))
show('homo_sapiens', get(f'{B}/lookup/symbol/homo_sapiens/BRCA1')[0])
show('MARCH1 (documented 404)', get(f'{B}/lookup/symbol/human/MARCH1'))
show('MARCHF1', get(f'{B}/lookup/symbol/human/MARCHF1')[0])
show('SEPT7 old symbol', get(f'{B}/lookup/symbol/human/SEPT7'))
show('xrefs/symbol/human/BRCA1', get(f'{B}/xrefs/symbol/human/BRCA1'))
show('overlap/id without feature', get(f'{B}/overlap/id/ENSG00000012048'))
show('overlap/id?feature=transcript', get(f'{B}/overlap/id/ENSG00000012048', params={'feature': 'transcript'})[0])
show('variation/human/rs699', get(f'{B}/variation/human/rs699'))
show('regulatory table form /regulatory/species/human/feature/ENSR00000000001', get(f'{B}/regulatory/species/human/feature/ENSR00000000001'))
show('regulatory actual form /regulatory/human/ENSR00000000001', get(f'{B}/regulatory/human/ENSR00000000001'))
show('regulatory /regulatory/species/human/id/ENSR00000000001', get(f'{B}/regulatory/species/human/id/ENSR00000000001'))
show('genetree/id with member? /genetree/member/id/ENSG00000012048', get(f'{B}/genetree/member/id/ENSG00000012048', params={'content-type': 'application/json'})[0])
show('homology/id', get(f'{B}/homology/id/human/ENSG00000012048', params={'type': 'orthologues', 'target_species': 'mouse'})[0])
show('homology/id (usage as in SKILL.md, no species)', get(f'{B}/homology/id/ENSG00000012048', params={'type': 'orthologues', 'target_species': 'mouse'}))
show('ga4gh/features/search? ping', get(f'{B}/ga4gh/references/1')[0])
r = requests.post(f'{B}/lookup/id', json={'ids': ['ENSG00000012048', 'ENSG00000141510']}, headers={**H, 'Content-Type': 'application/json'}, timeout=40)
show('POST /lookup/id batch', (r.status_code, {k: v.get('display_name') for k, v in r.json().items()}))
time.sleep(0.1)
for rel in ('e110', 'e111', 'e116', 'e90'):
    code = get(f'https://{rel}.rest.ensembl.org/info/data')
    show(f'archive {rel} /info/data (follows redirect)', code)
show('jun2026 host direct', get('https://jun2026.rest.ensembl.org/info/ping'))
show('jul2023 host direct', get('https://jul2023.rest.ensembl.org/info/ping'))
show('region example with 1000 base window VEP', get(f'{B}/vep/human/region/9:22125503-22125502:1/C')[0])
