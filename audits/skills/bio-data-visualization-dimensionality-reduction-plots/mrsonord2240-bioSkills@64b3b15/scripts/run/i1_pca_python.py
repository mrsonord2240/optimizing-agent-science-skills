"""Input 1 (Canonical): SKILL.md Python PCA block on synthetic bulk data; assert axis-label percentages vs independent numpy SVD."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, re, os
from common import *
counts, meta = make_bulk()
X = np.log2(counts.values + 1)                      # samples x genes (log-normalised)
# ---- independent ground truth: centred SVD
Xc = X - X.mean(0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
truth = S**2 / np.sum(S**2)
# ---- SKILL.md block, verbatim except `X`, `labels` supplied
from sklearn.decomposition import PCA
labels = pd.Categorical(meta['condition']).codes    # SKILL block uses c=labels: needs numeric
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X)
var = pca.explained_variance_ratio_
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sc_ = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels, alpha=0.7)
axes[0].set_xlabel(f'PC1 ({var[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({var[1]*100:.1f}%)')
axes[1].plot(range(1, 11), var, 'o-')
axes[1].set_xlabel('PC')
axes[1].set_ylabel('Variance explained')
fig.savefig(os.path.join(FIGS,'i1_pca_skillblock.png'), dpi=100)
# ---- assertions on CONTENT
xl = axes[0].get_xlabel(); yl = axes[0].get_ylabel()
p1 = float(re.search(r'\(([\d.]+)%\)', xl).group(1)); p2 = float(re.search(r'\(([\d.]+)%\)', yl).group(1))
print('label PC1/PC2 =', p1, p2, '| SVD truth =', round(truth[0]*100,1), round(truth[1]*100,1))
assert p1 == round(truth[0]*100,1) and p2 == round(truth[1]*100,1)
print('solver', pca._fit_svd_solver, 'max abs diff ratio', np.abs(var-truth[:10]).max()); assert np.allclose(var, truth[:10], atol=1e-3)
print('A1 PASS: variance labels equal independent SVD; first 10 ratios allclose')
# sign/centering: PC scores have mean 0; sklearn centres but does not scale
print('score means ~0:', np.allclose(X_pca.mean(0), 0, atol=1e-8), '; PC1 var sample-cov =', X_pca[:,0].var(ddof=1), 'explained_variance_[0] =', pca.explained_variance_[0])
# colour mapping: facecolors match cmap(norm(code))
fc = sc_.get_facecolor()[:, :3]
cm = plt.get_cmap(); exp = cm(sc_.norm(labels))[:, :3]
print('A2 colour-by-group mapping correct:', np.allclose(fc, exp, atol=1e-6))
# group separation on PCs: what PC drives condition vs batch (planted)
def r2(v, g): 
    g = pd.Series(g); return 1 - sum(((v[g==k]-v[g==k].mean())**2).sum() for k in g.unique())/((v-v.mean())**2).sum()
for i in range(4):
    print(f'PC{i+1} R2 condition={r2(X_pca[:,i], meta.condition.values):.2f} batch={r2(X_pca[:,i], meta.batch.values):.2f} corr(libfactor)={np.corrcoef(X_pca[:,i], meta.libfactor)[0,1]:+.2f}')
# ---- Skill block with STRING labels (what a researcher has in a metadata column)
try:
    fig2, ax = plt.subplots(); ax.scatter(X_pca[:,0], X_pca[:,1], c=meta['condition'].values); fig2.savefig(os.path.join(FIGS,'i1_strlabels.png'))
    print('string labels: scatter accepted')
except Exception as e:
    print('string labels c=labels FAILS:', type(e).__name__, str(e)[:120])
# ---- Skill claim: PCA without scaling -> library size dominates (raw counts, no log)
pr = PCA(n_components=3).fit(counts.values)
sc1 = pr.transform(counts.values)
print('RAW counts PC1 corr with libfactor: %+.2f ; PC1 var %.1f%%' % (np.corrcoef(sc1[:,0], meta.libfactor)[0,1], pr.explained_variance_ratio_[0]*100))
Xs = (X - X.mean(0)) / X.std(0)
ps = PCA(n_components=3).fit(Xs); ss = ps.transform(Xs)
print('log+scale PC1 corr with libfactor: %+.2f ; PC1 var %.1f%%' % (np.corrcoef(ss[:,0], meta.libfactor)[0,1], ps.explained_variance_ratio_[0]*100))
counts.to_csv(os.path.join(DATA,'bulk_counts.csv')); meta.to_csv(os.path.join(DATA,'bulk_meta.csv'))
# ---- does the Skill's stated fix ("vst()/rlog() or log + scale") remove the library-size PC? test size-factor normalisation too
cpm = counts.values / counts.values.sum(1, keepdims=True) * 1e6
Xn = np.log2(cpm + 1); Xns = (Xn - Xn.mean(0)) / Xn.std(0)
pn = PCA(n_components=4).fit(Xns); sn = pn.transform(Xns)
for i in range(3):
    print(f'CPM+log+scale PC{i+1}: corr(lib)={np.corrcoef(sn[:,i], meta.libfactor)[0,1]:+.2f} R2cond={r2(sn[:,i], meta.condition.values):.2f} R2batch={r2(sn[:,i], meta.batch.values):.2f}')
