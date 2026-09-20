"""
Input 1 (Canonical), genome-scale-representative run.
Combines the Skill's examples/gi_scoring.py aggregation pattern with the
SKILL.md gi_score() z-normalization/classification logic, on the 200-pair
synthetic dataset.
"""
import pandas as pd
import numpy as np
from scipy.stats import zscore

paired_raw = pd.read_csv('paired_lfc_genome.tsv', sep='\t')
single_raw = pd.read_csv('single_lfc_genome.tsv', sep='\t')
single_lookup = dict(zip(single_raw['gene'], single_raw['lfc']))

pair_lfc = paired_raw.groupby(['gene_A', 'gene_B']).agg(
    paired_lfc_mean=('lfc', 'mean'),
    n_cassettes=('lfc', 'count'),
).reset_index()

pair_lfc['single_A_lfc'] = pair_lfc['gene_A'].map(single_lookup)
pair_lfc['single_B_lfc'] = pair_lfc['gene_B'].map(single_lookup)
pair_lfc['expected_additive'] = pair_lfc['single_A_lfc'] + pair_lfc['single_B_lfc']
pair_lfc = pair_lfc.dropna(subset=['single_A_lfc', 'single_B_lfc'])
pair_lfc['gi_score'] = pair_lfc['paired_lfc_mean'] - pair_lfc['expected_additive']
pair_lfc['gi_z'] = zscore(pair_lfc['gi_score'])
pair_lfc['gi_class'] = np.where(pair_lfc['gi_z'] < -2, 'synthetic_lethal',
                                 np.where(pair_lfc['gi_z'] > 2, 'synthetic_rescue', 'no_interaction'))

pair_lfc.to_csv('gi_scores_genome.tsv', sep='\t', index=False)

sl = pair_lfc[pair_lfc['gi_class'] == 'synthetic_lethal'].sort_values('gi_z')
sr = pair_lfc[pair_lfc['gi_class'] == 'synthetic_rescue'].sort_values('gi_z', ascending=False)

print(f"Total pairs: {len(pair_lfc)}")
print(f"Synthetic-lethal called (z<-2): {len(sl)}")
print(sl[['gene_A', 'gene_B', 'gi_score', 'gi_z']].to_string(index=False))
print(f"\nSynthetic-rescue called (z>2): {len(sr)}")
print(sr[['gene_A', 'gene_B', 'gi_score', 'gi_z']].to_string(index=False))

planted_sl = {(f"G{i:04d}", f"G{i+1:04d}") for i in range(1, 16, 2)}
called_sl = set(zip(sl['gene_A'], sl['gene_B']))
print(f"\nPlanted SL pairs recovered: {len(planted_sl & called_sl)}/{len(planted_sl)}")
print(f"False-positive SL calls (not planted): {len(called_sl - planted_sl)}")
