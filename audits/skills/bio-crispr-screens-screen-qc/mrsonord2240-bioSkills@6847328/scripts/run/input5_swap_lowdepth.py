"""Input 5 -- Stress (regression). Planted faults: HAP1_T18B replaced with a jittered copy of
the plasmid-stage sample mislabeled as an endpoint replicate, plus HAP1_T18C down-sampled 50x.
Same data as the pre-fix audit's Input 5; functions unchanged by the fix -- no-regression
check."""
import sys
import pandas as pd, numpy as np
sys.path.insert(0, '.')
import qc_functions as qc

DATA = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_swap_lowdepth_fault.txt'
df = pd.read_csv(DATA, sep='\t')
counts = df[['HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']]

cmap = {'endpoint': ['HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']}
rc = qc.replicate_concordance(counts, cmap)
print('replicate concordance (endpoint):')
print(rc.round(4))

r_swap_vs_plasmid = qc.replicate_concordance(counts, {'x': ['HAP1_T0', 'HAP1_T18B']}).iloc[0]['pearson_log']
r_swap_vs_real = rc[(rc.rep1 == 'HAP1_T18A') & (rc.rep2 == 'HAP1_T18B')]['pearson_log'].values[0]
print(f'\nHAP1_T18B vs HAP1_T0 (plasmid)      pearson_log = {r_swap_vs_plasmid:.4f}')
print(f'HAP1_T18B vs HAP1_T18A (true rep)   pearson_log = {r_swap_vs_real:.4f}')

meta = pd.DataFrame({'stage': ['plasmid', 'endpoint', 'endpoint', 'endpoint']}, index=counts.columns)
pcs, evr = qc.screen_pca(counts, meta)
print('\nPCA (PC1, PC2):')
print(pcs[['PC1', 'PC2']].round(3))

da = qc.depth_audit(counts)
print('\ndepth audit:')
print(da[['reads_per_sgrna', 'depth_grade']].round(2))

swap_caught = r_swap_vs_plasmid > 0.95 and r_swap_vs_plasmid > r_swap_vs_real
lowdepth_caught = da.loc['HAP1_T18C', 'depth_grade'] == 'FAIL'
print(f'\nSwap fault caught (T18B correlates with plasmid, not real rep): {swap_caught}')
print(f'Low-depth fault caught (T18C depth FAIL): {lowdepth_caught}')
assert swap_caught and lowdepth_caught, 'REGRESSION: one or both planted faults no longer caught'
