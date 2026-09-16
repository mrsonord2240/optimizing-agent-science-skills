"""Input 5 (Stress) - bio-single-cell-batch-integration
The Skill's own prescription at SKILL.md:41 and :162 - "run 2-3 candidates and score them",
"Run candidates through scib-metrics (Benchmarker)". Done for real across four embeddings,
with the Skill's 0.6 bio / 0.4 batch composite computed explicitly.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, adjusted_rand_score

R = r'F:/OpenScience/audits/bio-single-cell-batch-integration/run'
a = sc.read_h5ad(R + '/input1_harmony.h5ad')
b = sc.read_h5ad(R + '/input2_scvi.h5ad')
# scVI object was subset to a different HVG set; align cells and copy the embedding over
a.obsm['X_scVI'] = b[a.obs_names].obsm['X_scVI']
a.obsm['X_scANVI'] = b[a.obs_names].obsm['X_scANVI']
print('embeddings scored:', [k for k in a.obsm])

try:
    from scib_metrics.benchmark import Benchmarker
    bm = Benchmarker(a, batch_key='batch', label_key='cell_type',
                     embedding_obsm_keys=['X_pca', 'X_pca_harmony', 'X_scVI', 'X_scANVI'],
                     n_jobs=1)
    bm.benchmark()
    res = bm.get_results(min_max_scale=False)
    print('\nscib-metrics Benchmarker results (raw, not min-max scaled):')
    print(res.round(4).to_string())
    ok = True
except Exception as e:
    print('scib-metrics Benchmarker FAILED:', type(e).__name__, str(e)[:300])
    ok = False

# --- the Skill's composite, computed by hand so the weighting is visible ---
if ok:
    num = res.drop(index=[i for i in res.index if i == 'Metric Type'])
    num = num.apply(pd.to_numeric, errors='coerce')
    print('\nSKILL.md:41 composite = 0.6 x Bio conservation + 0.4 x Batch correction:')
    for m in num.index:
        bio = num.loc[m].get('Bio conservation', np.nan)
        bat = num.loc[m].get('Batch correction', np.nan)
        if not np.isnan(bio) and not np.isnan(bat):
            print(f'  {m:16s} bio {bio:.4f}  batch {bat:.4f}  composite {0.6*bio + 0.4*bat:.4f}')

# --- the gaming demonstration the Skill warns about ---
print('\nSKILL.md:162 "batch-mixing metrics are trivially maximized by over-correction".')
rng = np.random.default_rng(20260916)
a.obsm['X_destroyed'] = rng.normal(size=a.obsm['X_pca'].shape)   # all structure removed
ct, bt = a.obs['cell_type'].values, a.obs['batch'].values
for rep in ['X_pca', 'X_pca_harmony', 'X_scANVI', 'X_destroyed']:
    print(f'  {rep:16s} batch ASW {silhouette_score(a.obsm[rep], bt, random_state=0):+.4f} | '
          f'cell-type ASW {silhouette_score(a.obsm[rep], ct, random_state=0):+.4f}')
print('  -> pure noise has the best batch ASW of all four. A batch metric alone selects it.')
print('DONE')
