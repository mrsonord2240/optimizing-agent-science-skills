# Runs the Skill's documented per-animal meta-analysis (Stouffer's Z) on the
# 6 real mageck_out/animal_N.gene_summary.txt files produced by mageck test.
# Adapted directly from examples/per_animal_meta_analysis.py and the
# meta_analyze_animals() snippet in SKILL.md ("Per-animal RRA + meta-analysis").
import pandas as pd
import numpy as np
from scipy.stats import norm
from pathlib import Path
from statsmodels.stats.multitest import multipletests

animal_files = {f"animal_{i}": f"mageck_out/animal_{i}.gene_summary.txt" for i in range(1, 7)}

animal_dfs = {}
for animal, file in animal_files.items():
    if Path(file).exists():
        animal_dfs[animal] = pd.read_csv(file, sep="\t")

if not animal_dfs:
    raise FileNotFoundError("No per-animal MAGeCK results found")

all_results = pd.concat([df.assign(animal=name) for name, df in animal_dfs.items()])


def stouffer_meta(group):
    pvals = group["neg|p-value"].clip(lower=1e-10).values
    z_scores = -norm.ppf(pvals)
    combined_z = np.sum(z_scores) / np.sqrt(len(z_scores))
    combined_p = norm.sf(combined_z)
    return pd.Series(
        {
            "meta_z": combined_z,
            "meta_p": combined_p,
            "mean_neg_score": group["neg|score"].mean(),
            "median_neg_lfc": group["neg|lfc"].median(),
            "n_animals": len(group),
            "animals_at_fdr_05": (group["neg|fdr"] < 0.05).sum(),
        }
    )


meta = all_results.groupby("id").apply(stouffer_meta, include_groups=False).reset_index()
meta = meta.sort_values("meta_z", ascending=False)
meta["meta_fdr"] = multipletests(meta["meta_p"], method="fdr_bh")[1]

n_animals = len(animal_dfs)
hits = meta[(meta["meta_fdr"] < 0.05) & (meta["animals_at_fdr_05"] >= n_animals * 0.5)]

print(f"Total animals analyzed: {n_animals}")
print(f"Meta-significant hits (FDR<0.05 + >=50% animal consistency): {len(hits)}")
print(hits[["id", "meta_z", "meta_fdr", "mean_neg_score", "animals_at_fdr_05", "n_animals"]].to_string(index=False))

print("\nTop 10 by meta_z (for reference, regardless of FDR):")
print(meta[["id", "meta_z", "meta_p", "meta_fdr", "animals_at_fdr_05"]].head(10).to_string(index=False))

planted = {"Gene000", "Gene001", "Gene002", "Gene003", "Gene004"}
recovered = planted & set(hits["id"])
print(f"\nPlanted true hits: {sorted(planted)}")
print(f"Recovered as meta-significant: {sorted(recovered)} ({len(recovered)}/5)")

hits.to_csv("in_vivo_meta_hits.tsv", sep="\t", index=False)
meta.to_csv("in_vivo_meta_all.tsv", sep="\t", index=False)
