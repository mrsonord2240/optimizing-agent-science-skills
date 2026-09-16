"""Prepare canonical + planted-fault datasets for the screen-qc audit.
Source: real HAP1 TKOv3 counts (hart-lab/bagel, MIT), cached at
F:\\OpenScience\\audit-envs\\crispr-screen-analyst\\public-data\\HAP1_TKOv3_reads.txt
Writes into F:\\OpenScience\\audits\\bio-crispr-screens-screen-qc\\data\\
"""
import pandas as pd
import numpy as np

np.random.seed(0)

SRC = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\HAP1_TKOv3_reads.txt"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data"

df = pd.read_csv(SRC, sep="\t")
print("Loaded real HAP1 TKOv3:", df.shape, list(df.columns))

# --- Input 1 (canonical): real data, unmodified, just copied for provenance ---
df.to_csv(f"{OUT}\\hap1_tkov3_canonical.txt", sep="\t", index=False)

# --- Input 4 (edge, planted fault A): dropped-out guides in one replicate ---
# Simulate a library-prep failure on HAP1_T18B: zero out a random 8% of guides
# (well above the <5% endpoint failure threshold in SKILL.md) plus heavy
# uniform down-sampling to mimic a shallow/failed prep.
degraded_dropout = df.copy()
n = len(degraded_dropout)
drop_idx = np.random.choice(n, size=int(0.08 * n), replace=False)
degraded_dropout.loc[drop_idx, "HAP1_T18B"] = 0
# also crush remaining counts in that column to simulate low-depth resequencing
keep_mask = np.ones(n, dtype=bool)
keep_mask[drop_idx] = False
degraded_dropout.loc[keep_mask, "HAP1_T18B"] = (
    degraded_dropout.loc[keep_mask, "HAP1_T18B"] * 0.05
).round()
degraded_dropout.to_csv(f"{OUT}\\hap1_tkov3_dropout_fault.txt", sep="\t", index=False)
print("Dropout-fault file written. Zeroed guides:", len(drop_idx),
      f"({len(drop_idx)/n*100:.2f}% of {n})")

# --- Input 5 (stress, planted fault B): swapped-in plasmid replicate + low depth sample ---
# Realistic sample-sheet mixup: the T0 (plasmid) sample tube gets mislabeled
# and sequenced a second time as if it were an endpoint replicate, replacing
# what should have been a real HAP1_T18B endpoint replicate (jittered so it
# is not a byte-identical duplicate of T0, as a real re-prep would not be).
# Separately, HAP1_T18C is down-sampled 50x to simulate a low-depth lane.
swap_lowdepth = df.copy()
jitter = rng_swap = np.random.default_rng(2)
plasmid_vals = swap_lowdepth["HAP1_T0"].to_numpy(dtype=float)
noisy_plasmid_copy = np.clip(
    plasmid_vals * rng_swap.normal(1.0, 0.03, size=len(plasmid_vals)), 0, None
).round()
swap_lowdepth["HAP1_T18B"] = noisy_plasmid_copy  # mislabeled plasmid masquerading as endpoint rep
swap_lowdepth["HAP1_T18C"] = (swap_lowdepth["HAP1_T18C"] / 50.0).round()  # low-depth lane
swap_lowdepth.to_csv(f"{OUT}\\hap1_tkov3_swap_lowdepth_fault.txt", sep="\t", index=False)
print("Swap(plasmid-as-endpoint)+low-depth fault file written.")

# --- Synthetic copy-number profile for Input 3 (CN bias diagnostic) ---
# No real matched WGS/SNP-array profile ships with this dataset, so this is
# a SYNTHETIC per-gene copy-number table: most genes diploid (CN~2), a
# deliberately amplified block of 40 genes at CN 6-10 (mimicking a focal
# amplicon) whose guides we also make appear depleted in a companion
# gene-level LFC table, to test whether the CN-bias diagnostic catches the
# artifact.
genes = df["GENE"].unique()
rng = np.random.default_rng(1)
cn = pd.DataFrame({"gene": genes})
cn["copy_number"] = np.clip(rng.normal(2.0, 0.3, size=len(genes)), 1.0, 3.0)
amplified_genes = rng.choice(genes, size=40, replace=False)
cn.loc[cn["gene"].isin(amplified_genes), "copy_number"] = rng.uniform(6, 10, size=40)
cn.to_csv(f"{OUT}\\synthetic_copy_number.txt", sep="\t", index=False)

# Companion synthetic gene-level LFC: real biology (essential genes depleted)
# PLUS an injected CN artifact -- amplified genes get extra negative LFC
# independent of essentiality, which is exactly what cn_bias_diagnostic()
# is supposed to catch.
gene_lfc = pd.DataFrame({"gene": genes})
gene_lfc["lfc"] = rng.normal(0, 0.4, size=len(genes))
gene_lfc = gene_lfc.merge(cn, on="gene")
artifact_penalty = -0.15 * (gene_lfc["copy_number"] - 2.0).clip(lower=0)
gene_lfc["lfc"] = gene_lfc["lfc"] + artifact_penalty
gene_lfc[["gene", "lfc"]].to_csv(f"{OUT}\\synthetic_gene_lfc_for_cn.txt", sep="\t", index=False)

print("Synthetic CN + gene-LFC files written. Amplified genes:", list(amplified_genes[:8]), "...")
print("DONE")
