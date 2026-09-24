# Input 4 (Variant B, post-fix regression 2026-09-15): "Pull every ClinVar P/LP VariationID in BRCA1 for a research curation
# table and tell me how many there are." Live E-utilities; SKILL.md clinvar_search_gene verbatim (../p_skill_code.py).
import sys, time, requests
sys.path.insert(0, '..')
from p_skill_code import clinvar_search_gene, EUTILS
t0 = time.time()
count, ids = clinvar_search_gene('BRCA1', pathogenic_only=True)
print(f'P/LP: count={count} ids returned={len(ids)} unique={len(set(ids))} ({time.time()-t0:.0f}s)')
time.sleep(0.4)
c2, ids2 = clinvar_search_gene('BRCA1', max_ids=1200)
print(f'all BRCA1 with max_ids=1200: count={c2} ids returned={len(ids2)} (stops after the page that reaches max_ids)')
time.sleep(0.4)
r = requests.get(f'{EUTILS}/esummary.fcgi', params={'db': 'clinvar', 'id': ','.join(ids[:200]), 'retmode': 'json'}, timeout=60).json()['result']
multi = [u for u in r['uids'] if len(r[u].get('genes', [])) > 1]
print('of first 200 P/LP ids, records listing >1 gene:', len(multi), '(the docstring says to check esummary genes)')
