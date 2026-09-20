"""
Larger, more representative synthetic dataset for Input 1 (Canonical) and
Input 5 (Stress): 200 paralog pairs (vs. the toy 8-pair set used for the
Input 3 edge case), 4 cassettes/pair, to give the z-score-based GI cutoff
(z < -2 / z > 2) a properly populated null distribution -- closer to real
screen scale (Inzolia covers ~4,435 pairs) than the 8-pair toy set.
8 pairs are planted as synthetic-lethal, 4 as synthetic-rescue, the rest
near-additive + noise. All data synthetic.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)

n_pairs = 200
genes = [f"G{i:04d}" for i in range(1, n_pairs * 2 + 1)]
pairs = [(genes[i], genes[i + 1]) for i in range(0, n_pairs * 2, 2)]

single_lfc = {g: rng.normal(-0.3, 0.15) for g in genes}
pd.DataFrame([{"gene": g, "lfc": v} for g, v in single_lfc.items()]).to_csv(
    "single_lfc_genome.tsv", sep="\t", index=False
)

plant_sl = set(pairs[0:8])
plant_rescue = set(pairs[8:12])

rows = []
cassette_counter = 0
for (a, b) in pairs:
    expected_additive = single_lfc[a] + single_lfc[b]
    if (a, b) in plant_sl:
        true_gi = -1.8
    elif (a, b) in plant_rescue:
        true_gi = 1.6
    else:
        true_gi = rng.normal(0, 0.05)
    for rep in range(4):
        cassette_counter += 1
        noisy_lfc = expected_additive + true_gi + rng.normal(0, 0.12)
        rows.append({
            "cassette_id": f"cass_{cassette_counter:04d}",
            "gene_A": a,
            "gene_B": b,
            "lfc": noisy_lfc,
        })

pd.DataFrame(rows).to_csv("paired_lfc_genome.tsv", sep="\t", index=False)
print(f"pairs={n_pairs}, planted_SL={len(plant_sl)}, planted_rescue={len(plant_rescue)}")
print("SL pairs:", sorted(plant_sl)[:3], "...")
print("Rescue pairs:", sorted(plant_rescue)[:3], "...")
