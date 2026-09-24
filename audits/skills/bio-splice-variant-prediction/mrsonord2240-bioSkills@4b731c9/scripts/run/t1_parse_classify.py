"""Input 1: parse real SpliceAI D50 output on the GRCh37 chrX panel with the Skill's own splice_parsers, assert values.
Run from run/ in WSL env as-spvp: asenv as-spvp python t1_parse_classify.py"""
import sys
sys.path.insert(0, 'skill/examples')
import numpy as np, pandas as pd
from splice_parsers import (parse_spliceai_vcf, classify_delta, read_input_vcf, unscored_report)

s = parse_spliceai_vcf('out/sai_D50_M0.vcf')
inp = read_input_vcf('data/panel_grch37.vcf')
print('input variants', len(inp), '| parsed rows', len(s), '| unique keys', s['key'].nunique())
s['acmg'] = classify_delta(s['delta_max'])
# reduce per variant (max over genes) - what the SKILL/example say to do
per = s.sort_values('delta_max', ascending=False).drop_duplicates('key').set_index('key')
inp = inp.set_index('key')
tab = inp[['id']].join(per[['gene', 'delta_max', 'acmg']])
print(tab.to_string())
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# ground truth from raw INFO (independent regex-free read: split by '|')
raw = {}
for l in open('out/sai_D50_M0.vcf'):
    if l.startswith('#'): continue
    c = l.split('\t'); ann = c[7].split('SpliceAI=')[1].strip().split(',')
    raw[c[2]] = max(max(float(x) for x in a.split('|')[2:6]) for a in ann)
for vid, d in raw.items():
    got = tab.loc[tab['id'] == vid, 'delta_max'].iloc[0]
    chk(f'delta_max {vid} parser {got:.2f} == raw {d:.2f}', abs(got - d) < 1e-9)
canon = ['PLCXD1_donor_G>A', 'DMD_c.9563+1G>A', 'DMD_c.31+1G>A', 'GLA_c.370-1G>A']
for v in canon:
    chk(f'{v} >= 0.8 PP3_supporting_prec0.8', raw[v] >= 0.8 and tab.loc[tab['id'] == v, 'acmg'].iloc[0] == 'PP3_supporting_prec0.8')
for v in [k for k in raw if 'benign' in k]:
    chk(f'{v} BP4', tab.loc[tab['id'] == v, 'acmg'].iloc[0] == 'BP4')
chk('GLA_c.639+919G>A = 0.30 PP3_supporting', tab.loc[tab['id'] == 'GLA_c.639+919G>A', 'acmg'].iloc[0] == 'PP3_supporting')
chk('one summary row per variant (10)', len(tab) == 10 and tab['delta_max'].notna().all())
# boundary regression (the pre-fix defect): 0.10/0.20/0.50/0.80
b = classify_delta([0.0, 0.10, 0.11, 0.19, 0.20, 0.49, 0.50, 0.79, 0.80, 1.0, np.nan, 0.199999999, 0.2000001])
print(list(b))
exp = ['BP4', 'BP4', 'inconclusive', 'inconclusive', 'PP3_supporting', 'PP3_supporting', 'PP3_supporting_prec0.5',
       'PP3_supporting_prec0.5', 'PP3_supporting_prec0.8', 'PP3_supporting_prec0.8', 'not_scored', 'PP3_supporting', 'PP3_supporting']
chk('boundary labels inclusive + NaN -> not_scored', list(b) == exp)
print('unscored_report (all scored):', unscored_report('data/panel_grch37.vcf', s['key'], 'SpliceAI'))
print('FAILS:', fails)
