"""Synthetic data for the dimensionality-reduction-plots audit. ALL DATA HERE IS SYNTHETIC (seeded)."""
import numpy as np, pandas as pd, os
AUD = r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots"
DATA = os.path.join(AUD, "data"); FIGS = os.path.join(AUD, "figs")

def make_bulk(seed=1, n_per=10, n_genes=2000):
    """Bulk RNA-seq-like counts: 3 conditions x 2 batches (n_per samples per cell of the design).
    Planted: 200 condition-driven genes (log2FC ~ +-1.5 per condition), 300 batch genes (+-1.0), library-size factor 0.5-2x."""
    rng = np.random.default_rng(seed)
    cond = np.repeat(['ctrl','trtA','trtB'], 2*n_per)
    batch = np.tile(np.repeat(['b1','b2'], n_per), 3)
    n = len(cond)
    base = rng.gamma(2.0, 200.0, n_genes)  # mean expression per gene
    lfc = np.zeros((n, n_genes))
    cg = rng.choice(n_genes, 200, replace=False)
    for c, sgn in zip(['trtA','trtB'], [1.5,-1.5]):
        lfc[np.ix_(cond==c, cg)] = sgn * rng.choice([-1,1], 200)
    bg = rng.choice(n_genes, 300, replace=False)
    lfc[np.ix_(batch=='b2', bg)] += rng.choice([-1,1], 300) * 1.0
    lib = rng.uniform(0.5, 2.0, n)
    mu = base[None,:] * 2**lfc * lib[:,None]
    counts = rng.negative_binomial(5, 5/(5+mu)).astype(float)
    df = pd.DataFrame(counts, index=[f's{i:02d}' for i in range(n)], columns=[f'g{j}' for j in range(n_genes)])
    meta = pd.DataFrame({'condition': cond, 'batch': batch, 'libfactor': lib}, index=df.index)
    return df, meta

def make_sc(seed=2, n_cells=600, n_genes=1000, n_clusters=4, batch_shift=0.0, traj=False):
    """scRNA-like counts. Clusters: n_clusters planted groups each with 60 marker genes up (x4).
    batch_shift>0 adds a second-batch effect on 100 genes. traj=True: one continuous trajectory (pseudotime 0..1) instead of clusters."""
    rng = np.random.default_rng(seed)
    base = rng.gamma(0.5, 1.0, n_genes)
    batch = rng.integers(0, 2, n_cells)
    if traj:
        pt = np.sort(rng.uniform(0,1,n_cells)); lab = np.digitize(pt,[.33,.66])
        prog = np.zeros((n_cells,n_genes)); gi = rng.choice(n_genes,150,replace=False)
        for k,g in enumerate(gi): prog[:,g] = np.log2(3)*np.sin(np.pi*(pt*(1+ (k%3)*0.5)) + k)  # smooth gene programs
        lfc = prog
    else:
        lab = rng.integers(0, n_clusters, n_cells); pt=None
        lfc = np.zeros((n_cells,n_genes))
        for c in range(n_clusters):
            genes = np.arange(c*60, c*60+60)
            lfc[np.ix_(lab==c, genes)] = 2.0
    if batch_shift>0:
        bg = rng.choice(n_genes, 100, replace=False)
        lfc[np.ix_(batch==1, bg)] += batch_shift * rng.choice([-1,1],100)
    lib = rng.lognormal(0, 0.3, n_cells)
    mu = base[None,:]*2**lfc*lib[:,None]
    counts = rng.poisson(mu*2.0).astype(np.float32)
    obs = pd.DataFrame({'cluster_true': lab.astype(str), 'batch': batch.astype(str)}, index=[f'c{i}' for i in range(n_cells)])
    if pt is not None: obs['pseudotime']=pt
    return counts, obs, [f'g{j}' for j in range(n_genes)]
