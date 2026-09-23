"""Phase 2 input 5: documented pseudobulk and Milo design on real Perturb-seq data."""
from pathlib import Path
import mudata as md
import pertpy as pt
import scanpy as sc

data = Path(r"F:/OpenScience/audits/bio-single-cell-perturb-seq/run/data/papalexi_2021.h5mu")
mdata = md.read_h5mu(data, backed=None)
mdata.push_obs(columns=["gene_target", "replicate"], mods=["rna"])
adata = mdata.mod["rna"]
adata.layers["counts"] = adata.X.copy()
pb = pt.tl.PseudobulkSpace().compute(adata, target_col="gene_target", groups_col="replicate", layer_key="counts", mode="sum")
assert pb.n_obs > 10 and pb.X.sum() > 0
target = "STAT1"
sub = adata[adata.obs["gene_target"].isin([target, "NT"])].copy()
sc.pp.normalize_total(sub, target_sum=1e4); sc.pp.log1p(sub); sc.pp.pca(sub, n_comps=30); sc.pp.neighbors(sub, n_pcs=30)
milo = pt.tl.Milo(); mm = milo.load(sub); milo.make_nhoods(mm["rna"], prop=0.1, seed=23)
mm["rna"].obs["replicate_target"] = mm["rna"].obs["replicate"].astype(str) + "_" + mm["rna"].obs["gene_target"].astype(str)
milo.count_nhoods(mm, sample_col="replicate_target")
milo.da_nhoods(mm, design="~ gene_target", solver="pydeseq2")
assert "SpatialFDR" in mm["milo"].var
print(f"PASS pseudobulk={pb.shape}; Milo neighborhoods={mm['milo'].n_vars}")
