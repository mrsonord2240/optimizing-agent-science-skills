# Input 2 (NEW), part 2: read what PTXQC's completed report says about the 0.39x under-loaded run T4,
# and compare with the SKILL.md raw_sample_qc rule on the same txt/ folder.
import re, numpy as np, pandas as pd
from skill import S

hm = pd.read_csv('qc_failed/report_v1.1.5_qc_failed_heatmap.txt', sep='\t')
hm.columns = [re.sub(r'[\\"]|~\[\d+\]|EVD:|MSMS:|PG:', '', c).replace('~', ' ').strip() for c in hm.columns]
hm = hm.set_index(hm.columns[0])
print('--- PTXQC per-run scores from the completed report (1 = best) ---')
print(hm.round(3).to_string())
q = hm[hm.columns[-1]]
print('\nAverage Overall Quality, sorted worst first:')
print(q.sort_values().round(4).to_string())
print('T4 rank (1 = worst):', int(q.rank().loc["T4"]), 'of', len(q))
print('spread worst-to-best:', round(q.max() - q.min(), 4))

print('\n--- SKILL.md raw_sample_qc on the same evidence.txt (its own Level-1/3 rule) ---')
ev = pd.read_csv('qc_failed/evidence.txt', sep='\t', low_memory=False)
mat = ev.pivot_table(index='Sequence', columns='Raw file', values='Intensity', aggfunc='sum')
grp = pd.Series({s: ('Control' if s.startswith('C') else 'Treat') for s in mat.columns})
out = S['raw_sample_qc'](mat, grp)
print(out.round(3).to_string())
flag = [c for c in out.columns if 'flag' in c.lower() or 'investigate' in c.lower()]
print('\nflag columns:', flag)
