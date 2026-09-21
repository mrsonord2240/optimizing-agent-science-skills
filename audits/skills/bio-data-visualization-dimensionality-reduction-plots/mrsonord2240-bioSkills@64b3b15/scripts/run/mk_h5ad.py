import numpy as np, pandas as pd, anndata as ad, os
from common import *
counts, obs, genes = make_sc(seed=4, n_cells=1200, n_genes=3000, n_clusters=5, batch_shift=0.0)
obs['condition'] = np.where(np.random.default_rng(0).random(len(obs))<0.5, 'ctrl', 'stim')
a = ad.AnnData(counts, obs=obs, var=pd.DataFrame(index=genes)); a.write_h5ad(os.path.join(AUD,'run','ex','processed.h5ad')); print(a)
