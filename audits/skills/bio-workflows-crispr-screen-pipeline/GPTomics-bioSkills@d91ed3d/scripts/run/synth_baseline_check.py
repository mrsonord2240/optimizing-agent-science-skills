import numpy as np, pandas as pd
rng = np.random.default_rng(42)
n_genes = 200
n_guides_per_gene = 4
genes = [f"GENE{i}" for i in range(n_genes)]
# 20 genes are "true drug targets" -> extra depletion only in drug arm
drug_targets = set(genes[:20])

rows = []
for g in genes:
    base_gene_effect = rng.normal(0, 0.05)  # normal proliferation-driven per-gene noise
    for k in range(n_guides_per_gene):
        day0 = rng.poisson(500)
        # normal proliferation dropout by Day14 in both arms (~30% loss), independent of drug
        veh_mult = 0.7 + base_gene_effect + rng.normal(0, 0.05)
        drug_extra = -0.3 if g in drug_targets else 0.0  # true drug effect only in drug arm
        drug_mult = 0.7 + base_gene_effect + drug_extra + rng.normal(0, 0.05)
        veh = max(0, rng.poisson(max(day0 * veh_mult, 1)))
        drug = max(0, rng.poisson(max(day0 * drug_mult, 1)))
        rows.append([f"sg_{g}_{k}", g, day0, veh, drug])

df = pd.DataFrame(rows, columns=["sgRNA", "Gene", "Day0", "Veh", "Drug"])
df.to_csv("synth_drug_screen.count.txt", sep="\t", index=False)
print(df.head())
print("True drug targets (first 5):", list(drug_targets)[:5])
