# INPUT 5: the Skill's "Concordance Across Predictors" snippet (SKILL.md python block #3, verbatim in blocks_dump.txt) with REAL outputs of all 3 tools.
# Part A: literal snippet with the natural frames an agent has (SpliceAI parser output; Pangolin VCF; MMSplice CSV) -> record the failure.
# Part B: my own adaptor (NOT part of the Skill) so the Skill's thresholds/interpretation map can be checked against ground truth.
import sys, re, traceback
sys.dont_write_bytecode = True
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
import importlib.util
spec = importlib.util.spec_from_file_location('ex', 'skill/examples/spliceai_clingen_classify.py'); ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
truth = {'PLCXD1_donor_G>A': 'path', 'PLCXD1_donor_GTdel': 'path', 'DMD_c.31+1G>A': 'path', 'DMD_c.9563+1G>A': 'path', 'GLA_c.370-1G>A': 'path',
         'GLA_c.639+919G>A': 'path', 'OTC_c.386+5G>A': 'lit-path', 'GLA_rs2071228_benign': 'benign', 'GLA_rs782094147_benign': 'benign', 'GLA_rs151195362_benign': 'benign'}
sai = ex.parse_spliceai_vcf('out/sai_D50_M1.vcf')          # SKILL: -M 1 "cleaner for clinical use"
def parse_pang(path):
    rows = []
    for l in open(path):
        if l.startswith('#'): continue
        f = l.rstrip('\n').split('\t'); m = re.search(r'Pangolin=([^;\t]+)', f[7])
        if not m: continue
        for g in m.group(1).split(','):
            p = g.split('|'); vals = [x for x in p[1:] if x != 'Warnings:' and ':' in x]
            sc = [float(v.split(':')[1]) for v in vals]
            rows.append({'chrom': f[0], 'pos': int(f[1]), 'alt': f[4].split(',')[0], 'id': f[2], 'gene_id': p[0], 'pangolin_score': max(sc, key=abs) if sc else 0.0})
    return pd.DataFrame(rows)
pang = parse_pang('out/pang_d50_mT.vcf')                    # SKILL: -m True
mm = pd.read_csv('out/mmsplice_plain.csv')
print('columns: spliceai', list(sai.columns)); print('columns: pangolin', list(pang.columns)); print('columns: mmsplice', list(mm.columns))
print('\n=== PART A: Skill snippet, literal ===')
try:
    merged = (sai.merge(pang, on=['chrom', 'pos', 'alt'], suffixes=('_sai', '_pang')).merge(mm, on=['chrom', 'pos', 'alt']))
    print('unexpected success', merged.shape)
except Exception as e:
    print('FAILED as expected:', type(e).__name__, str(e)[:120])
try:
    m2 = sai.merge(pang, on=['chrom', 'pos', 'alt'], suffixes=('_sai', '_pang')); print('sai+pangolin merge rows:', len(m2), 'has delta_max_sai col:', 'delta_max_sai' in m2.columns)
    m2['x'] = (m2['delta_max_sai'] >= 0.2)
except Exception as e:
    print('FAILED (delta_max_sai):', type(e).__name__, str(e)[:120])
print('Pangolin multi-gene rows (row inflation on the 2-key merge):', len(sai), 'sai rows for', sai[['chrom', 'pos']].drop_duplicates().shape[0], 'variants;', len(pang), 'pangolin rows')

print('\n=== PART B: adaptor (mine) + the Skill thresholds ===')
idmap = {(c, p): n for c, p, n in [(l.split('\t')[0], int(l.split('\t')[1]), l.split('\t')[2]) for l in open('data/panel_grch37.vcf') if not l.startswith('#')]}
sai['name'] = [idmap[(c, p)] for c, p in zip(sai.chrom, sai.pos)]
s = sai.groupby('name').delta_max.max().rename('sai')
pang['name'] = [idmap[(c, p)] for c, p in zip(pang.chrom, pang.pos)]
p = pang.groupby('name').pangolin_score.agg(lambda x: x.loc[x.abs().idxmax()]).rename('pang')
mm['name'] = [idmap[(a.split(':')[0], int(a.split(':')[1]))] for a in mm.ID]
mmx = mm.groupby('name').delta_logit_psi.agg(lambda x: x.loc[x.abs().idxmax()]).rename('mmsplice_dlogit')
mmp = mm.groupby('name').pathogenicity.max().rename('mmsplice_pathogenicity')
T = pd.concat([s, p, mmx, mmp], axis=1)
print('variants with an MMSplice row:', mmx.notna().sum(), 'of', len(T), '| inner-merge would keep only', T.dropna().shape[0])
T['concordance'] = (T.sai >= 0.2).astype(int) + (T.pang.abs() >= 0.2).astype(int) + (T.mmsplice_dlogit.abs().fillna(0) >= 1.0).astype(int)
T['interpretation'] = T.concordance.map({0: 'concordant_benign', 1: 'discordant_low_evidence', 2: 'concordant_evidence', 3: 'high_concordance_pathogenic'})
T['truth'] = pd.Series(truth)
print(T.round(2).to_string())
chk = []
def c(name, cond, detail=''): chk.append(bool(cond)); print('PASS' if cond else 'FAIL', name, detail)
c('all 3 benign controls concordance 0 (concordant_benign)', (T[T.truth == 'benign'].concordance == 0).all())
c('canonical +/-1,2 pathogenic (5 variants) concordance >=2', (T[T.index.isin(['PLCXD1_donor_G>A', 'PLCXD1_donor_GTdel', 'DMD_c.31+1G>A', 'DMD_c.9563+1G>A', 'GLA_c.370-1G>A'])].concordance >= 2).all())
c('deep-intronic pathogenic GLA c.639+919G>A concordance >=2 (Skill PP3 rule) with the Skill-recommended -m True / -M 1', T.loc['GLA_c.639+919G>A', 'concordance'] >= 2, 'concordance=%d -> %s' % (T.loc['GLA_c.639+919G>A', 'concordance'], T.loc['GLA_c.639+919G>A', 'interpretation']))
c('every input variant is present after the (inner) 3-way merge', T.dropna().shape[0] == len(T), '%d of %d survive' % (T.dropna().shape[0], len(T)))
print('\nSUMMARY %d/%d passed' % (sum(chk), len(chk)))
T.to_csv('out/t5_concordance.tsv', sep='\t')
