"""Input 3 add-on: raw_sample_qc exactly as written (zeros left in, as MaxQuant ships them) on proteinGroups_failed.txt."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *
D = os.path.join(os.path.dirname(__file__), '..', 'data')
S = ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4']
pg = strip_contaminant_rows(pd.read_csv(os.path.join(D, 'proteinGroups_failed.txt'), sep='\t', low_memory=False))
for prefix in ['LFQ intensity', 'Intensity']:
    m = pg[[f'{prefix} {s}' for s in S]]; m.columns = S
    q = raw_sample_qc(m)
    q['fold_total_vs_median'] = q['total_signal'] / q['total_signal'].median()
    q['fold_median_vs_median'] = q['median_intensity'] / q['median_intensity'].median()
    print(f'--- {prefix}, zeros left in (as written) ---'); print(q.round(3).to_string())
