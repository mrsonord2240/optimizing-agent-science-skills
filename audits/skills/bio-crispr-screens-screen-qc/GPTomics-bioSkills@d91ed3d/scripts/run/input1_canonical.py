"""Input 1 (Canonical). Prompt (as a researcher would send it):
"Audit my CRISPR screen quality before hit calling. This is a HAP1 TKOv3
pooled-knockout screen: one plasmid-stage column (HAP1_T0) and three endpoint
replicates (HAP1_T18A/B/C). Check library representation, Gini, replicate
Pearson/Spearman, sequencing depth, and CEGv2 essentialome recovery, then tell
me whether this screen is usable for hit calling."
Data: real HAP1 TKOv3 counts (hart-lab/bagel, MIT), unmodified.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\run")
import pandas as pd
import numpy as np
from qc_functions import (library_representation, stage_specific_thresholds, gini,
                           replicate_concordance, essentialome_recovery, depth_audit)

DATA = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_canonical.txt"
CEGV2 = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\CEGv2_core_essentials.txt"
NEGV1 = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\NEGv1_nonessentials.txt"

df = pd.read_csv(DATA, sep="\t")
counts = df[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]]
counts.index = df["SEQUENCE"]
gene_col = df.set_index("SEQUENCE")["GENE"]

print("=== Library representation ===")
lib = library_representation(counts)
print(lib.round(3))

print("\n=== Gini per sample vs stage thresholds ===")
thr = stage_specific_thresholds()
for col in counts.columns:
    g = gini(counts[col].to_numpy())
    stage = "plasmid" if col == "HAP1_T0" else "endpoint"
    verdict = "PASS" if g < thr[stage]["gini_max"] else "FAIL"
    print(f"{col} (stage={stage}): Gini={g:.4f} threshold<{thr[stage]['gini_max']} -> {verdict}")

print("\n=== Replicate concordance (endpoint T18 A/B/C) ===")
cond_map = {"T18_endpoint": ["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]}
rc = replicate_concordance(counts, cond_map)
print(rc.round(4))
for _, row in rc.iterrows():
    flag = "FAIL (<0.8 MAGeCK-VISPR floor)" if row["pearson_log"] < 0.8 else "PASS"
    print(f"  {row['rep1']} vs {row['rep2']}: pearson_log={row['pearson_log']:.4f} [{flag}]")

print("\n=== Sequencing depth ===")
print(depth_audit(counts).round(2))

print("\n=== CEGv2 / NEGv1 essentialome recovery ===")
cegv2 = set(pd.read_csv(CEGV2, sep="\t")["GENE"].str.strip())
negv1 = set(pd.read_csv(NEGV1, sep="\t")["GENE"].str.strip())
# Gene-level LFC: mean log2(T18_mean / T0) across guides per gene, for QC purposes only
merged = pd.DataFrame({
    "gene": gene_col.values,
    "t0": counts["HAP1_T0"].values,
    "t18_mean": counts[["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]].mean(axis=1).values,
})
merged["lfc_guide"] = np.log2((merged["t18_mean"] + 1) / (merged["t0"] + 1))
gene_lfc = merged.groupby("gene", as_index=False)["lfc_guide"].mean().rename(columns={"lfc_guide": "lfc"})
result = essentialome_recovery(gene_lfc, cegv2, negv1)
print(result)
verdict = "PASS (screen has essentiality signal)" if result["pr_auc"] > 0.7 else \
          ("CAUTION" if result["pr_auc"] > 0.5 else "FAIL (no essentiality signal)")
print(f"PR-AUC={result['pr_auc']:.4f} -> {verdict}")
