"""
Synthetic data generator for auditing bio-crispr-screens-combinatorial-screens.
Models a small Cas12a in4mer-style paralog-pair screen:
 - 16 genes -> 8 paralog pairs
 - singleton LFCs (mild negative, i.e. mildly detrimental single-KO)
 - paired LFCs for each pair, with 4 replicate cassettes each
 - 2 pairs planted as strong synthetic-lethal (GI << expected additive)
 - 1 pair planted as synthetic-rescue (GI >> expected additive)
 - remaining 5 pairs approximately additive (no interaction) + noise
All data synthetic; not derived from any real screen.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)

genes = [f"G{i:02d}" for i in range(1, 17)]
pairs = [(genes[i], genes[i + 1]) for i in range(0, 16, 2)]  # 8 pairs

# Singleton LFCs: mild, gene-specific fitness defect
single_lfc = {g: rng.normal(-0.3, 0.15) for g in genes}

records_single = [{"gene": g, "lfc": v} for g, v in single_lfc.items()]
single_df = pd.DataFrame(records_single)
single_df.to_csv("single_lfc.tsv", sep="\t", index=False)

paired_rows = []
plant_sl = {pairs[0], pairs[1]}       # synthetic lethal
plant_rescue = {pairs[2]}             # synthetic rescue
cassette_counter = 0
for (a, b) in pairs:
    expected_additive = single_lfc[a] + single_lfc[b]
    if (a, b) in plant_sl:
        true_gi = -1.8  # strong synthetic lethal offset
    elif (a, b) in plant_rescue:
        true_gi = 1.6   # strong synthetic rescue offset
    else:
        true_gi = rng.normal(0, 0.05)  # near-additive
    for rep in range(4):  # 4 cassettes per pair (Inzolia convention)
        cassette_counter += 1
        noisy_lfc = expected_additive + true_gi + rng.normal(0, 0.12)
        paired_rows.append({
            "cassette_id": f"cass_{cassette_counter:03d}",
            "gene_A": a,
            "gene_B": b,
            "lfc": noisy_lfc,
        })

paired_df = pd.DataFrame(paired_rows)
paired_df.to_csv("paired_lfc.tsv", sep="\t", index=False)

print("Wrote single_lfc.tsv:", single_df.shape)
print("Wrote paired_lfc.tsv:", paired_df.shape)
print("Planted synthetic-lethal pairs:", plant_sl)
print("Planted synthetic-rescue pairs:", plant_rescue)
