"""T3 Skill-Veto determinism check: run the Skill's documented Mixscape call pattern
twice on identical input (fresh copies) with NO seed argument (as the Skill's own
SKILL.md / examples/run_pertpy.py code does), and compare outputs.
"""
import pertpy as pt
import scanpy as sc
import anndata as ad
import numpy as np

def run_once():
    adata = ad.read_h5ad("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/synthetic_perturbseq.h5ad")
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=100)
    ms = pt.tl.Mixscape()
    # Verbatim SKILL.md call -- no seed/random_state argument passed to perturbation_signature
    ms.perturbation_signature(adata, pert_key='perturbation', control='NTC', n_neighbors=20)
    ms.mixscape(adata, pert_key='perturbation', control='NTC')  # mixscape() itself defaults random_state=0
    return adata

a1 = run_once()
a2 = run_once()

xpert1 = np.asarray(a1.layers['X_pert'].todense() if hasattr(a1.layers['X_pert'], 'todense') else a1.layers['X_pert'])
xpert2 = np.asarray(a2.layers['X_pert'].todense() if hasattr(a2.layers['X_pert'], 'todense') else a2.layers['X_pert'])

identical_xpert = np.array_equal(xpert1, xpert2)
max_abs_diff = np.max(np.abs(xpert1 - xpert2))
n_diff_cells = np.sum(np.any(xpert1 != xpert2, axis=1))

print(f"X_pert layer identical across 2 runs (no seed passed): {identical_xpert}")
print(f"Max abs diff in X_pert: {max_abs_diff}")
print(f"Cells with any differing X_pert value: {n_diff_cells} / {a1.n_obs}")

class1 = a1.obs['mixscape_class_global'].values
class2 = a2.obs['mixscape_class_global'].values
n_class_diff = np.sum(class1 != class2)
print(f"\nmixscape_class_global identical: {np.array_equal(class1, class2)}")
print(f"Cells with differing mixscape_class_global: {n_class_diff} / {len(class1)}")

for pert in ["GENE_A", "GENE_B", "GENE_C", "GENE_D"]:
    m1 = a1.obs.loc[a1.obs['perturbation'] == pert, 'mixscape_class_global']
    m2 = a2.obs.loc[a2.obs['perturbation'] == pert, 'mixscape_class_global']
    ko1 = (m1 == 'KO').mean()
    ko2 = (m2 == 'KO').mean()
    print(f"{pert}: KO retention run1={ko1:.1%} run2={ko2:.1%} (delta={abs(ko1-ko2)*100:.2f}pp)")
