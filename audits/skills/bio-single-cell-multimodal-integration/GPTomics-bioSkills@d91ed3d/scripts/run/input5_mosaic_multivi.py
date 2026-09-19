# Input 5 (Stress / multi-part): "I have batch A with RNA+ATAC (multiome) and batch B with
# RNA only. Integrate them into one joint embedding using MultiVI."
# IMPORTANT: unlike WNN, totalVI, Multiome-WNN and GLUE, the SKILL.md and usage-guide.md
# provide ZERO code for MultiVI, StabMap or Cobolt -- the three methods named for exactly this
# mosaic anchor structure, one of the 4 structures the skill's own "Governing Principle"
# classifies tasks into. This script is NOT derived from the skill (there is nothing to derive
# from); it independently verifies whether the mosaic path is even feasible in this env, to
# inform the completeness finding below.
import numpy as np
import anndata as ad
import scvi

rng = np.random.default_rng(1)
n_genes, n_peaks = 100, 150

def make_rna(n):
    a = ad.AnnData(rng.poisson(2.0, size=(n, n_genes)).astype("float32"))
    a.var_names = [f"g{i}" for i in range(n_genes)]
    return a

def make_atac(n):
    a = ad.AnnData(rng.poisson(0.5, size=(n, n_peaks)).astype("float32"))
    a.var_names = [f"p{i}" for i in range(n_peaks)]
    return a

# batch A: paired multiome (RNA+ATAC same cells) -- combined feature space
n_a, n_b_rna, n_c_atac = 80, 60, 60
rna_a, atac_a = make_rna(n_a), make_atac(n_a)
multi = ad.concat([rna_a, atac_a], axis=1, merge="same")
multi.var_names = list(rna_a.var_names) + list(atac_a.var_names)
multi.obs_names = [f"batchA_{i}" for i in range(n_a)]

rna_only = make_rna(n_b_rna)
rna_only.obs_names = [f"batchB_{i}" for i in range(n_b_rna)]
atac_only = make_atac(n_c_atac)
atac_only.obs_names = [f"batchC_{i}" for i in range(n_c_atac)]

combined = scvi.data.organize_multiome_anndatas(multi, rna_anndata=rna_only, atac_anndata=atac_only)
print("Combined shape:", combined.shape, "modality counts:\n", combined.obs["modality"].value_counts())

scvi.model.MULTIVI.setup_anndata(combined, batch_key="modality")
model = scvi.model.MULTIVI(combined, n_genes=n_genes, n_regions=n_peaks)
model.train(max_epochs=5)
latent = model.get_latent_representation()
print("Latent shape:", latent.shape)
print("Status: COMPLETED (independently constructed -- the skill ships no MultiVI code to test)")
