"""Fresh synthetic multiome fixture with planted RNA and ATAC perturbation effects."""
from pathlib import Path
import numpy as np
import anndata as ad
import muon as mu

OUT = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data\multiome_fixture.h5mu")
rng = np.random.default_rng(9232026)
n_ko, n_ntc, genes, peaks = 100, 100, 40, 45
n = n_ko + n_ntc
labels = np.array(["GENE_A KO"] * n_ko + ["NTC"] * n_ntc)
rna_x = rng.poisson(3, size=(n, genes)).astype(np.int32)
atac_x = rng.poisson(2, size=(n, peaks)).astype(np.int32)
rna_x[:n_ko, :5] += rng.poisson(7, size=(n_ko, 5))
atac_x[:n_ko, :5] += rng.poisson(6, size=(n_ko, 5))
obs = {"mixscape_class": labels}
rna = ad.AnnData(rna_x, obs=obs)
rna.var_names = [f"gene_{i}" for i in range(genes)]
atac = ad.AnnData(atac_x, obs=obs)
atac.var_names = [f"peak_{i}" for i in range(peaks)]
rna.obs_names = [f"cell_{i}" for i in range(n)]
atac.obs_names = rna.obs_names.copy()
mdata = mu.MuData({"rna": rna, "atac": atac})
mdata.write_h5mu(OUT)
print(f"wrote={OUT}")
print("planted_rna=gene_0,gene_1,gene_2,gene_3,gene_4")
print("planted_atac=peak_0,peak_1,peak_2,peak_3,peak_4")
