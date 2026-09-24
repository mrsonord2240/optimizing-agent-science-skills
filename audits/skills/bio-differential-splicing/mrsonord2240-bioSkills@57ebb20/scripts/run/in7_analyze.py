#!/usr/bin/env python3
"""INPUT 7 statistics. Runs the SKILL.md 'Confounder Handling' snippet VERBATIM (exec of the extracted fenced block) once per event on rMATS SE per-replicate PSI
of the batch-confounded SYNTHETIC design (sim2b), then BH across events.
Usage: in7_analyze.py <run dir>   (run dir contains data/sim2b, out/in7, skill/SKILL.md, extract logic inline)"""
import sys, re, os, json
import numpy as np, pandas as pd
import patsy
import statsmodels
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

run = sys.argv[1]
sim = f'{run}/data/sim2b'
out = f'{run}/out/in7'
print('statsmodels', statsmodels.__version__, 'patsy', patsy.__version__, 'pandas', pd.__version__)
txt = open(f'{run}/skill/SKILL.md', encoding='utf-8').read()
blocks = [(m.group(1), m.group(2)) for m in re.finditer(r'```(\w*)\n(.*?)```', txt, re.S)]
conf_block = [b for l, b in blocks if l == 'python' and 'patsy.dmatrix' in b][0]
truth = pd.read_csv(f'{sim}/truth.tsv', sep='\t', keep_default_na=False).set_index('gene')
meta_all = pd.read_csv(f'{sim}/meta.tsv', sep='\t').set_index('sample')
strong = set(truth.index[(truth['class'] == 'DS_strong') & (truth['etype'] == 'SE')])
alltrue = set(truth.index[truth['class'].str.startswith('DS') & (truth['etype'] == 'SE')])
bshift = set(truth.index[truth['class'] == 'null_batchshift'])
nullg = set(truth.index[truth['class'].isin(['null', 'null_overdisp', 'null_lowcov']) & (truth['etype'] == 'SE')])
print('SE genes: true DS %d (strong %d), batch-shift nulls %d, other nulls %d' % (len(alltrue), len(strong), len(bshift), len(nullg)))
minrep = lambda s: s.str.split(',').apply(lambda x: min(int(v) for v in x))


def load(design, samples1, samples2):
    d = pd.read_csv(f'{out}/rmats_{design}/out/SE.MATS.JC.txt', sep='\t')
    d['gene'] = d['GeneID'].str.strip('"')
    return d, samples1 + samples2


def run_design(design, s1, s2):
    d, samples = load(design, s1, s2)
    d = d[d['IncLevel1'].notna() & d['IncLevel2'].notna()].copy()
    d = d[~d['IncLevel1'].str.contains('NA') & ~d['IncLevel2'].str.contains('NA')]
    meta = meta_all.loc[samples, ['cond', 'batch', 'RIN']].rename(columns={'cond': 'group'}).copy()
    meta['batch'] = meta['batch'].astype(int)
    # rMATS (Skill filter)
    d['mi'] = minrep(d['IJC_SAMPLE_1']).combine(minrep(d['IJC_SAMPLE_2']), min)
    d['ms'] = minrep(d['SJC_SAMPLE_1']).combine(minrep(d['SJC_SAMPLE_2']), min)
    rm = d[(d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10) & ((d['mi'] + d['ms']) >= 10)]
    rmg = set(rm['gene'])
    print(f'\n### {design}: {len(samples)} samples, group/batch table:')
    print(pd.crosstab(meta['group'], meta['batch']).to_string())
    print(f'rMATS (Skill filter, no covariates): calls {len(rmg)} | true DS {len(rmg & alltrue)}/{len(alltrue)} | batch-shift nulls (false, batch-driven) {len(rmg & bshift)}/{len(bshift)} | other nulls {len(rmg & nullg)}')
    # PCA of the per-replicate PSI matrix (events with complete data)
    M = np.array([[float(x) for x in a.split(',')] + [float(x) for x in b.split(',')] for a, b in zip(d['IncLevel1'], d['IncLevel2'])])   # events x samples
    Xc = M - M.mean(axis=1, keepdims=True)
    u, sv, vt = np.linalg.svd(Xc, full_matrices=False)
    pc = vt[:3].T * sv[:3]
    for k in range(2):
        rg = np.corrcoef(pc[:, k], meta['group'].values)[0, 1]; rb = np.corrcoef(pc[:, k], meta['batch'].values)[0, 1]
        print(f'  PCA PC{k + 1} (var {sv[k] ** 2 / (sv ** 2).sum():.2f}): |r| with group {abs(rg):.2f}, |r| with batch {abs(rb):.2f}')
    # Skill snippet verbatim per event
    rows = []
    for i, (gene, a, b) in enumerate(zip(d['gene'], d['IncLevel1'], d['IncLevel2'])):
        vals = [float(x) for x in a.split(',')] + [float(x) for x in b.split(',')]
        psi = meta.copy()
        psi['psi'] = vals
        ns = {'np': np, 'pd': pd, 'patsy': patsy, 'smf': smf, 'multipletests': multipletests, 'meta': meta, 'psi': psi}
        exec(conf_block, ns)
        rows.append((gene, ns['p_group']))
    res = pd.DataFrame(rows, columns=['gene', 'p']).dropna()
    res['q'] = multipletests(res['p'], method='fdr_bh')[1]
    c_nom = set(res.loc[res['p'] < 0.05, 'gene']); c_bh = set(res.loc[res['q'] < 0.05, 'gene'])
    print(f'Skill snippet (logit_psi ~ group + C(batch) + RIN; group coef; {len(res)} events, residual df = {len(samples) - 4}):')
    print(f'   BH q<0.05: calls {len(c_bh)} | true DS {len(c_bh & alltrue)}/{len(alltrue)} | batch-shift nulls {len(c_bh & bshift)}/{len(bshift)} | other nulls {len(c_bh & nullg)}')
    print(f'   nominal p<0.05: calls {len(c_nom)} | true DS {len(c_nom & alltrue)}/{len(alltrue)} | batch-shift nulls {len(c_nom & bshift)}/{len(bshift)} | other nulls {len(c_nom & nullg)}')
    # direction of true DS calls: planted delta = cond1 - cond0
    # naive alternative: same model WITHOUT batch (what an unadjusted analysis does), for contrast
    rows2 = []
    for gene, a, b in zip(d['gene'], d['IncLevel1'], d['IncLevel2']):
        vals = [float(x) for x in a.split(',')] + [float(x) for x in b.split(',')]
        psi = meta.copy(); psi['psi'] = vals
        p = psi['psi'].clip(1e-3, 1 - 1e-3); psi['logit_psi'] = np.log(p / (1 - p))
        rows2.append((gene, smf.ols('logit_psi ~ group', data=psi).fit().pvalues['group']))
    r2 = pd.DataFrame(rows2, columns=['gene', 'p']).dropna(); r2['q'] = multipletests(r2['p'], method='fdr_bh')[1]
    c2 = set(r2.loc[r2['q'] < 0.05, 'gene'])
    print(f'Contrast, logit_psi ~ group only (no batch term), BH q<0.05: calls {len(c2)} | true DS {len(c2 & alltrue)}/{len(alltrue)} | batch-shift nulls {len(c2 & bshift)}/{len(bshift)}')
    return dict(design=design, rmats_calls=len(rmg), rmats_true=len(rmg & alltrue), rmats_batchfp=len(rmg & bshift), snippet_bh_calls=len(c_bh), snippet_bh_true=len(c_bh & alltrue),
                snippet_bh_batchfp=len(c_bh & bshift), snippet_bh_othernull=len(c_bh & nullg), snippet_nom_true=len(c_nom & alltrue), snippet_nom_batchfp=len(c_nom & bshift),
                nobatch_bh_calls=len(c2), nobatch_bh_true=len(c2 & alltrue), nobatch_bh_batchfp=len(c2 & bshift))


