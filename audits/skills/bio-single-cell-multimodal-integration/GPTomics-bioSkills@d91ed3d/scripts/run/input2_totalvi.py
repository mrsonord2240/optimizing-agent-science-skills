# Input 2 (Variant A): "Train totalVI on my CITE-seq MuData and give me denoised protein
# plus foreground probabilities." Follows SKILL.md's totalVI pattern.
# Determinism check: run the documented pattern twice without setting scvi.settings.seed
# (as the SKILL.md pattern does not mention it) and compare latent representations.
import numpy as np
import anndata as ad
import mudata as md
import scvi

rng = np.random.default_rng(0)
n_cells, n_genes, n_prot = 300, 200, 15
rna_counts = rng.poisson(2.0, size=(n_cells, n_genes)).astype("float32")
prot_counts = rng.poisson(20.0, size=(n_cells, n_prot)).astype("float32")

rna = ad.AnnData(rna_counts)
rna.layers["counts"] = rna_counts
prot = ad.AnnData(prot_counts)
prot.layers["counts"] = prot_counts

mdata = md.MuData({"rna": rna, "prot": prot})
mdata.obs_names = [f"cell{i}" for i in range(n_cells)]
for m in mdata.mod.values():
    m.obs_names = mdata.obs_names


def run_totalvi(seed_setting=None):
    if seed_setting is not None:
        scvi.settings.seed = seed_setting
    mdata_local = mdata.copy()
    scvi.model.TOTALVI.setup_mudata(
        mdata_local, rna_layer="counts", protein_layer="counts",
        modalities={"rna_layer": "rna", "protein_layer": "prot"},
    )
    model = scvi.model.TOTALVI(mdata_local)
    model.train(max_epochs=5)
    latent = model.get_latent_representation()
    fg = model.get_protein_foreground_probability()
    return latent, fg


print("=== Run A (no seed set, as SKILL.md pattern does not set scvi.settings.seed) ===")
latent_a, fg_a = run_totalvi(seed_setting=None)
print("latent shape:", latent_a.shape, "fg shape:", fg_a.shape)

print("=== Run B (same call, fresh process-level default seed) ===")
latent_b, fg_b = run_totalvi(seed_setting=None)

diff = np.abs(latent_a - latent_b).max()
print(f"Max abs difference between run A and run B latents (unseeded pattern): {diff:.4f}")
print("Identical (unseeded):", np.allclose(latent_a, latent_b))

print("=== Run C and D with scvi.settings.seed=0 explicitly set each time ===")
latent_c, _ = run_totalvi(seed_setting=0)
latent_d, _ = run_totalvi(seed_setting=0)
diff_seeded = np.abs(latent_c - latent_d).max()
print(f"Max abs difference between run C and run D latents (seed=0 each time): {diff_seeded:.4f}")
print("Identical (seeded):", np.allclose(latent_c, latent_d))

print("Status: COMPLETED")
