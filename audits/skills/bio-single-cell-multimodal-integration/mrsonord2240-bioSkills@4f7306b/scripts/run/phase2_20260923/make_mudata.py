"""Independent synthetic CITE-seq MuData generator for the re-audit.
Different seed/shape from the original auditor's input2_totalvi.py (rng seed 0, 300x200x15)
so this exercises fresh ground, not just a rerun of the same numbers.
"""
import numpy as np
import anndata as ad
import mudata as md

rng = np.random.default_rng(777)
n_cells, n_genes, n_prot = 240, 150, 12
rna_counts = rng.poisson(3.0, size=(n_cells, n_genes)).astype("float32")
prot_counts = rng.poisson(25.0, size=(n_cells, n_prot)).astype("float32")

rna = ad.AnnData(rna_counts)
rna.layers["counts"] = rna_counts
prot = ad.AnnData(prot_counts)
prot.layers["counts"] = prot_counts

mdata = md.MuData({"rna": rna, "prot": prot})
mdata.obs_names = [f"cell{i}" for i in range(n_cells)]
for m in mdata.mod.values():
    m.obs_names = mdata.obs_names

mdata.write_h5mu("reaudit_cite_seq.h5mu")
print("wrote reaudit_cite_seq.h5mu", mdata)
