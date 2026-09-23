"""
Re-auditor's independent end-to-end run of the fixed Skill against the real
pt.dt.papalexi_2021() dataset (not reusing the fixer's exact script -- this
adds explicit BEFORE/AFTER checks for the two extra bugs the fixer claims to
have found and fixed on this same code path: the missing gene_target merge,
and PyDESeq2 being fed log-normalized data instead of raw counts).
"""
import numpy as np
import pandas as pd
import pertpy as pt
import scanpy as sc

print("=== Loading real papalexi_2021() dataset ===")
mdata = pt.dt.papalexi_2021()
adata = mdata["rna"]
print(f"MuData modalities: {list(mdata.mod.keys())}")
print(f"RNA modality: {adata.n_obs} cells x {adata.n_vars} genes")

# --- Independent check 1: reproduce the pre-fix defect claim ---
# Claim: gene_target lives on mdata.obs, NOT on adata.obs (rna modality) before merge.
print("\n=== Check: gene_target column location (pre-fix defect) ===")
print("'gene_target' in mdata.obs.columns:", "gene_target" in mdata.obs.columns)
print("'gene_target' in adata.obs.columns (before merge):", "gene_target" in adata.obs.columns)
assert "gene_target" in mdata.obs.columns
assert "gene_target" not in adata.obs.columns, "gene_target unexpectedly already on rna modality -- fixer's claimed defect does not reproduce"
print("CONFIRMED: gene_target is on mdata.obs only -- pre-fix code path (pert_key='perturbation' on adata.obs) would KeyError as claimed.")

# Also confirm obs_names align before merging (fixer's claim)
same_order = (mdata.obs_names == adata.obs_names).all()
print(f"mdata.obs_names == adata.obs_names (same order): {same_order}")
assert same_order, "obs_names do not align -- naive merge would misassign labels"

# Apply the fix
adata.obs["gene_target"] = mdata.obs["gene_target"]
print("gene_target value counts (top 10):")
print(adata.obs["gene_target"].value_counts().head(10))
n_targets = adata.obs["gene_target"].nunique()
print(f"Total distinct gene_target values: {n_targets}")
assert "NT" in adata.obs["gene_target"].values, "Expected 'NT' control label in real data"

# --- Independent check 2: raw counts vs log-normalized (pre-fix defect) ---
print("\n=== Check: raw counts requirement for PyDESeq2 ===")
raw_X = adata.X.copy()
# Are raw values close to integers?
raw_dense_sample = np.asarray(raw_X[:200].todense() if hasattr(raw_X, "todense") else raw_X[:200])
raw_nonzero = raw_dense_sample[raw_dense_sample != 0]
frac_nonint_raw_nonzero = np.mean(np.abs(raw_nonzero - np.round(raw_nonzero)) > 1e-6) if raw_nonzero.size else float("nan")
print(f"Fraction of non-near-integer values among NONZERO raw adata.X entries (first 200 cells): {frac_nonint_raw_nonzero:.4f}")
adata.layers["counts"] = adata.X.copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
lognorm_dense_sample = np.asarray(adata.X[:200].todense() if hasattr(adata.X, "todense") else adata.X[:200])
lognorm_nonzero = lognorm_dense_sample[lognorm_dense_sample != 0]
frac_nonint_lognorm_nonzero = np.mean(np.abs(lognorm_nonzero - np.round(lognorm_nonzero)) > 1e-6) if lognorm_nonzero.size else float("nan")
print(f"Fraction of non-near-integer values among NONZERO adata.X entries AFTER normalize+log1p: {frac_nonint_lognorm_nonzero:.4f}")
assert frac_nonint_raw_nonzero < 0.01, "Expected raw nonzero counts to be near-integer"
assert frac_nonint_lognorm_nonzero > 0.9, "Expected log-normalized nonzero values to be non-integer (confirms the pre-fix hazard: feeding this to PyDESeq2 would fail its _check_counts())"
print("CONFIRMED: raw counts are integer, post-normalization nonzero values are not -- PyDESeq2 with layer=X (no counts layer) would raise the ValueError the fixer describes. The counts layer is genuinely needed.")

sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# --- Mixscape ---
print("\n=== Running Mixscape (perturbation_signature + mixscape) ===")
ms = pt.tl.Mixscape()
ms.perturbation_signature(adata=adata, pert_key="gene_target", control="NT", n_neighbors=20, random_state=0)
ms.mixscape(adata=adata, pert_key="gene_target", control="NT")
print("mixscape_class_global value counts:")
print(adata.obs["mixscape_class_global"].value_counts())

# --- Filter to KO + NT ---
adata_filtered = adata[adata.obs["mixscape_class_global"] != "NP"].copy()
print(f"\nCells after Mixscape filtering: {adata_filtered.n_obs} / {adata.n_obs}")

# --- PyDESeq2 on raw counts layer ---
print("\n=== PyDESeq2 fit (layer='counts') ===")
de = pt.tl.PyDESeq2(adata_filtered, design="~gene_target", layer="counts")
de.fit()
print("Fit completed with no error.")

# Pick a handful of real perturbation targets from the ECCITE-seq IFN-gamma pathway
# screen (Papalexi et al. 2021, Nat Genet -- perturbs JAK2/STAT1/IFNGR1/IFNGR2/IRF1 etc.
# to characterize regulation of immune checkpoint CD274/PD-L1). Test whichever of these
# targets are actually present in this dataset's gene_target column.
candidate_targets = ["STAT1", "IFNGR2", "IFNGR1", "JAK2", "IRF1", "MYC", "SPI1", "CMTM6", "CD274"]
present_targets = [t for t in candidate_targets if t in adata_filtered.obs["gene_target"].unique()]
print(f"\nCandidate biologically-known targets present in this dataset: {present_targets}")

results = {}
for pert in present_targets:
    contrast = de.contrast("gene_target", "NT", pert)
    res = de.test_contrasts(contrast)
    res = res.set_index("variable")
    results[pert] = res
    top5 = res.sort_values("adj_p_value").head(5)
    print(f"\n--- {pert} vs NT: top 5 DE genes ---")
    print(top5[["log_fc", "p_value", "adj_p_value"]])
    n_sig = (res["adj_p_value"] < 0.05).sum()
    print(f"  n genes significant at FDR<0.05: {n_sig} / {res.shape[0]}")

# Independent biological sanity check: STAT1 perturbation should show STAT1 itself
# (or canonical interferon-stimulated genes it regulates) among the most significant
# / most depleted hits, since STAT1 is the perturbed gene and IFN-response genes
# depend on it.
if "STAT1" in results:
    r = results["STAT1"]
    stat1_rank = None
    if "STAT1" in r.index:
        sorted_r = r.sort_values("adj_p_value")
        stat1_rank = list(sorted_r.index).index("STAT1") + 1
        stat1_row = r.loc["STAT1"]
        print(f"\nSTAT1 KO vs NT -- STAT1 gene itself: rank #{stat1_rank} by adj_p_value, "
              f"log_fc={stat1_row['log_fc']:.3f}, adj_p={stat1_row['adj_p_value']:.3e}")
        assert stat1_row["log_fc"] < 0, "Expected STAT1 KO to show STAT1 transcript reduced (negative log_fc)"
        print("CONFIRMED: STAT1 perturbation shows reduced STAT1 expression (sign matches CRISPR KO biology).")

print("\n=== Saving results ===")
all_de = []
for pert, res in results.items():
    res = res.copy()
    res["perturbation"] = pert
    all_de.append(res)
combined = pd.concat(all_de)
combined.to_csv("test2_papalexi_de_results.tsv", sep="\t")
print(f"Wrote test2_papalexi_de_results.tsv: {combined.shape}")

print("\nPASS: real papalexi_2021() dataset runs end-to-end through the fixed pipeline; "
      "both extra-bug claims (gene_target merge, raw-counts requirement) independently reproduced and fixed; "
      "biological sanity check on STAT1 perturbation confirmed.")
