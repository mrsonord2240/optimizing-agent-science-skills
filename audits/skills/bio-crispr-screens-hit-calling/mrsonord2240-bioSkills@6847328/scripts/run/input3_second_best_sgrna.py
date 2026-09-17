'''Input 3 (Variant B, regression of pre-fix Input 3): "Apply the second-best-sgRNA
rule to my hit list to flag single-guide-driven false positives" -- MAGeCK
sgrna_summary.txt for real Tier-1 genes, PLUS a synthetic single-guide-gene
regression case for the P2 fix (silent single-guide fallback -> NaN + flag).
'''
import os, sys
import pandas as pd
import numpy as np

RUN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN)
os.chdir(RUN)
from lib_consensus_inline import second_best_lfc

sgrna = pd.read_csv('mageck_hap1.sgrna_summary.txt', sep='\t')
print(f'Loaded {len(sgrna)} sgRNA rows across {sgrna["Gene"].nunique()} genes')

# Part A: real TKOv3 data. The audit's pre-fix assumption ("TKOv3 is always 4
# guides/gene, so single-guide risk never triggers") turns out to be wrong on this
# real file -- most genes have 4 guides, but 231 genes have exactly 1 (likely
# QC-filtered/dropped guides upstream of this summary), which makes this an even
# better regression test than a purely synthetic one: the P2 fix is exercised by
# real data, not just a constructed example.
res = second_best_lfc(sgrna['LFC'], sgrna['Gene'], direction='neg')
n_single = int(res['single_guide'].sum())
n_multi = len(res) - n_single
print(f'\nPart A (real TKOv3 sgrna_summary.txt): {n_single} single-guide genes, '
      f'{n_multi} multi-guide genes, out of {len(res)} total')

single_rows = res[res['single_guide'] == True]
multi_rows = res[res['single_guide'] == False]
assert single_rows['second_best_lfc'].isna().all(), (
    'REGRESSION: real single-guide genes should return NaN, not a silent pass value')
assert multi_rows['second_best_lfc'].notna().all(), (
    'genes with >=2 guides should always get a real second-best LFC')
print('PASS (real data): all 231 real single-guide genes return NaN + single_guide=True, '
      'not their own LFC as a silent pass.')

# Confirm none of the 844 real Tier-1 consensus genes (Input 1) are single-guide-driven
# false "passes" -- cross-check against the real consensus list.
import subprocess, sys as _sys
tier1_genes = set(pd.read_csv('consensus_hits.csv')['gene']) if __import__('os').path.exists('consensus_hits.csv') else set()
if tier1_genes:
    tier1_single = tier1_genes & set(single_rows['gene'])
    print(f'Tier-1 consensus genes (from Input 1) that are single-guide in this library: {len(tier1_single)}')

# Part B: synthetic single-guide-gene regression test for the P2 fix.
# Build a tiny synthetic library: 3 genes with 3 guides each (real 3 guides, real LFCs
# subsampled from the real data) plus 1 gene with exactly 1 guide.
synthetic_lfc = pd.concat([
    sgrna[sgrna['Gene'] == 'POLR2L']['LFC'].reset_index(drop=True),
    sgrna[sgrna['Gene'] == 'EIF3A']['LFC'].reset_index(drop=True),
    sgrna[sgrna['Gene'] == 'GTPBP10']['LFC'].reset_index(drop=True),
    pd.Series([sgrna[sgrna['Gene'] == 'PES1']['LFC'].astype(float).iloc[0]]),
], ignore_index=True)
synthetic_genes = pd.Series(
    ['MULTI_A'] * (sgrna['Gene'] == 'POLR2L').sum() +
    ['MULTI_B'] * (sgrna['Gene'] == 'EIF3A').sum() +
    ['MULTI_C'] * (sgrna['Gene'] == 'GTPBP10').sum() +
    ['SINGLE_D']
)
synthetic_lfc = synthetic_lfc.astype(float)
res_b = second_best_lfc(synthetic_lfc, synthetic_genes, direction='neg')
print('\nPart B (synthetic library, one 1-guide gene "SINGLE_D"):')
print(res_b.to_string(index=False))

single_row = res_b[res_b['gene'] == 'SINGLE_D'].iloc[0]
assert single_row['single_guide'] == True, 'SINGLE_D should be flagged single_guide=True'
assert pd.isna(single_row['second_best_lfc']), (
    'REGRESSION: SINGLE_D should return NaN, not silently fall back to its own LFC '
    'as a passing value (the pre-fix defect)')
print('\nPASS: single-guide gene returns NaN + single_guide=True, not a silent pass.')

multi_rows = res_b[res_b['gene'] != 'SINGLE_D']
assert multi_rows['single_guide'].eq(False).all()
assert multi_rows['second_best_lfc'].notna().all()
print('PASS: multi-guide genes still get a real second-best LFC (no regression).')
