"""Input 1 step E: call the shipped example module's helper functions (from the COPY in run/skill/examples) on REAL brie-quant output.
Labels are RANDOM (null) so any 'significant' event is a false positive."""
import sys, numpy as np, pandas as pd, scanpy as sc, traceback
sys.path.insert(0,'/mnt/openscience/audits/bio-single-cell-splicing/run/skill/examples')
import sc_splicing_brie2 as ex
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a = sc.read_h5ad(f'{R}/out/real_quant.h5ad')
cf = pd.read_csv(f'{R}/out/real_cellfeat.tsv', sep='\t', index_col=0)
a.obs['cell_type'] = cf.loc[a.obs_names,'rand_group'].map({0:'A',1:'B'}).values
print('X is', type(a.X), None if a.X is None else a.X.shape)
print('---find_variable_splicing (min_cells=50)')
try:
    v, m = ex.find_variable_splicing(a, 'cell_type', 50)
    print(v.head(3)); print('n events', len(v), 'mean_psi cols', list(m.columns))
except Exception as e:
    traceback.print_exc()
print('---pseudobulk_by_celltype (uses adata.X)')
try:
    pb = ex.pseudobulk_by_celltype(a, 'cell_type'); print(pb.shape); print(pb.head(3))
except Exception as e:
    print('FAILED:', type(e).__name__, e)
print('---differential_splicing_pseudobulk (null labels)')
try:
    g1 = (a.obs['cell_type']=='A').values; g2=(a.obs['cell_type']=='B').values
    d = ex.differential_splicing_pseudobulk(a, g1, g2)
    print(d[['event','delta_psi','pvalue','fdr']].head(5).to_string())
    print('n tested', len(d), 'n fdr<0.05 (null => should be 0):', int((d.fdr<0.05).sum()), 'n raw p<0.05:', int((d.pvalue<0.05).sum()))
except Exception as e:
    traceback.print_exc()
print('---read_h5ad via brie')
import brie
b = brie.read_h5ad(f'{R}/out/real_quant.h5ad'); print(type(b), b.shape)
