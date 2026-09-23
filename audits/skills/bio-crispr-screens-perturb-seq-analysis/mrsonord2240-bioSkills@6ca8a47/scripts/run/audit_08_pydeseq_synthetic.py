"""Fresh current-pertpy contrast API check on planted pseudobulk counts."""
import numpy as np
import anndata as ad
import pertpy as pt

rng = np.random.default_rng(2026092308)
n_per_group, n_genes = 6, 80
labels = np.array(["NT"] * n_per_group + ["GENE_X"] * n_per_group)
base = rng.poisson(40, size=(2 * n_per_group, n_genes)).astype(np.int64)
base[n_per_group:, :8] += rng.poisson(90, size=(n_per_group, 8))
adata = ad.AnnData(base)
adata.obs["gene_target"] = labels
adata.var_names = [f"g{i}" for i in range(n_genes)]
de = pt.tl.PyDESeq2(adata, design="~gene_target")
de.fit()
res = de.test_contrasts(de.contrast("gene_target", "NT", "GENE_X"))
required = {"log_fc", "p_value", "adj_p_value"}
assert required.issubset(res.columns), sorted(res.columns)
name_col = next((c for c in ("variable", "gene", "index", "_index", "names") if c in res.columns), None)
assert name_col is not None, list(res.columns)
called = set(res.loc[res["adj_p_value"] < 0.01, name_col])
planted = {f"g{i}" for i in range(8)}
assert planted <= called, (planted - called)
assert not (called - planted), (called - planted)
print(f"columns={','.join(sorted(required))}")
print(f"gene_name_column={name_col}")
print(f"planted_recovered={len(planted & called)}/{len(planted)}")
print(f"null_false_positives={len(called - planted)}")
