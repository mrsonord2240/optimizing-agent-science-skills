"""Input 5: build_concordance() (the Skill's SKILL.md block) on the auditor's own real outputs, both builds; assertions against
ground truth (canonical = pathogenic in ClinVar/literature, benign = ClinVar benign) and against independent per-tool tables."""
import sys
sys.path.insert(0, 'skill/examples')
import pandas as pd, numpy as np
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
from splice_parsers import build_concordance
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)
def by_id(T, inp):
    ids = {}
    for l in open(inp):
        if l.startswith('#'): continue
        c = l.split('\t'); ids[f'{c[0].replace("chr","")}:{c[1]}:{c[3]}>{c[4]}'] = c[2]
    T = T.copy(); T['id'] = [ids.get(k, '?') for k in T.index]; return T.set_index('id')
runs = {
 'GRCh37 chrX': dict(input_vcf='data/panel_grch37.vcf', spliceai_vcf='out/sai_D50_M0.vcf', pangolin_vcf='out/pang37_mF.vcf', mmsplice_csv='out/mmsplice_grch37.csv'),
 'GRCh38 panel': dict(input_vcf='data/panel_grch38_auditor.vcf', spliceai_vcf='out/sai38_D50.vcf', pangolin_vcf='out/pang38_canon_mFalse.vcf', mmsplice_csv='out/mmsplice_grch38.csv'),
}
for name, kw in runs.items():
    T = build_concordance(**kw)
    Ti = by_id(T, kw['input_vcf'])
    print(f'==== {name}\n', Ti[['spliceai_delta', 'pangolin_score', 'delta_logit_psi', 'n_scored', 'n_above', 'concordance', 'spliceai_label']].round(2).to_string())
    n_in = sum(1 for l in open(kw['input_vcf']) if not l.startswith('#'))
    chk(f'{name}: one row per input variant ({n_in}), none dropped by an inner merge', len(T) == n_in)
    can = [i for i in Ti.index if any(t in i for t in ['c.9563', 'c.31+1', 'c.370-1', 'donor_G>A', 'c.386', 'TP53'])]
    chk(f'{name}: canonical/donor/acceptor variants -> all_predict_disruption', all(Ti.loc[i, 'concordance'] == 'all_predict_disruption' for i in can))
    ben = [i for i in Ti.index if 'benign' in i]
    chk(f'{name}: benign controls -> none_predict_disruption', all(Ti.loc[i, 'concordance'] == 'none_predict_disruption' for i in ben))
    g = Ti.loc['GLA_c.639+919G>A']
    print('   GLA c.639+919G>A:', dict(g[['spliceai_delta', 'pangolin_score', 'delta_logit_psi', 'n_scored', 'n_above', 'concordance']]))
    chk(f'{name}: GLA c.639+919G>A (pseudoexon) is NOT called benign/insufficient (flagged disruption by SpliceAI+Pangolin)',
        g['spliceai_delta'] >= 0.2 and abs(g['pangolin_score']) >= 0.2 and g['concordance'] in ('majority_predict_disruption', 'all_predict_disruption'))
    chk(f'{name}: n_scored counts only tools with a value', (Ti['n_scored'] == Ti[['spliceai_delta', 'pangolin_score', 'delta_logit_psi']].notna().sum(axis=1)).all())
    if name.startswith('GRCh38'):
        chk('GRCh38: GLA c.639+919G>A shows MMSplice NaN and n_scored == 2 (the Skill says so)', np.isnan(g['delta_logit_psi']) and g['n_scored'] == 2)
# skipped-record stress: wrong-REF record appended -> outer join keeps it
open('data/panel_37_plus_bad.vcf', 'w').write(open('data/panel_grch37.vcf').read() + 'X\t100654735\tGLA_wrongREF\tA\tG\t.\t.\t.\n')
T = build_concordance('data/panel_37_plus_bad.vcf', spliceai_vcf='out/sai_D50_M0.vcf', pangolin_vcf='out/pang37_mF.vcf', mmsplice_csv='out/mmsplice_grch37.csv')
bad = T.loc['X:100654735:A>G']
print(dict(bad))
chk('un-scored wrong-REF variant stays as a row with n_scored 0 -> insufficient_tools (not benign, not dropped)', bad['n_scored'] == 0 and bad['concordance'] == 'insufficient_tools')
print('FAILS:', fails)
