"""
Re-audit regression + independent extension of Input 5 (Stress / multi-part):
"I have replicate labels per perturbation. Run pseudobulk DE with DESeq2 for the within-state
program change, and also check with Milo whether the DE I'm seeing is actually just a
compositional shift rather than a real within-state expression change. Report both."

Follows the FIXED SKILL.md's "Pseudobulk DE" and "Compositional vs Expression" sections
verbatim (post fix/sc-perturb commit 420b60b). Runs on the same real papalexi_2021 dataset,
but tests the Milo replacement on TWO targets the fixer's own fix log does not mention
verifying (fixer verified STAT1 vs NT only) to check the fix generalizes, and adds an actual
pydeseq2 pseudobulk DE call (not shown as executable code in SKILL.md, only described in prose)
as an independent extension of the regression test.
"""
import numpy as np
import pandas as pd
import scanpy as sc
import pertpy as pt

mdata = pt.dt.papalexi_2021()
adata = mdata.mod['rna']
mdata.push_obs(columns=['perturbation', 'gene_target', 'replicate'], mods=['rna'])
print("gene_target value_counts:")
print(adata.obs['gene_target'].value_counts())

adata.layers['counts'] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.pca(adata, n_comps=50)

# --- Pseudobulk DE (SKILL.md "Pseudobulk DE (Within-State Change)"), extended with a real pydeseq2 call ---
pb = pt.tl.PseudobulkSpace()
pdata = pb.compute(adata, target_col='gene_target', groups_col='replicate', layer_key='counts', mode='sum')
print("\npseudobulk shape:", pdata.shape)
print(pdata.obs.head())

from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

target = 'ATF2'  # a different target than the fixer's STAT1 verification run
sub_targets = [target, 'NT']
mask = pdata.obs['gene_target'].isin(sub_targets)
counts_df = pd.DataFrame(pdata[mask].layers['counts'] if 'counts' in pdata.layers else pdata[mask].X,
                          index=pdata[mask].obs_names, columns=pdata.var_names)
counts_df = counts_df.round().astype(int)
meta = pdata[mask].obs[['gene_target']].copy()
dds = DeseqDataSet(counts=counts_df, metadata=meta, design='~gene_target')
dds.deseq2()
stats = DeseqStats(dds, contrast=['gene_target', target, 'NT'])
stats.summary()
res = stats.results_df
print(f"\npydeseq2 pseudobulk DE {target} vs NT: {(res['padj'] < 0.1).sum()}/{res.shape[0]} genes padj<0.1")

# --- Milo differential abundance (FIXED SKILL.md "Compositional vs Expression"), 2 targets ---
for target in ['STAT1', 'ATF2']:
    print(f"\n=== Milo DA: {target} vs NT ===")
    sub = adata[adata.obs['gene_target'].isin([target, 'NT'])].copy()
    sc.pp.neighbors(sub, n_pcs=50)

    milo = pt.tl.Milo()
    mdata_milo = milo.load(sub)
    milo.make_nhoods(mdata_milo['rna'], prop=0.1, seed=0)
    mdata_milo['rna'].obs['replicate_target'] = (
        mdata_milo['rna'].obs['replicate'].astype(str) + '_' + mdata_milo['rna'].obs['gene_target'].astype(str)
    )
    milo.count_nhoods(mdata_milo, sample_col='replicate_target')
    try:
        milo.da_nhoods(mdata_milo, design='~ gene_target', solver='pydeseq2')
        n_sig = (mdata_milo['milo'].var['SpatialFDR'] < 0.1).sum()
        n_total = mdata_milo['milo'].var.shape[0]
        print(f"da_nhoods SUCCEEDED: {n_sig}/{n_total} neighborhoods significant (SpatialFDR<0.1)")
    except Exception as e:
        print("da_nhoods FAILED:", repr(e))

print("\nDONE input5_fixed")
