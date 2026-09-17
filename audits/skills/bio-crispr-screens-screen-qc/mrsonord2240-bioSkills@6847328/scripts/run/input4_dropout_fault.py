"""Input 4 -- Edge (regression). Planted fault: 8% guide dropout in HAP1_T18B. Same data as
the pre-fix audit's Input 4 (functions unchanged by the fix, so this is a pure no-regression
check)."""
import sys
import pandas as pd, numpy as np
sys.path.insert(0, '.')
import qc_functions as qc

DATA = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_dropout_fault.txt'
df = pd.read_csv(DATA, sep='\t')
counts = df[['HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']]

lr = qc.library_representation(counts)
print('pct_zero:')
print(lr['pct_zero'].round(2))

da = qc.depth_audit(counts)
print('\ndepth audit:')
print(da.round(2))

thr = qc.stage_specific_thresholds()['endpoint']['pct_zero_max']
caught = bool(lr.loc['HAP1_T18B', 'pct_zero'] > thr and da.loc['HAP1_T18B', 'depth_grade'] == 'FAIL')
print(f'\nendpoint pct_zero_max={thr}%')
print('Planted dropout fault in HAP1_T18B caught by QC thresholds:', caught)
assert caught, 'REGRESSION: planted dropout fault no longer caught'
