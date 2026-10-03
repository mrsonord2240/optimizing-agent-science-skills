"""Follow-ups: full OMA mouse check, TP53 human->mouse Compara row schema, eggNOG scripted-access probe."""
import sys
import time

import requests

sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference/scripts')
import ortholog_clients as oc  # noqa: E402

try:
    oma = oc.oma_orthologs('P04637', rel_type='1:1')
    mouse = [o.get('canonicalid') or o.get('omaid') for o in oma if o['species']['code'] == 'MOUSE']
    print('OMA TP53 1:1 total', len(oma), 'mouse', mouse, 'keys', sorted(oma[0].keys()), 'species keys', sorted(oma[0]['species'].keys()), flush=True)
    print('PASS' if mouse == ['P53_MOUSE'] else 'FAIL', 'OMA mouse P53_MOUSE', flush=True)
except Exception as e:
    print('EXC OMA', type(e).__name__, str(e)[:200], flush=True)
time.sleep(1)
for attempt in (1, 2):
    try:
        rows = oc.compara_orthologs('human', 'TP53', 'mouse')
        print('Compara TP53 human->mouse', rows, flush=True)
        ok = len(rows) == 1 and rows[0]['target_id'] == 'ENSMUSG00000059552' and rows[0]['type'] == 'ortholog_one2one' \
            and rows[0]['taxonomy_level'] and rows[0]['confidence'] is None
        print('PASS' if ok else 'FAIL', 'Compara TP53 row schema', flush=True)
        break
    except Exception as e:
        print('EXC Compara attempt', attempt, type(e).__name__, str(e)[:200], flush=True)
        time.sleep(20)
for url in ('https://eggnog6.embl.de/api/', 'https://eggnogdb.org/api/'):
    try:
        r = requests.get(url, timeout=30, allow_redirects=True)
        print('eggNOG', url, r.status_code, r.url, len(r.text), flush=True)
    except Exception as e:
        print('eggNOG', url, type(e).__name__, str(e)[:160], flush=True)
