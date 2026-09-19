"""
Input 1 (Canonical): "I have a Perturb-seq experiment (CROP-seq, low MOI) with guide counts and
RNA counts in a MuData object. Assign guides with a mixture model and run Mixscape to remove
non-perturbed cells."

Follows SKILL.md's Guide Assignment + Mixscape + E-distance sections almost verbatim, using
pertpy's real papalexi_2021 CROP-seq dataset (public, downloaded via pertpy.dt).
"""
import sys
import scanpy as sc
import pertpy as pt

print("pertpy", pt.__name__)

mdata = pt.dt.papalexi_2021()
print("MuData modalities:", list(mdata.mod.keys()))
adata = mdata.mod['rna']
print("rna shape:", adata.shape)
print("rna obs columns:", list(adata.obs.columns))

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.pca(adata, n_comps=50)

# --- Guide assignment (SKILL.md "Guide Assignment (pertpy)") ---
gdo = mdata.mod['gdo']
print("gdo shape:", gdo.shape)
if hasattr(gdo.X, 'tocsr'):
    gdo.X = gdo.X.tocsr()
gdo.layers['counts'] = gdo.X.copy()

ga = pt.pp.GuideAssignment()
try:
    ga.assign_mixture_model(gdo, assigned_guides_key='assigned_guide')
    print("\n--- assign_mixture_model succeeded ---")
except ImportError as e:
    print("\n--- assign_mixture_model FAILED (optional JAX backend missing): ---")
    print(repr(e))
    print("Falling back to assign_by_threshold (documented alternative in SKILL.md's decision table) to continue the audit.")
    ga.assign_by_threshold(gdo, assignment_threshold=5, output_layer='assigned_guides')
    import numpy as np
    import pandas as pd
    assigned = gdo.layers['assigned_guides']
    # assign_by_threshold writes a binary cell x guide layer, not a single-column obs call like assign_mixture_model
    if hasattr(assigned, 'toarray'):
        assigned = assigned.toarray()
    n_guides_per_cell = (assigned > 0).sum(axis=1)
    print("guides-per-cell distribution (threshold method):")
    print(pd.Series(n_guides_per_cell).value_counts().sort_index())
    # Build a single-column call for downstream comparability (dominant guide, else Negative)
    guide_names = gdo.var_names.to_numpy()
    calls = []
    for row in assigned:
        idx = np.where(row > 0)[0]
        if len(idx) == 0:
            calls.append('Negative')
        elif len(idx) == 1:
            calls.append(guide_names[idx[0]])
        else:
            calls.append('multiple')
    gdo.obs['assigned_guide'] = calls
print("\n--- assigned_guide value_counts (head) ---")
print(gdo.obs['assigned_guide'].value_counts().head(10))

# --- Mixscape (SKILL.md "Mixscape: Remove Non-Perturbed Escapers (pertpy)") ---
print("\nadata.obs columns for pert_key candidates:", [c for c in adata.obs.columns if 'pert' in c.lower() or 'gene' in c.lower() or 'target' in c.lower() or 'NT' in c])

# FINDING: SKILL.md's shipped pertpy_analysis.py calls ms.mixscape(adata, pert_key='gene_target', ...)
# directly on adata = mdata.mod['rna'], but 'gene_target'/'perturbation' only exist on the JOINED
# mdata.obs, not on adata.obs (confirmed above: adata.obs only has
# ['nCount_RNA','nFeature_RNA','percent.mito']). Running the shipped example verbatim raises
# KeyError: 'perturbation'. Pulling the columns across from mdata.obs (an undocumented step
# SKILL.md never mentions) to continue the audit.
for col in ('perturbation', 'gene_target', 'NT', 'replicate'):
    adata.obs[col] = mdata.obs[col].to_numpy()
print("\n[FINDING] pulled ['perturbation','gene_target','NT','replicate'] from mdata.obs into "
      "adata.obs -- SKILL.md's shipped example does not do this and fails with KeyError as shipped.")

ms = pt.tl.Mixscape()
ms.perturbation_signature(adata, pert_key='perturbation', control='NT', n_neighbors=20)
ms.mixscape(adata, pert_key='gene_target', control='NT', layer='X_pert')
print("\n--- mixscape_class_global value_counts ---")
print(adata.obs['mixscape_class_global'].value_counts())

# --- E-distance (SKILL.md "E-distance and the E-test (pertpy)") ---
dist = pt.tl.Distance(metric='edistance', obsm_key='X_pca')
pairwise = dist.pairwise(adata, groupby='gene_target')
print("\n--- pairwise E-distance (5x5 head) ---")
print(pairwise.iloc[:5, :5])

etest = pt.tl.DistanceTest('edistance', n_perms=100)  # reduced perms for audit runtime; SKILL.md default is 1000
results = etest(adata, groupby='gene_target', contrast='NT')
print("\n--- E-test results (top 5 by pvalue) ---")
print(results.sort_values('pvalue').head())

print("\nDONE input1")
