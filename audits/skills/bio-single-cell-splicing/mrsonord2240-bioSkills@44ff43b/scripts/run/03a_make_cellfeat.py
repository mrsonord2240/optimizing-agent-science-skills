"""Build cell-feature tables for brie-quant on REAL cells: (a) random binary label (null), (b) log spliced-read depth (a real covariate)."""
import numpy as np, pandas as pd, anndata as ad
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a=ad.read_h5ad(f'{R}/out/real_counts/brie_count.h5ad')
rng=np.random.default_rng(1)
tot=np.asarray(a.layers['isoform1'].sum(1)).ravel()+np.asarray(a.layers['isoform2'].sum(1)).ravel()
df=pd.DataFrame({'cell':a.obs_names,'rand_group':rng.integers(0,2,a.n_obs),'log_depth':np.log1p(tot)}).set_index('cell')
df['log_depth']=(df.log_depth-df.log_depth.mean())/df.log_depth.std()
df.to_csv(f'{R}/out/real_cellfeat.tsv',sep='\t')
print(df.head(), df.shape)