summ = [run_design('4v4', ['S1', 'S2', 'S3', 'S4'], ['S5', 'S6', 'S7', 'S8']), run_design('3v3', ['S1', 'S2', 'S4'], ['S5', 'S6', 'S8'])]
json.dump(summ, open(f'{out}/summary.json', 'w'), indent=1)

print('\n### aliasing check (Skill snippet verbatim) when batch == group (S1-4 in batch 1, S5-8 in batch 2)')
meta = meta_all.loc[['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'], ['cond', 'RIN']].rename(columns={'cond': 'group'}).copy()
meta['batch'] = [1, 1, 1, 1, 2, 2, 2, 2]
psi = meta.copy(); psi['psi'] = np.linspace(0.2, 0.8, 8)
try:
    exec(conf_block, {'np': np, 'pd': pd, 'patsy': patsy, 'smf': smf, 'multipletests': multipletests, 'meta': meta, 'psi': psi})
    print('NO ERROR: snippet did not refuse the aliased design')
    raise SystemExit(1)
except ValueError as e:
    print('ASSERT OK: ValueError raised:', e)
print('\n### aliasing check: batch perfectly nested only via a second covariate (batch2 = group xor 0) and a non-aliased design must pass')
meta['batch'] = [1, 2, 1, 2, 1, 2, 1, 2]
psi = meta.copy(); psi['psi'] = np.linspace(0.2, 0.8, 8)
ns = {'np': np, 'pd': pd, 'patsy': patsy, 'smf': smf, 'multipletests': multipletests, 'meta': meta, 'psi': psi}
exec(conf_block, ns)
print('ASSERT OK: balanced batch accepted, p_group = %.3f' % ns['p_group'])

print('\n### leafcutter results (from in7_run.sh)')
gene_of = lambda s: 'G%03d' % (int(s) // 3000)
for v in ('plain', 'batch', 'conf', 'confnum'):
    p = f'{out}/lc/ds_{v}_cluster_significance.txt'
    if not os.path.exists(p):
        print(v, 'no result file'); continue
    c = pd.read_csv(p, sep='\t'); e = pd.read_csv(f'{out}/lc/ds_{v}_effect_sizes.txt', sep='\t')
    e['clu'] = e['intron'].str.extract(r'(clu_\d+)')[0]; e['gene'] = [gene_of(x.split(':')[1]) for x in e['intron']]
    c['clu'] = c['cluster'].str.extract(r'(clu_\d+)')[0]; c['gene'] = c['clu'].map(e.groupby('clu')['gene'].first())
    ok = c[c['status'] == 'Success']; sg = set(ok.loc[ok['p.adjust'] < 0.05, 'gene'])
    print(f'leafcutter [{v}]: clusters tested {len(ok)}, called {len(sg)} | true DS (SE) {len(sg & alltrue)}/{len(alltrue)} | batch-shift nulls {len(sg & bshift)}/{len(bshift)} | other nulls {len(sg & nullg)}')
