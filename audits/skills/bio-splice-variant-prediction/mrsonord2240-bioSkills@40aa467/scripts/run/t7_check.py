"""NEW inputs (CFTR/BRCA1, GRCh38): concordance of SpliceAI + Pangolin + MMSplice via the Skill's build_concordance, plus CI-SpliceAI/Pangolin mask comparison."""
import sys, re
sys.path.insert(0, 'skill/examples')
import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
from splice_parsers import build_concordance, parse_pangolin_vcf, parse_spliceai_vcf, read_input_vcf
inp = 'data/panel_new_grch38.vcf'
T = build_concordance(inp, spliceai_vcf='ex_new/new_D50.vcf', pangolin_vcf='out/pang_new_mFalse.vcf', mmsplice_csv='out/mmsplice_new.csv')
ids = {}
for l in open(inp):
    if l.startswith('#'): continue
    c = l.split('\t'); ids[f'{c[0][3:]}:{c[1]}:{c[3]}>{c[4]}'] = c[2]
T['id'] = [ids[k] for k in T.index]
pm = parse_pangolin_vcf('out/pang_new_mTrue.vcf').groupby('key')['pangolin_score'].apply(lambda s: s.iloc[s.abs().argmax()])
T['pang_maskTrue'] = pm
# CI-SpliceAI (parse by replacing tag, as the Skill says)
ci = {}
for l in open('out/ci_new.vcf'):
    if l.startswith('#'): continue
    c = l.split('\t'); p = re.search(r'CISpliceAI=([^;\t]+)', c[7]).group(1).split('|')
    ci[f'{c[0][3:]}:{c[1]}:{c[3]}>{c[4]}'] = max(float(x) for x in p[2:6])
T['ci_delta'] = pd.Series(ci)
s500 = parse_spliceai_vcf('out/sai_new_D500.vcf').groupby('key')['delta_max'].max(); T['sai_D500'] = s500
print(T.set_index('id')[['spliceai_delta', 'sai_D500', 'pangolin_score', 'pang_maskTrue', 'delta_logit_psi', 'ci_delta', 'n_scored', 'n_above', 'concordance', 'spliceai_label']].round(2).to_string())
fails = []
def chk(n, c):
    print(('PASS ' if c else 'FAIL ') + n)
    if not c: fails.append(n)
Ti = T.set_index('id')
chk('12 input variants -> 12 rows (none dropped)', len(T) == 12)
for v in ['CFTR_c.1585-1G>A_acceptor', 'CFTR_c.1393-1G>A_acceptor', 'BRCA1_c.594-2A>C_acceptor', 'BRCA1_c.5074+1G>A_donor']:
    chk(f'{v}: SpliceAI >= 0.5 and concordance all/majority', Ti.loc[v, 'spliceai_delta'] >= 0.5 and Ti.loc[v, 'concordance'] in ('all_predict_disruption', 'majority_predict_disruption'))
for v in ['CFTR_c.3718-15A>T_LB', 'CFTR_c.4242+9T>C_LB', 'CFTR_c.4137-18A>G_LB', 'BRCA1_c.5332+84G>A_LB', 'BRCA1_c.594-4A>T_LB']:
    chk(f'{v}: BP4 and none_predict_disruption', Ti.loc[v, 'spliceai_label'] == 'BP4' and Ti.loc[v, 'concordance'] == 'none_predict_disruption')
chk('BRCA1 c.212+3A>G (non-canonical +3): SpliceAI >= 0.5', Ti.loc['BRCA1_c.212+3A>G_donor+3', 'spliceai_delta'] >= 0.5)
print('CFTR pseudoexon:', dict(Ti.loc['CFTR_c.3717+12191C>T_3849+10kb_pseudoexon'][['spliceai_delta', 'sai_D500', 'pangolin_score', 'delta_logit_psi', 'ci_delta', 'concordance']]))
print('CFTR c.2909-10T>G (ClinVar likely benign):', dict(Ti.loc['CFTR_c.2909-10T>G_LB'][['spliceai_delta', 'pangolin_score', 'delta_logit_psi', 'ci_delta', 'concordance']]))
print('FAILS', fails)
