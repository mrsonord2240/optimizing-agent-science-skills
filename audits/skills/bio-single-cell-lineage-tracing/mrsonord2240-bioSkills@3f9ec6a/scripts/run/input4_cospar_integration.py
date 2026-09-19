"""
Input 4 (Variant B): CoSpar clone+state integration, following SKILL.md
'Integrate Clones With State Using CoSpar', against the synthetic LARRY-style
lineage_traced.h5ad (deliberately constructed so Day2 state is indistinguishable
across clones, but clones differ in their Day4 fate -- ground truth fate bias
is known and printed by generate_data.py).
"""
import warnings
warnings.filterwarnings('ignore')
import cospar as cs
import scanpy as sc

adata = sc.read_h5ad('../data/lineage_traced.h5ad')
print('loaded', adata.shape, 'time_info values:', adata.obs['time_info'].unique().tolist())

sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

adata2 = cs.pp.initialize_adata_object(
    adata, X_clone=adata.obsm['X_clone'], time_info=adata.obs['time_info']
)
print('initialize_adata_object OK, adata2 keys:', list(adata2.obs.keys())[:10])

adata2 = cs.tmap.infer_Tmap_from_multitime_clones(
    adata2, smooth_array=[15, 10, 5], sparsity_threshold=0.1
)
print('infer_Tmap_from_multitime_clones OK, uns keys with "map" in name:',
      [k for k in adata2.uns.keys() if 'map' in k.lower()])

cs.tl.fate_bias(adata2, selected_fates=['Monocyte', 'Neutrophil'], source='transition_map')
print('fate_bias OK')
