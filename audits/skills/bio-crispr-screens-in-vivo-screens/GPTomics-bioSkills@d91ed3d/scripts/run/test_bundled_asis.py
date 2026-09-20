# Test the bundled examples/per_animal_meta_analysis.py's exact groupby().apply() call
# (without include_groups=False) against pandas 3.0.5 installed in this env, to check
# if the shipped example as-written actually runs.
import pandas as pd
import numpy as np
from scipy.stats import norm
from pathlib import Path

animal_files = {f"animal_{i}": f"mageck_out/animal_{i}.gene_summary.txt" for i in range(1, 7)}
animal_dfs = {a: pd.read_csv(f, sep="\t") for a, f in animal_files.items() if Path(f).exists()}
all_results = pd.concat([df.assign(animal=name) for name, df in animal_dfs.items()])

def stouffer_meta(group):
    pvals = group['neg|p-value'].clip(lower=1e-10).values
    z_scores = -norm.ppf(pvals)
    combined_z = np.sum(z_scores) / np.sqrt(len(z_scores))
    combined_p = norm.sf(combined_z)
    return pd.Series({
        'meta_z': combined_z, 'meta_p': combined_p,
        'mean_neg_score': group['neg|score'].mean(),
        'median_neg_lfc': group['neg|lfc'].median(),
        'n_animals': len(group),
        'animals_at_fdr_05': (group['neg|fdr'] < 0.05).sum(),
    })

# EXACT bundled call -- no include_groups=False
meta = all_results.groupby('id').apply(stouffer_meta).reset_index()
print("Ran without error. Shape:", meta.shape)
print(meta.head(3))
