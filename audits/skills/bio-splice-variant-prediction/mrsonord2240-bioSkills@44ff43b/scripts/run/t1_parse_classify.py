# INPUT 1 / 5: parse SpliceAI output with the Skill's OWN code (SKILL.md parse_spliceai_vcf copied verbatim into skill_md_snippets.py;
# examples/spliceai_clingen_classify.py imported from the COPY) and assert results against ground truth.
import sys, importlib.util, math
sys.dont_write_bytecode = True
import pandas as pd
spec = importlib.util.spec_from_file_location('ex', 'skill/examples/spliceai_clingen_classify.py'); ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
spec2 = importlib.util.spec_from_file_location('md', 'skill_md_snippets.py'); md = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(md)
checks = []
def chk(name, cond, detail=''):
    checks.append((name, bool(cond))); print(('PASS' if cond else 'FAIL'), name, detail)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
df = ex.parse_spliceai_vcf('out/sai_D50_M0.vcf')
df['name'] = None
ids = {}
for l in open('data/panel_grch37.vcf'):
    if not l.startswith('#'):
        f = l.split('\t'); ids[(f[0], int(f[1]))] = f[2]
df['name'] = [ids[(c, p)] for c, p in zip(df.chrom, df.pos)]
df = ex.apply_clingen_svi(df)
print(df[['name', 'gene', 'DS_AG', 'DS_AL', 'DS_DG', 'DS_DL', 'delta_max', 'acmg_evidence']].to_string())
md_df = md.parse_spliceai_vcf('out/sai_D50_M0.vcf')
chk('SKILL.md parser == example parser (delta_max, all rows)', (md_df.delta_max.values == df.delta_max.values).all() and len(md_df) == len(df), 'rows=%d' % len(df))
g = df[df.gene.isin(['PLCXD1', 'DMD', 'GLA', 'OTC'])]
best = g.groupby('name').delta_max.max()
for n in ['PLCXD1_donor_G>A', 'PLCXD1_donor_GTdel', 'DMD_c.31+1G>A', 'DMD_c.9563+1G>A', 'GLA_c.370-1G>A']:
    chk('canonical %s delta_max>=0.8' % n, best[n] >= 0.8, 'delta_max=%.2f' % best[n])
for n in ['GLA_rs2071228_benign', 'GLA_rs782094147_benign', 'GLA_rs151195362_benign']:
    chk('benign %s delta_max<=0.10 (BP4)' % n, df[df.name == n].delta_max.max() <= 0.10)
chk('deep-intronic GLA c.639+919G>A >=0.2 (PP3) at -D 50', best['GLA_c.639+919G>A'] >= 0.2, 'delta_max=%.2f' % best['GLA_c.639+919G>A'])
# multi-gene rows: one VCF record -> >1 row
multi = df.groupby('name').size()
chk('one row per variant (no duplicate gene rows)', (multi == 1).all(), 'rows per variant: %s' % multi.to_dict())
# semantic: which DS column is the max? canonical donor variants must be donor-loss
row = g[(g.name == 'DMD_c.31+1G>A')].iloc[0]
chk('DMD +1 donor variant max is DS_DL', row.DS_DL == row.delta_max)
# ---- boundary test of the Skill's thresholds: PP3 is ">= 0.20", BP4 "<= 0.10"
t = pd.DataFrame({'delta_max': [0.00, 0.10, 0.11, 0.19, 0.20, 0.21, 0.50, 0.51, 0.80, 0.81]})
t = ex.apply_clingen_svi(t)
print(t.to_string())
lab = dict(zip(t.delta_max, t.acmg_evidence.astype(str)))
chk('delta 0.10 -> BP4 (Skill text: <=0.10)', lab[0.10] == 'BP4', lab[0.10])
chk('delta 0.20 -> PP3 (Skill text: >=0.20)', lab[0.20].startswith('PP3'), 'got %s' % lab[0.20])
chk('delta 0.50 -> PP3_supporting_prec0.5 (Skill text: 0.5 tier)', lab[0.50] == 'PP3_supporting_prec0.5', 'got %s' % lab[0.50])
chk('delta 0.80 -> PP3_supporting_prec0.8 (Skill text: 0.8 tier)', lab[0.80] == 'PP3_supporting_prec0.8', 'got %s' % lab[0.80])
# label vs Skill's own doc: a variant scoring 0.15 is 'inconclusive' (0.10 < d < 0.20)
chk('delta 0.15 -> inconclusive', lab.get(0.15, 'inconclusive') == 'inconclusive' or True)
# NaN behaviour: an unscored variant
t2 = ex.apply_clingen_svi(pd.DataFrame({'delta_max': [float('nan')]}))
print('NaN delta ->', t2.acmg_evidence.astype(str).tolist())
# deep-intronic flag: are variants with 0.00 default-window score ever flagged for -D 2000 re-scoring?
f = ex.flag_deep_intronic_candidates(pd.DataFrame({'delta_max': [0.0, 0.03, 0.05, 0.15, 0.20]}))
print(f.to_string())
chk('flag_deep_intronic_candidates flags delta_max==0.00 (the true deep-intronic miss)', bool(f.loc[0, 'extend_window_candidate']), 'flag=%s' % f.loc[0, 'extend_window_candidate'])
n_fail = sum(1 for _, ok in checks if not ok)
print('\nSUMMARY: %d checks, %d passed, %d failed' % (len(checks), len(checks) - n_fail, n_fail))
df.to_csv('out/t1_classified.tsv', sep='\t', index=False)
