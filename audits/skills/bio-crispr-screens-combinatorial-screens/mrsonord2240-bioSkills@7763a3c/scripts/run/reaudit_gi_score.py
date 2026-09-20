"""
Re-auditor's independent verification of the fixed gi_score() function in
crispr-screens/combinatorial-screens/SKILL.md (fix commit 7763a3c).

Fresh synthetic dataset (different seed, different gene set, different pair
count than either the original auditor's or the fixer's data) to avoid
reusing anyone else's fixture.
"""
import numpy as np
import pandas as pd
from scipy.stats import zscore

rng = np.random.default_rng(20260919)

# 150 gene pairs, disjoint gene pool from prior runs (RA_ prefix = "re-audit")
genes = [f"RA_{i:03d}" for i in range(1, 301)]
pairs = [(genes[2 * i], genes[2 * i + 1]) for i in range(150)]

# Plant 6 synthetic-lethal pairs (strong negative GI) and 3 synthetic-rescue
# pairs (strong positive GI); rest additive + noise.
sl_idx = [3, 17, 42, 88, 101, 133]
sr_idx = [9, 55, 120]

single_rows = []
for g in genes:
    single_rows.append({"gene": g, "lfc": rng.normal(-0.3, 0.4)})
single_df = pd.DataFrame(single_rows)
single_lookup = dict(zip(single_df["gene"], single_df["lfc"]))

paired_rows = []
for idx, (a, b) in enumerate(pairs):
    expected = single_lookup[a] + single_lookup[b]
    if idx in sl_idx:
        # planted strong synthetic-lethal: much more depleted than additive
        gi_true = rng.normal(-3.0, 0.2)
    elif idx in sr_idx:
        gi_true = rng.normal(3.0, 0.2)
    else:
        gi_true = rng.normal(0.0, 0.5)
    observed = expected + gi_true
    for cassette in range(4):  # 4 cassettes per pair, small per-cassette noise
        paired_rows.append({
            "cassette_id": f"{a}_{b}_c{cassette}",
            "gene_A": a,
            "gene_B": b,
            "lfc": observed + rng.normal(0, 0.15),
        })
paired_df = pd.DataFrame(paired_rows)

paired_df.to_csv("paired_lfc.tsv", sep="\t", index=False)
single_df.to_csv("single_lfc.tsv", sep="\t", index=False)

print("=== File format written (matches SKILL.md's documented tsv format) ===")
print("paired_lfc.tsv columns:", list(paired_df.columns))
print("single_lfc.tsv columns:", list(single_df.columns))

# ---------------------------------------------------------------------
# gi_score() copied VERBATIM from the fixed SKILL.md (commit 7763a3c)
# ---------------------------------------------------------------------
def gi_score(paired_lfc_df, single_lfc_df):
    '''Score genetic interactions from paired vs single LFCs.

    paired_lfc_df: rows = paired-KO; columns = ['gene_A', 'gene_B', 'lfc']
    single_lfc_df: rows = single-KO; columns = ['gene', 'lfc']
    (both files use the same 'lfc' column name -- see examples/gi_scoring.py)
    '''
    single = dict(zip(single_lfc_df['gene'], single_lfc_df['lfc']))
    df = paired_lfc_df.copy()
    df['single_A_lfc'] = df['gene_A'].map(single)
    df['single_B_lfc'] = df['gene_B'].map(single)
    df['expected_additive'] = df['single_A_lfc'] + df['single_B_lfc']
    df['gi_score'] = df['lfc'] - df['expected_additive']
    df = df.dropna(subset=['gi_score'])          # a single missing singleton would NaN every z-score
    df['gi_z'] = zscore(df['gi_score'])
    df['gi_class'] = np.where(df['gi_z'] < -2, 'synthetic_lethal',
                                np.where(df['gi_z'] > 2, 'synthetic_rescue', 'no_interaction'))
    return df.sort_values('gi_z')

# --- Aggregate cassette-level to pair-level first (as examples/gi_scoring.py does) ---
pair_lfc = paired_df.groupby(['gene_A', 'gene_B']).agg(lfc=('lfc', 'mean')).reset_index()

# Reload straight from the tsv files as a downstream user would, to test the
# documented function against the documented file format with zero
# translation -- this is the exact claim under test (Input 1's original
# P1: "KeyError('paired_lfc')" when applied verbatim).
reloaded_paired = pd.read_csv("paired_lfc.tsv", sep="\t")
reloaded_single = pd.read_csv("single_lfc.tsv", sep="\t")
reloaded_pair_lfc = reloaded_paired.groupby(['gene_A', 'gene_B']).agg(lfc=('lfc', 'mean')).reset_index()

try:
    result = gi_score(reloaded_pair_lfc, reloaded_single)
    print("\n=== gi_score() executed with NO KeyError on the documented file format ===")
except KeyError as e:
    print(f"\n=== FAIL: KeyError still present: {e} ===")
    raise

print(f"Total pairs scored: {len(result)}")

recovered_sl = 0
for idx in sl_idx:
    a, b = pairs[idx]
    row = result[(result['gene_A'] == a) & (result['gene_B'] == b)]
    cls = row['gi_class'].iloc[0] if len(row) else None
    z = row['gi_z'].iloc[0] if len(row) else None
    ok = cls == 'synthetic_lethal'
    recovered_sl += ok
    print(f"planted SL {a}/{b}: gi_z={z:.3f} class={cls} {'OK' if ok else 'MISSED'}")

recovered_sr = 0
for idx in sr_idx:
    a, b = pairs[idx]
    row = result[(result['gene_A'] == a) & (result['gene_B'] == b)]
    cls = row['gi_class'].iloc[0] if len(row) else None
    z = row['gi_z'].iloc[0] if len(row) else None
    ok = cls == 'synthetic_rescue'
    recovered_sr += ok
    print(f"planted rescue {a}/{b}: gi_z={z:.3f} class={cls} {'OK' if ok else 'MISSED'}")

n_false_pos = ((result['gi_class'] != 'no_interaction')).sum() - recovered_sl - recovered_sr
print(f"\nRecovered {recovered_sl}/{len(sl_idx)} planted synthetic-lethal pairs")
print(f"Recovered {recovered_sr}/{len(sr_idx)} planted synthetic-rescue pairs")
print(f"Other pairs classified as interacting (false positives): {n_false_pos}")
