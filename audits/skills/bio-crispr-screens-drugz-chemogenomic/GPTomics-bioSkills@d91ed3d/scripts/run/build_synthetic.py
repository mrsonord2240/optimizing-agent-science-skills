"""
Build a synthetic chemogenomic (drug vs vehicle) screen from the real HAP1
TKOv3 counts, with planted drug-specific sensitizer/suppressor genes as
ground truth. This is SYNTHETIC DATA -- the base sgRNA/gene structure and T0
counts are real (hart-lab/bagel reads_hap1.txt), but there is no real drug
arm in the source data, so the "Vehicle" and "Drug" arms below are
constructed for this audit only.

Design:
  Vehicle_r1/r2/r3 = real HAP1_T18A/B/C replicate counts (normal culture growth,
                     no drug -- this matches the Skill's own vehicle-anchored design).
  Drug_r1/r2/r3    = Vehicle counts x per-gene multiplier x per-replicate noise.
                       - planted SENSITIZER genes (KO sensitizes to drug): x0.22 (strong extra depletion)
                       - planted SUPPRESSOR genes (KO confers resistance): x4.5 (strong extra enrichment)
                       - drug-target gene (paradox case, Failure Mode #5 in SKILL.md): x3.0 (appears as suppressor)
                       - all other genes: x1.0 with small multiplicative noise (no drug-specific effect)

Genes are chosen from real TKOv3 genes with >=6 sgRNAs and near-neutral
T18-vs-T0 baseline fold change (|log2FC| < 0.5, average across replicates),
so the planted drug effect is not confounded with baseline essentiality/
growth-suppressor behavior already in the real data.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260916)

SRC = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\HAP1_TKOv3_reads.txt"
OUT_DIR = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data"

df = pd.read_csv(SRC, sep="\t")
df = df.rename(columns={"SEQUENCE": "GUIDE"})

# baseline log2FC per sgRNA (T18 mean vs T0), pseudo-count 5 as the Skill recommends
pc = 5.0
t0 = df["HAP1_T0"] + pc
t18_mean = df[["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]].mean(axis=1) + pc
df["_lfc"] = np.log2(t18_mean / t0)

gene_stats = df.groupby("GENE").agg(n_sgrna=("GUIDE", "size"), mean_lfc=("_lfc", "mean"))
# TKOv3 median is ~4 sgRNAs/gene (a lean library); the Skill's own stated
# stability floor is 4-6 guides/gene, so >=4 matches real library design
# rather than an idealized threshold.
candidates = gene_stats[(gene_stats["n_sgrna"] >= 4) & (gene_stats["mean_lfc"].abs() < 1.0)]
candidate_genes = sorted(candidates.index.tolist())
print(f"Neutral candidate genes (>=4 sgRNAs, |baseline LFC|<1.0): {len(candidate_genes)}")

pick = rng.choice(candidate_genes, size=13, replace=False)
sensitizers = sorted(pick[0:6].tolist())
suppressors = sorted(pick[6:12].tolist())
drug_target = pick[12]

print("Planted SENSITIZERS (ground truth, expect fdr_synth<0.05):", sensitizers)
print("Planted SUPPRESSORS (ground truth, expect fdr_supp<0.05):", suppressors)
print("Planted DRUG-TARGET paradox gene (expect fdr_supp<0.05):", drug_target)

gene_mult = {g: 0.22 for g in sensitizers}
gene_mult.update({g: 4.5 for g in suppressors})
gene_mult[drug_target] = 3.0

veh_cols = ["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]
drug_cols = ["Drug_r1", "Drug_r2", "Drug_r3"]

out = df[["GUIDE", "GENE", "HAP1_T0"] + veh_cols].copy()
out = out.rename(columns={"HAP1_T0": "T0", "HAP1_T18A": "Veh_r1", "HAP1_T18B": "Veh_r2", "HAP1_T18C": "Veh_r3"})

for i, (vc, dc) in enumerate(zip(["Veh_r1", "Veh_r2", "Veh_r3"], drug_cols)):
    mult = out["GENE"].map(gene_mult).fillna(1.0).to_numpy()
    noise = rng.lognormal(mean=0.0, sigma=0.08, size=len(out))
    vals = out[vc].to_numpy() * mult * noise
    out[dc] = np.round(np.clip(vals, 0, None)).astype(int)

out.to_csv(f"{OUT_DIR}/synthetic_drug_vehicle_counts.txt", sep="\t", index=False)

with open(f"{OUT_DIR}/ground_truth.txt", "w") as f:
    f.write("planted_sensitizers\t" + ",".join(sensitizers) + "\n")
    f.write("planted_suppressors\t" + ",".join(suppressors) + "\n")
    f.write("planted_drug_target_paradox\t" + drug_target + "\n")

print("Wrote", f"{OUT_DIR}/synthetic_drug_vehicle_counts.txt", "rows:", len(out))

# --- Day-0 vs Drug variant (for the Day-0-mistake diagnostic input) ---
# Same drug arm, but "control" wrongly set to T0 instead of vehicle.
out2 = out[["GUIDE", "GENE", "T0", "Drug_r1", "Drug_r2", "Drug_r3"]].copy()
out2.to_csv(f"{OUT_DIR}/synthetic_day0_vs_drug_counts.txt", sep="\t", index=False)
print("Wrote", f"{OUT_DIR}/synthetic_day0_vs_drug_counts.txt")
