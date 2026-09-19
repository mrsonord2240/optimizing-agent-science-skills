"""
Input 5 (Stress / multi-part): "I have replicate labels per perturbation. Run pseudobulk DE with
DESeq2 for the within-state program change, and also check with Milo whether the DE I'm seeing is
actually just a compositional shift (perturbation moves cells across states) rather than a real
within-state expression change. Report both."

Follows SKILL.md's "Pseudobulk DE (Within-State Change)" and "Compositional vs Expression" sections.
Uses the same real papalexi_2021 CROP-seq dataset; 'replicate' column already exists in the dataset.
"""
import numpy as np
import pandas as pd
import scanpy as sc
import pertpy as pt

mdata = pt.dt.papalexi_2021()
adata = mdata.mod['rna']
for col in ('perturbation', 'gene_target', 'NT', 'replicate'):
    adata.obs[col] = mdata.obs[col].to_numpy()
print("replicate value_counts:")
print(adata.obs['replicate'].value_counts())
print("gene_target x replicate crosstab (subset):")
print(pd.crosstab(adata.obs['gene_target'], adata.obs['replicate']).iloc[:6])

# Stash raw counts BEFORE any log1p, per SKILL.md's explicit warning
adata.layers['counts'] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)

# --- Pseudobulk DE (SKILL.md "Pseudobulk DE (Within-State Change)") ---
pb = pt.tl.PseudobulkSpace()
pdata = pb.compute(adata, target_col='gene_target', groups_col='replicate', layer_key='counts', mode='sum')
print("\npseudobulk shape:", pdata.shape)
print("pseudobulk obs columns:", list(pdata.obs.columns))
print(pdata.obs.head())

# --- Milo differential abundance (SKILL.md "Compositional vs Expression") ---
milo = pt.tl.Milo()
mdata_milo = milo.load(adata)
milo.make_nhoods(mdata_milo['rna'], prop=0.1, seed=0)
milo.count_nhoods(mdata_milo, sample_col='replicate')
try:
    milo.da_nhoods(mdata_milo, design='~gene_target', solver='pydeseq2')
    print("\nmilo da_nhoods (pydeseq2 solver) succeeded")
    print(mdata_milo['milo'].var.head())
    print("n significant nhoods (SpatialFDR<0.1):",
          (mdata_milo['milo'].var['SpatialFDR'] < 0.1).sum(), "/", mdata_milo['milo'].var.shape[0])
except Exception as e:
    print("\nmilo da_nhoods FAILED:", repr(e))

print("\nDONE input5")
