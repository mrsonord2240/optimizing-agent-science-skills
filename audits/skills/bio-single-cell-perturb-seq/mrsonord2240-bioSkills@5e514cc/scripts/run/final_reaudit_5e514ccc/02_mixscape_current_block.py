"""Fresh Input 2: execute the current SKILL.md Mixscape block with its memory safeguard."""
from pathlib import Path

import mudata as md
import pertpy as pt
import scanpy as sc

data = Path(r"F:/OpenScience/audits/bio-single-cell-perturb-seq/run/data/papalexi_2021.h5mu")
mdata = md.read_h5mu(data, backed=None)
mdata.push_obs(columns=["perturbation", "gene_target", "replicate"], mods=["rna"])
base = mdata.mod["rna"]
adata = base[base.obs["gene_target"].isin(["STAT1", "NT"])].copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=1000)
sc.pp.pca(adata, n_comps=30)
adata.X = adata.X.toarray()
ms = pt.tl.Mixscape()
ms.perturbation_signature(
    adata, pert_key="perturbation", control="NT", n_neighbors=20, batch_size=1000
)
ms.mixscape(adata, pert_key="gene_target", control="NT", layer="X_pert")
counts = adata.obs["mixscape_class_global"].value_counts()
assert {"KO", "NP", "NT"}.issubset(set(counts.index))
print("PASS current Mixscape block KO/NP/NT:", counts.to_dict())
