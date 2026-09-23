"""Input 8 (fresh Edge): validate the documented --reffile output contract and
the same-ID/wrong-efficacy warning using fresh executions on example-small."""
import os
import sys
import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks")
from jacks.jacks_io import runJACKS

EX = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out8"
os.makedirs(OUT, exist_ok=True)
base_prior = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1\whp_false_canonical_grna_JACKS_results.txt"
prior = pd.read_csv(base_prior, sep="\t")[["sgrna", "X1", "X2"]]
prior_path = os.path.join(OUT, "matched_prior.tsv")
prior.to_csv(prior_path, sep="\t", index=False)
common = dict(countfile=os.path.join(EX, "example_count_data.tab"),
              replicatefile=os.path.join(EX, "example_repmap.tab"),
              guidemappingfile=os.path.join(EX, "example_count_data.tab"),
              rep_hdr="Replicate", sample_hdr="Sample", common_ctrl_sample="CTRL",
              sgrna_hdr="sgRNA", gene_hdr="Gene", apply_w_hp=False)

matched = os.path.join(OUT, "matched")
runJACKS(outprefix=matched, reffile=prior_path, **common)
gene = pd.read_csv(matched + "_gene_JACKS_results.txt", sep="\t")
lfc = [matched + "_logfoldchange_means.txt", matched + "_logfoldchange_std.txt"]
print(f"matched reffile run genes={len(gene)}")
print(f"logfoldchange files absent with --reffile: {[not os.path.exists(p) for p in lfc]}")
assert len(gene) == 1579
assert all(not os.path.exists(p) for p in lfc)

# The Skill says IDs alone are insufficient. Alter values while preserving every ID.
scrambled = prior.copy()
scrambled[["X1", "X2"]] = prior[["X1", "X2"]].sample(frac=1, random_state=23).to_numpy()
scrambled_path = os.path.join(OUT, "same_ids_scrambled_values.tsv")
scrambled.to_csv(scrambled_path, sep="\t", index=False)
wrong = os.path.join(OUT, "same_ids_wrong_values")
runJACKS(outprefix=wrong, reffile=scrambled_path, **common)
wrong_gene = pd.read_csv(wrong + "_gene_JACKS_results.txt", sep="\t")
cols = [c for c in gene.columns if c != "Gene"]
joined = gene.merge(wrong_gene, on="Gene", suffixes=("_matched", "_wrong"))
max_diff = max((joined[f"{c}_matched"] - joined[f"{c}_wrong"]).abs().max() for c in cols)
changed = sum((joined[f"{c}_matched"] - joined[f"{c}_wrong"]).abs().gt(0.1).sum() for c in cols)
print(f"same-ID scrambled reffile accepted; effect cells differing >0.1: {changed}; max_abs_diff={max_diff:.3f}")
assert changed > 0 and max_diff > 0.1
