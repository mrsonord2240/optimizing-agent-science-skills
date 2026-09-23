"""Run the SKILL.md totalVI block EXACTLY as shipped (post-fix, verbatim minus mdata load)
in its own fresh process, save the latent to disk. Called twice as separate subprocess
invocations (not just separate function calls in one process) to catch process-level
nondeterminism the original audit's within-process test could have missed.
"""
import sys
import numpy as np
import mudata as md

# ---- verbatim SKILL.md CITE-seq totalVI block (post-fix) below this line ----
import scvi

# scvi-tools VAE training is stochastic unless seeded: verified two unseeded runs of this
# exact pattern on identical input differ by up to 0.97 (max abs latent diff); seeding
# makes reruns bit-identical. Set this before setup_mudata/train, every run.
scvi.settings.seed = 0

mdata = md.read_h5mu("reaudit_cite_seq.h5mu")

# mdata holds .mod['rna'] (raw counts) and .mod['prot'] (raw ADT counts)
scvi.model.TOTALVI.setup_mudata(
    mdata, rna_layer='counts', protein_layer=None,
    modalities={'rna_layer': 'rna', 'protein_layer': 'prot'}
)
model = scvi.model.TOTALVI(mdata)
model.train(max_epochs=5)

mdata.obsm['X_totalVI'] = model.get_latent_representation()
fg = model.get_protein_foreground_probability()        # 1 - background mixing weight per protein per cell
denoised_rna, denoised_prot = model.get_normalized_expression()
# ---- end verbatim block ----

out = sys.argv[1] if len(sys.argv) > 1 else "latent_out.npy"
np.save(out, mdata.obsm['X_totalVI'])
print(f"saved {out}, shape={mdata.obsm['X_totalVI'].shape}, fg shape={fg.shape}")
