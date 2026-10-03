"""Follow-up probes: regulatory endpoint with a real feature id, xrefs retry, e90 archive via the client, homology/id forms."""
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(r'F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest', 'scripts'))
import requests
from ensembl_client import genes_in_region, symbol_to_id

H = {'Accept': 'application/json'}
B = 'https://rest.ensembl.org'


def get(url, **kw):
    try:
        r = requests.get(url, headers=H, timeout=90, **kw)
        return r.status_code, r.text[:200].replace('\n', ' ')
    except Exception as e:  # noqa
        return 'EXC', f'{type(e).__name__}: {str(e)[:120]}'
    finally:
        time.sleep(0.15)


regs = genes_in_region('human', '17:43044295-43045295', feature='regulatory')
print('regulatory overlap in BRCA1 promoter window:', [(g['id'], g.get('description')) for g in regs[:3]])
if regs:
    rid = regs[0]['id']
    print('table form  /regulatory/species/human/feature/ID:', get(f'{B}/regulatory/species/human/feature/{rid}'))
    print('actual form /regulatory/human/ID:', get(f'{B}/regulatory/human/{rid}', params={'activity': 1}))
    print('actual form /regulatory/human/ID (no params):', get(f'{B}/regulatory/human/{rid}'))
print('xrefs/symbol retry:', get(f'{B}/xrefs/symbol/human/BRCA1'))
print('homology/id/human/ID:', get(f'{B}/homology/id/human/ENSG00000012048', params={'target_species': 'mouse'}))
try:
    symbol_to_id('human', 'BRCA1', base='https://e90.rest.ensembl.org')
except Exception as e:  # noqa
    print('client on e90 archive ->', type(e).__name__, str(e)[:160])
print('jun2026 host again:', get('https://jun2026.rest.ensembl.org/info/ping')[0])
