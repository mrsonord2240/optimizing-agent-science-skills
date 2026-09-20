"""
Re-auditor's independent regression test of Input 3 (small-N edge case):
does the documented z<-2 cutoff miss real planted interactions at low pair
count, and does that remain an open, undisclosed gap (disputed P2 #2)?

Fresh 9-pair dataset (different from both the original auditor's 8-pair set
and the fixer's), 2 planted strong synthetic-lethal pairs.
"""
import numpy as np
import pandas as pd
from scipy.stats import zscore

rng = np.random.default_rng(55221)

genes = [f"SN_{i:02d}" for i in range(1, 19)]
pairs = [(genes[2 * i], genes[2 * i + 1]) for i in range(9)]
sl_idx = [2, 6]  # 2 planted strong SL pairs out of 9

single_lookup = {g: rng.normal(-0.2, 0.3) for g in genes}
rows = []
for idx, (a, b) in enumerate(pairs):
    expected = single_lookup[a] + single_lookup[b]
    gi_true = rng.normal(-2.5, 0.15) if idx in sl_idx else rng.normal(0.0, 0.4)
    rows.append({"gene_A": a, "gene_B": b, "lfc": expected + gi_true})
paired_df = pd.DataFrame(rows)
single_df = pd.DataFrame([{"gene": g, "lfc": v} for g, v in single_lookup.items()])

def gi_score(paired_lfc_df, single_lfc_df):
    single = dict(zip(single_lfc_df['gene'], single_lfc_df['lfc']))
    df = paired_lfc_df.copy()
    df['single_A_lfc'] = df['gene_A'].map(single)
    df['single_B_lfc'] = df['gene_B'].map(single)
    df['expected_additive'] = df['single_A_lfc'] + df['single_B_lfc']
    df['gi_score'] = df['lfc'] - df['expected_additive']
    df = df.dropna(subset=['gi_score'])
    df['gi_z'] = zscore(df['gi_score'])
    df['gi_class'] = np.where(df['gi_z'] < -2, 'synthetic_lethal',
                                np.where(df['gi_z'] > 2, 'synthetic_rescue', 'no_interaction'))
    return df.sort_values('gi_z')

result = gi_score(paired_df, single_df)
print(result[['gene_A', 'gene_B', 'gi_score', 'gi_z', 'gi_class']].to_string(index=False))

print("\nPlanted SL pairs:")
for idx in sl_idx:
    a, b = pairs[idx]
    row = result[(result['gene_A'] == a) & (result['gene_B'] == b)]
    print(f"  {a}/{b}: gi_z={row['gi_z'].iloc[0]:.3f} class={row['gi_class'].iloc[0]}")

n_missed = sum(
    result[(result['gene_A'] == pairs[i][0]) & (result['gene_B'] == pairs[i][1])]['gi_class'].iloc[0] != 'synthetic_lethal'
    for i in sl_idx
)
print(f"\nPlanted SL pairs MISSED by the documented z<-2 cutoff at N=9: {n_missed}/{len(sl_idx)}")
print("Rank by raw gi_score (most negative first) -- would raw-effect-size ranking have caught them instead?")
print(result.sort_values('gi_score')[['gene_A', 'gene_B', 'gi_score']].head(4).to_string(index=False))
