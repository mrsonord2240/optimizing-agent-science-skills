"""Fresh execution of the SKILL.md in4mer pair-aggregation helper."""
from __future__ import annotations

import pandas as pd

paired_counts_df = pd.DataFrame({
    "cassette_id": ["A1", "A2", "B1", "B2"],
    "endpoint_lfc": [-1.1, -0.9, -0.2, -0.4],
    "day0_count": [101, 99, 103, 97],
})
gene_pairs = pd.DataFrame({
    "cassette_id": ["A1", "A2", "B1", "B2"],
    "gene_A": ["MAPK1", "MAPK1", "AKT1", "AKT1"],
    "gene_B": ["MAPK3", "MAPK3", "AKT2", "AKT2"],
})

def in4mer_pair_analysis(paired_counts_df, gene_pairs, value_cols):
    merged = paired_counts_df.merge(gene_pairs, on="cassette_id")
    return merged.groupby(["gene_A", "gene_B"])[value_cols].agg(["mean", "std", "count"])

result = in4mer_pair_analysis(paired_counts_df, gene_pairs, ["endpoint_lfc", "day0_count"])
print(result.to_string())
assert result.shape == (2, 6)
assert result.loc[("MAPK1", "MAPK3"), ("endpoint_lfc", "count")] == 2
assert result.loc[("MAPK1", "MAPK3"), ("endpoint_lfc", "mean")] == -1.0
print("ASSERT PASS: two-pair aggregation preserves correct mean, standard deviation, and replicate count.")
