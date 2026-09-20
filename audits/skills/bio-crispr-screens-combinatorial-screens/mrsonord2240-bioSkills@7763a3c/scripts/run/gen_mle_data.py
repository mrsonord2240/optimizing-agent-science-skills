"""
Fresh synthetic sgRNA count table + design matrix for an independent MAGeCK
MLE reproducibility check (re-auditor's own data, not the fixer's or the
original auditor's).

30 genes x 6 sgRNAs each = 180 sgRNAs. One planted synthetic-lethal gene
(GENE_SL) with a strong negative double-KO effect beyond additive.
Design: NT (control), A_KO, B_KO, AB_KO (interaction indicator), 2 reps each.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(777333)

n_genes = 30
sgrnas_per_gene = 6
genes = [f"G{i:03d}" for i in range(n_genes)]
genes[0] = "GENE_SL"  # planted hit

rows = []
for g in genes:
    for s in range(sgrnas_per_gene):
        rows.append({"sgRNA": f"{g}_sg{s}", "gene": g})
lib = pd.DataFrame(rows)

samples = ["NT_r1", "NT_r2", "A_r1", "A_r2", "B_r1", "B_r2", "AB_r1", "AB_r2"]

base_counts = rng.integers(300, 700, size=len(lib))

counts = pd.DataFrame({"sgRNA": lib["sgRNA"], "gene": lib["gene"]})
for s in samples:
    counts[s] = base_counts + rng.integers(-40, 40, size=len(lib))

# Apply per-gene depletion effects
for i, row in lib.iterrows():
    g = row["gene"]
    if g == "GENE_SL":
        # single effects mild, double effect strongly synergistic (synthetic lethal)
        a_effect, b_effect, ab_effect = 0.85, 0.85, 0.25  # multiplicative on counts
    else:
        # generic small single effects, additive-ish double effect, per-gene jitter
        eff = rng.uniform(0.7, 1.0)
        a_effect, b_effect, ab_effect = eff, eff, eff * eff  # roughly additive in log-space

    for s in samples:
        if s.startswith("A_"):
            counts.loc[i, s] = max(1, int(counts.loc[i, s] * a_effect))
        elif s.startswith("B_"):
            counts.loc[i, s] = max(1, int(counts.loc[i, s] * b_effect))
        elif s.startswith("AB_"):
            counts.loc[i, s] = max(1, int(counts.loc[i, s] * ab_effect))

counts.to_csv("combo_counts.txt", sep="\t", index=False)

design = """Samples\tbaseline\tgeneA\tgeneB\tinteraction
NT_r1\t1\t0\t0\t0
NT_r2\t1\t0\t0\t0
A_r1\t1\t1\t0\t0
A_r2\t1\t1\t0\t0
B_r1\t1\t0\t1\t0
B_r2\t1\t0\t1\t0
AB_r1\t1\t1\t1\t1
AB_r2\t1\t1\t1\t1
"""
with open("combo_design.txt", "w", newline="\n") as f:
    f.write(design)

print("Wrote combo_counts.txt (", len(counts), "sgRNAs,", n_genes, "genes) and combo_design.txt")
