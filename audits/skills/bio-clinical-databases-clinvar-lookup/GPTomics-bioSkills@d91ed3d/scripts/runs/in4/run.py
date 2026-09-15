# Input 4 (Variant B): "Pull every ClinVar P/LP VariationID in BRCA1 for a research curation table and tell me how
# many there are." Live E-utilities; SKILL.md clinvar_search_gene verbatim.
import sys, time, requests
sys.path.insert(0, '..')
from skill_code import clinvar_search_gene, clinvar_summary, EUTILS

ids_all = clinvar_search_gene('BRCA1'); time.sleep(0.4)
ids_pl = clinvar_search_gene('BRCA1', pathogenic_only=True); time.sleep(0.4)
print('SKILL.md clinvar_search_gene: all ->', len(ids_all), ' P/LP ->', len(ids_pl))
for term in ('BRCA1[gene]', 'BRCA1[gene] AND (clinsig_pathogenic[Properties] OR clinsig_likely_pathogenic[Properties])'):
    r = requests.get(f'{EUTILS}/esearch.fcgi', params={'db': 'clinvar', 'term': term, 'retmax': 0, 'retmode': 'json'}, timeout=30).json()
    print('esearch count for', repr(term), '=', r['esearchresult']['count']); time.sleep(0.4)
print('\nfirst 5 P/LP ids -> germline class / title:')
for vid in ids_pl[:5]:
    s = clinvar_summary(vid); time.sleep(0.4)
    print(vid, s['germline_class'], '|', s['germline_review_status'], '|', s['name'][:70])
# multi-gene records captured by [gene]
r = requests.get(f'{EUTILS}/esummary.fcgi', params={'db': 'clinvar', 'id': ','.join(ids_pl[:200]), 'retmode': 'json'}, timeout=60).json()['result']
multi = [u for u in r['uids'] if len(r[u].get('genes', [])) > 1]
print('\nof first 200 P/LP ids, records spanning >1 gene (CNVs etc.):', len(multi), [r[u]['title'][:60] for u in multi[:3]])
