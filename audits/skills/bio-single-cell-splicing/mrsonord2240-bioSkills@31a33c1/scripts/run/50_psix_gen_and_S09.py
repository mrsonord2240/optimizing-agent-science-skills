"""INPUT 6a: Psix. SYNTHETIC trajectory data (auditor's own design), then SKILL.md block S09 run LITERALLY (exec) in the dir holding cells.h5ad, psi_matrix.tsv, mrna_matrix.tsv.
 240 cells along pseudotime t; 100 exons: 15 sigmoid-dynamic, 10 bump-dynamic (PSI rises then falls), 75 static; mRNA ~ NB(mean 5) (sparser than a pre-fix set: mean 8), PSI = Binomial(mrna, true)/mrna, NaN where mrna==0.
 X_pca = 20 dims: dim0 = t (+noise), dim1 = second gradient, dims 2-19 pure noise.
Run in WSL as-sc:  asenv as-sc python 50_psix_gen_and_S09.py"""
import numpy as np, pandas as pd, anndata as ad, os, sys, time
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'; W = f'{R}/out/in6_psix'; os.makedirs(W, exist_ok=True); os.chdir(W)
rng = np.random.default_rng(58); NC, NE = 240, 100
t = np.sort(rng.uniform(0, 1, NC)); cells = [f'c{i:03d}' for i in range(NC)]
dyn = np.zeros(NE, bool); dyn[:25] = True
psi_true = np.zeros((NC, NE))
for e in range(NE):
    if e < 15: c = rng.uniform(.3, .7); k = rng.uniform(8, 14); s = rng.choice([-1, 1]); psi_true[:, e] = 1 / (1 + np.exp(-s * k * (t - c)))
    elif e < 25: c = rng.uniform(.35, .65); psi_true[:, e] = .1 + .8 * np.exp(-((t - c) ** 2) / (2 * .12 ** 2))
    else: psi_true[:, e] = rng.uniform(.15, .85)
mrna = rng.negative_binomial(1.2, 1.2 / (1.2 + 5), size=(NC, NE))
psi = np.where(mrna > 0, rng.binomial(mrna, psi_true) / np.maximum(mrna, 1), np.nan)
ev = [f'ev{e:03d}' for e in range(NE)]
pd.DataFrame(psi.T, index=ev, columns=cells).rename_axis('event').to_csv('psi_matrix.tsv', sep='\t')
pd.DataFrame(mrna.T.astype(float), index=ev, columns=cells).rename_axis('event').to_csv('mrna_matrix.tsv', sep='\t')
pca = np.hstack([(t + rng.normal(0, .03, NC))[:, None], (np.sin(3 * t) + rng.normal(0, .1, NC))[:, None], rng.normal(0, .05, (NC, 18))])
a = ad.AnnData(np.zeros((NC, 5), dtype='float32'), obs=pd.DataFrame(index=cells)); a.obsm['X_pca'] = pca; a.write_h5ad('cells.h5ad')
print('NaN fraction in PSI', np.isnan(psi).mean().round(3), '; truth dynamic', int(dyn.sum()))
t0 = time.time()
exec(open(f'{R}/blocks/S09_python.py', encoding='utf-8').read())     # literal block: defaults n_random_exons=2000, n_neighbors=100, n_jobs=4
print('S09 wall time %.1f s' % (time.time() - t0))
r = psix_obj.psix_results; print('results columns', list(r.columns), 'rows', len(r)); print(r.sort_values('qvals').head(3).round(4))
isdyn = pd.Series(dyn, index=ev).reindex(r.index)
call = r.qvals < 0.05; print('regulated (qvals<0.05):', len(regulated), '; dynamic sigmoid+bump hit', int((call & isdyn).sum()), '/ 25 ; static false positives', int((call & ~isdyn).sum()), '/ 75 tested', int((~isdyn).sum()))
print('by kind: sigmoid', int((call[:0].sum() if False else call.reindex(ev[:15]).sum())), '/15 ; bump', int(call.reindex(ev[15:25]).sum()), '/10')
print('median psix_score dynamic %.2f static %.2f' % (r.psix_score[isdyn].median(), r.psix_score[~isdyn].median()))
# second method: naive smoothness check = |Spearman(PSI, t)| for monotone events, agrees on sigmoid ones
from scipy.stats import spearmanr
rho = pd.Series([abs(spearmanr(psi[~np.isnan(psi[:, e]), e], t[~np.isnan(psi[:, e])])[0]) for e in range(NE)], index=ev)
print('independent |Spearman(PSI,t)| mean: sigmoid', rho[:15].mean().round(2), ' bump', rho[15:25].mean().round(2), ' static', rho[25:].mean().round(2))
assert (call & isdyn).sum() >= 15
