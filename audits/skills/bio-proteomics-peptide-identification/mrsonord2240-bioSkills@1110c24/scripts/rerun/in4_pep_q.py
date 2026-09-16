# Re-audit 2026-09-15, Input 4 (Variant B, regression). Shipped examples/fdr_filtering.py from the fork (imported
# read-only, no bytecode) run as-is; its add_qvalues/add_pep on the rank-1 Comet table; demo calibration over seeds.
import sys, runpy, io, contextlib
sys.dont_write_bytecode = True
EX = 'F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/peptide-identification/examples'
sys.path.insert(0, EX)
import numpy as np, pandas as pd
import fdr_filtering as ex

print('--- example main() ---')
ex.main()

c = pd.read_csv('../data/comet_concat.txt', sep='\t').rename(columns={'xcorr': 'score'})
p = ex.add_pep(ex.add_qvalues(c))          # add_qvalues does the rank-1 dedup itself
acc_q = p[(p.qvalue <= 0.01) & ~p.is_decoy]; acc_pep = p[(p.pep <= 0.01) & ~p.is_decoy]
print(f'\nq<=0.01 : {len(acc_q)} PSMs, true FDP {1 - acc_q.is_correct.mean():.4f}, worst PEP {acc_q.pep.max():.3f}')
print(f'PEP<=0.01: {len(acc_pep)} PSMs, true FDP {1 - acc_pep.is_correct.mean():.4f}')
tail = acc_q.sort_values('score').head(100)
print(f'lowest-scoring 100 accepted: mean PEP {tail.pep.mean():.3f}, observed wrong {1 - tail.is_correct.mean():.3f}')

fdps = []
for seed in range(10):
    d = ex.add_qvalues(ex.build_demo_table(seed=seed))
    k = d[(d.qvalue <= 0.01) & ~d.is_decoy]
    fdps.append((len(k), int((~k.is_true).sum())))
print('demo seeds 0-9 (kept, false):', fdps)
print('pooled demo FDP:', round(sum(f for _, f in fdps) / sum(n for n, _ in fdps), 4))
