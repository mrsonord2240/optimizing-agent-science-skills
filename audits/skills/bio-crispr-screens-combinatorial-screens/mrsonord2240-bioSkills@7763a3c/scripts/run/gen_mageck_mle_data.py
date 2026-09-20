"""
Input 4 (Variant B: MAGeCK MLE with explicit interaction terms) data generator.
Builds a small synthetic sgRNA count table + design matrix exactly matching
the SKILL.md "Run Combinatorial Screen Analysis (MAGeCK MLE with Interaction
Indicator)" section: 4 conditions (NT, A_KO, B_KO, A_B_KO), 2 replicates each,
with a design matrix column 'interaction' = 1 only for the AB_KO samples.

Library: 38 background (neutral) genes + GENEA + GENEB, 5 sgRNAs/gene = 200
sgRNAs total -- small enough for mageck mle to converge in seconds rather
than the multi-hour genome-scale runtime noted in TOOLS.md.

Simulated biology:
 - GENEA sgRNAs depleted under A_KO and AB_KO (single-KO fitness defect)
 - GENEB sgRNAs depleted under B_KO and AB_KO (single-KO fitness defect)
 - GENEA sgRNAs get an EXTRA depletion specifically in AB_KO beyond the
   additive single-KO effect (planted synthetic-lethal interaction)
 - Background genes: flat, Poisson noise only (normalization controls)
All data synthetic.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)

n_bg_genes = 38
guides_per_gene = 5
baseline_count = 500

genes = ["GENEA", "GENEB"] + [f"BG{i:02d}" for i in range(1, n_bg_genes + 1)]
rows = []
for g in genes:
    for gi in range(guides_per_gene):
        rows.append({"sgRNA": f"{g}_sg{gi}", "gene": g})
lib = pd.DataFrame(rows)

samples = ["NT_r1", "NT_r2", "A_r1", "A_r2", "B_r1", "B_r2", "AB_r1", "AB_r2"]


def depletion_factor(gene, sample):
    cond = sample.split("_")[0]  # NT / A / B / AB
    factor = 1.0
    if gene == "GENEA" and cond in ("A", "AB"):
        factor *= 0.55  # single-KO defect
    if gene == "GENEB" and cond in ("B", "AB"):
        factor *= 0.55
    if gene == "GENEA" and cond == "AB":
        factor *= 0.5  # extra synthetic-lethal interaction beyond additive
    return factor


count_cols = {s: [] for s in samples}
for _, row in lib.iterrows():
    for s in samples:
        f = depletion_factor(row["gene"], s)
        mean_count = baseline_count * f
        count_cols[s].append(rng.poisson(mean_count))

for s in samples:
    lib[s] = count_cols[s]

lib.to_csv("combo_counts.txt", sep="\t", index=False)

design = pd.DataFrame({
    "Samples":     samples,
    "baseline":    [1, 1, 1, 1, 1, 1, 1, 1],
    "geneA":       [0, 0, 1, 1, 0, 0, 1, 1],
    "geneB":       [0, 0, 0, 0, 1, 1, 1, 1],
    "interaction": [0, 0, 0, 0, 0, 0, 1, 1],
})
design.to_csv("combo_design.txt", sep="\t", index=False)

print("Wrote combo_counts.txt:", lib.shape)
print("Wrote combo_design.txt:")
print(design.to_string(index=False))
