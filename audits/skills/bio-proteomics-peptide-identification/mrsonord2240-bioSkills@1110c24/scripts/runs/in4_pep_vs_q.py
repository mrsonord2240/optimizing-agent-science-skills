# Input 4 - PEP vs q-value, using the Skill's shipped example functions (add_qvalues, add_pep) on the SYNTHETIC
# rank-1 Comet table, plus a ground-truth check of the example's own demo table.
import sys
sys.dont_write_bytecode = True           # never write __pycache__ into the read-only external clone
sys.path.insert(0, 'F:/OpenScience/external/GPTomics__bioSkills/proteomics/peptide-identification/examples')
import numpy as np
import pandas as pd
import fdr_filtering as ex

D = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/'

# --- 1. the user's (synthetic) data: rank-1 PSMs of a concatenated search
c = pd.read_csv(D + 'comet_concat.txt', sep='\t')
c = c[c['num'] == 1].rename(columns={'xcorr': 'score'})
p = ex.add_pep(ex.add_qvalues(c))
acc_q = p[(p['qvalue'] <= 0.01) & ~p['is_decoy']]
acc_pep = p[(p['pep'] <= 0.01) & ~p['is_decoy']]
print(f'q<=0.01 : {len(acc_q)} PSMs, true FDP {1 - acc_q["is_correct"].mean():.4f}, mean PEP of accepted {acc_q["pep"].mean():.4f}, worst PEP {acc_q["pep"].max():.3f}')
print(f'PEP<=0.01: {len(acc_pep)} PSMs, true FDP {1 - acc_pep["is_correct"].mean():.4f}')
for lo, hi in [(0.0, 0.01), (0.01, 0.05), (0.05, 0.2), (0.2, 1.01)]:
    b = acc_q[(acc_q['pep'] >= lo) & (acc_q['pep'] < hi)]
    if len(b):
        print(f'   accepted with PEP in [{lo},{hi}): n={len(b):>5}  observed wrong fraction={1 - b["is_correct"].mean():.3f}')
# the last 100 accepted PSMs (lowest scores inside the 1% list): true local error rate
tail = acc_q.sort_values('score').head(100)
print(f'lowest-scoring 100 accepted PSMs: mean PEP {tail["pep"].mean():.3f}, observed wrong fraction {1 - tail["is_correct"].mean():.3f}')

# --- 2. the shipped example's demo table, with its hidden ground truth restored
demo = ex.build_demo_table()
demo['truth_true'] = [True] * 1000 + [False] * 1000 + [False] * 2000
dq = ex.add_qvalues(demo)
kept = dq[(dq['qvalue'] <= 0.01) & ~dq['is_decoy']]
print(f'example demo: kept {len(kept)} at q<=0.01, true FDP {1 - kept["truth_true"].mean():.4f} '
      f'(rows are independent: 1000 null targets vs 2000 decoys, no per-spectrum competition)')
# what q would a correct null count give? decoys/2 estimate the 1000 null targets here
s = dq.sort_values('score', ascending=False)
t = (~s['is_decoy']).cumsum(); d = s['is_decoy'].cumsum()
q_half = ((d * 0.5) / t)[::-1].cummin()[::-1]
k2 = s[(q_half <= 0.01) & ~s['is_decoy']]
print(f'   same table with decoys scaled to the null-target count (x0.5): kept {len(k2)}, true FDP {1 - k2["truth_true"].mean():.4f}')
