# Input 1 (Canonical): "Look up ClinVar VariationID 17661 (BRCA1): germline classification, review status,
# star rating, last evaluated date, and whether an expert panel curated it. Also give me its ClinGen CA ID."
# Live NCBI E-utilities + ClinGen Allele Registry, 2026-09-15. SKILL.md code verbatim (../skill_code.py).
import json, sys, time
sys.path.insert(0, '..')
import requests
from skill_code import clinvar_summary, car_id, EUTILS

print('== SKILL.md clinvar_summary(17661) ==')
s = clinvar_summary(17661)
print(json.dumps(s, indent=1))
time.sleep(0.4)
raw = requests.get(f'{EUTILS}/esummary.fcgi', params={'db': 'clinvar', 'id': 17661, 'retmode': 'json'}, timeout=30).json()['result']['17661']
print('== raw eSummary keys ==')
print(sorted(raw.keys()))
print('germline_classification:', json.dumps(raw.get('germline_classification'), indent=1)[:900])
print('variation_set[0].variation_loc (GRCh38):', [l for l in raw.get('variation_set', [{}])[0].get('variation_loc', []) if l.get('assembly_name') == 'GRCh38'])
time.sleep(0.4)
print('== SKILL/example demo HGVS: car_id("NC_000017.11:g.43094464G>A") ==')
print(repr(car_id('NC_000017.11:g.43094464G>A')))
r = requests.put('https://reg.clinicalgenome.org/allele', headers={'Content-Type': 'text/plain'}, data='NC_000017.11:g.43094464G>A', timeout=30)
print('Allele Registry PUT status', r.status_code, r.text[:300].replace('\n', ' '))
time.sleep(0.4)
r = requests.get('https://reg.clinicalgenome.org/allele', params={'hgvs': 'NC_000017.11:g.43094464G>A'}, timeout=30)
print('Allele Registry GET ?hgvs= status', r.status_code, r.text[:200].replace('\n', ' '))
