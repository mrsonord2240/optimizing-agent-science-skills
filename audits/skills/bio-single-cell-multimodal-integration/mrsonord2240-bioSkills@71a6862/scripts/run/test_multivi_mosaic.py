"""Independent end-to-end run of the new SKILL.md 'Mosaic: MultiVI' block.
Different synthetic generation from the fixer's own verification (own RNG seed/shape/
cell-type signal), to check the recovery claim isn't an artifact of one dataset.
"""
import numpy as np
import anndata as ad
import mudata as md
import scvi

scvi.settings.seed = 0

rng = np.random.default_rng(31415)
n_genes, n_regions = 120, 80
n_types = 3
paired_per_type = 40   # 120 paired cells
rnaonly_per_type = 25  # 75 RNA-only cells
n_paired = paired_per_type * n_types
n_rnaonly = rnaonly_per_type * n_types
n_total = n_paired + n_rnaonly

# distinct marker gene/region blocks per cell type so structure is real and recoverable
gene_markers = {0: slice(0, 15), 1: slice(15, 30), 2: slice(30, 45)}
region_markers = {0: slice(0, 10), 1: slice(10, 20), 2: slice(20, 30)}

def make_block(n, ctype, has_atac):
    rna = rng.poisson(1.0, size=(n, n_genes)).astype("float32")
    rna[:, gene_markers[ctype]] += rng.poisson(12.0, size=(n, 15)).astype("float32")
    if has_atac:
        atac = rng.poisson(0.5, size=(n, n_regions)).astype("float32")
        atac[:, region_markers[ctype]] += rng.poisson(8.0, size=(n, 10)).astype("float32")
    else:
        atac = np.zeros((n, n_regions), dtype="float32")
    return rna, atac

rna_blocks, atac_blocks, labels, paired_flag = [], [], [], []
for ctype in range(n_types):
    r, a = make_block(paired_per_type, ctype, has_atac=True)
    rna_blocks.append(r); atac_blocks.append(a)
    labels += [ctype] * paired_per_type
    paired_flag += [True] * paired_per_type
for ctype in range(n_types):
    r, a = make_block(rnaonly_per_type, ctype, has_atac=False)
    rna_blocks.append(r); atac_blocks.append(a)
    labels += [ctype] * rnaonly_per_type
    paired_flag += [False] * rnaonly_per_type

rna_counts = np.vstack(rna_blocks)
atac_counts = np.vstack(atac_blocks)
labels = np.array(labels)
paired_flag = np.array(paired_flag)

rna = ad.AnnData(rna_counts)
rna.layers["counts"] = rna_counts
atac = ad.AnnData(atac_counts)
atac.layers["counts"] = atac_counts

obs_names = [f"cell{i}" for i in range(n_total)]
mdata = md.MuData({"rna": rna, "atac": atac})
mdata.obs_names = obs_names
for m in mdata.mod.values():
    m.obs_names = obs_names

# ---- verbatim SKILL.md 'Mosaic: MultiVI' block below ----
scvi.model.MULTIVI.setup_mudata(
    mdata, modalities={'rna_layer': 'rna', 'atac_layer': 'atac'}
)
model = scvi.model.MULTIVI(
    mdata, n_genes=mdata.mod['rna'].n_vars, n_regions=mdata.mod['atac'].n_vars
)
model.train()
mdata.obsm['X_multivi'] = model.get_latent_representation()
# ---- end verbatim block ----

latent = mdata.obsm['X_multivi']
print("latent shape:", latent.shape)

# Structure-recovery check, independent of the fixer's own metric: for each RNA-only
# cell, is its nearest PAIRED neighbor (by latent Euclidean distance) the SAME cell type
# more often than chance (1/3 baseline)?
from scipy.spatial.distance import cdist

paired_idx = np.where(paired_flag)[0]
rnaonly_idx = np.where(~paired_flag)[0]
dists = cdist(latent[rnaonly_idx], latent[paired_idx])
nearest_paired = paired_idx[np.argmin(dists, axis=1)]
nn_correct = (labels[nearest_paired] == labels[rnaonly_idx]).mean()
print(f"RNA-only cells whose NEAREST paired neighbor shares their true cell type: {nn_correct:.3f} (chance = {1/n_types:.3f})")

# same-type vs different-type mean distance (mirrors the fixer's own metric, independent data)
same_d, diff_d = [], []
for i, ridx in enumerate(rnaonly_idx):
    for j, pidx in enumerate(paired_idx):
        d = dists[i, j]
        if labels[ridx] == labels[pidx]:
            same_d.append(d)
        else:
            diff_d.append(d)
print(f"mean dist RNA-only -> same-type paired: {np.mean(same_d):.3f}")
print(f"mean dist RNA-only -> diff-type paired: {np.mean(diff_d):.3f}")
print("Status: COMPLETED")
