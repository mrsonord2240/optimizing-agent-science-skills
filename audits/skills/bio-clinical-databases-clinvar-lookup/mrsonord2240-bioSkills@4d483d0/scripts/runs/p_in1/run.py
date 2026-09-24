# Input 1 (Canonical, post-fix regression 2026-09-15): "Look up ClinVar VariationID 17661: germline classification,
# review status, star rating, last evaluated date, expert-panel status, and its ClinGen CA ID."
# Live NCBI E-utilities + ClinGen Allele Registry. SKILL.md code verbatim (../p_skill_code.py).
import json, sys, time
sys.path.insert(0, '..')
from p_skill_code import clinvar_summary, car_id
print('== clinvar_summary(17661) ==')
print(json.dumps(clinvar_summary(17661), indent=1)); time.sleep(0.4)
print('== car_id on the post-fix demo HGVS NC_000017.11:g.43106487A>C ==')
print(repr(car_id('NC_000017.11:g.43106487A>C'))); time.sleep(0.4)
print('== car_id on the pre-fix (wrong-REF) demo NC_000017.11:g.43094464G>A ==')
try:
    print(repr(car_id('NC_000017.11:g.43094464G>A')))
except ValueError as e:
    print('ValueError:', e)
