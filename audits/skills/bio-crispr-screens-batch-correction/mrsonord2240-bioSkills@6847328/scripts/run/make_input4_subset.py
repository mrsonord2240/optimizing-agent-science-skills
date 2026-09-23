"""Build Input 4's count table: a manageable gene subset of real HAP1 TKOv3
data, arranged as 2 batches x 2 conditions x 2 replicates (8 samples), with
the SAME planted batch shift as Input 1, so mageck mle's batch-covariate beta
can be checked against a known ground truth."""
import numpy as np
import pandas as pd
from pathlib import Path

PUBLIC = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data")
OUT = Path(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\run")

raw = pd.read_csv(PUBLIC / "HAP1_TKOv3_reads.txt", sep="\t")
cegv2 = set(pd.read_csv(PUBLIC / "CEGv2_core_essentials.txt", sep="\t")["GENE"])

# Keep all CEGv2 essential genes present in the library (real biology, real dropout)
# plus a random sample of non-essential genes, to keep mle's runtime small (~1500 genes
# instead of 18056) while retaining a real, checkable essentiality signal.
rng = np.random.default_rng(3)
ess_present = raw[raw["GENE"].isin(cegv2)]["GENE"].unique()
other_genes = raw[~raw["GENE"].isin(cegv2)]["GENE"].unique()
other_sample = rng.choice(other_genes, size=1000, replace=False)
keep_genes = set(ess_present) | set(other_sample)
sub = raw[raw["GENE"].isin(keep_genes)].reset_index(drop=True)
print(f"Subset: {sub['GENE'].nunique()} genes ({len(ess_present)} CEGv2 essential + 1000 other), "
      f"{len(sub)} guides")

MULT, ADD = 0.5, 150
b1 = pd.DataFrame({
    "B1_veh_1": sub["HAP1_T0"],
    "B1_veh_2": rng.poisson(sub["HAP1_T0"].clip(lower=0).values).astype(float),
    "B1_trt_1": sub["HAP1_T18A"],
    "B1_trt_2": sub["HAP1_T18B"],
})
b2 = pd.DataFrame({
    "B2_veh_1": rng.poisson((sub["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_veh_2": rng.poisson((sub["HAP1_T0"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_trt_1": rng.poisson((sub["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
    "B2_trt_2": rng.poisson((sub["HAP1_T18C"].clip(lower=0) * MULT + ADD).values).astype(float),
})
counts = pd.concat([sub[["SEQUENCE", "GENE"]].rename(columns={"SEQUENCE": "sgRNA", "GENE": "gene"}), b1, b2], axis=1)
counts.to_csv(OUT / "input4_mle_counts.txt", sep="\t", index=False)

sample_cols = list(b1.columns) + list(b2.columns)
batch = [0, 0, 0, 0, 1, 1, 1, 1]        # 0 = batch1, 1 = batch2 (indicator column)
treatment = [0, 0, 1, 1, 0, 0, 1, 1]    # 0 = vehicle, 1 = treatment
design = pd.DataFrame({
    "Samples": sample_cols,
    "baseline": [1] * 8,
    "batch2": batch,
    "treatment": treatment,
})
design.to_csv(OUT / "input4_design.txt", sep="\t", index=False)
print("Wrote input4_mle_counts.txt and input4_design.txt")
print(design.to_string(index=False))
