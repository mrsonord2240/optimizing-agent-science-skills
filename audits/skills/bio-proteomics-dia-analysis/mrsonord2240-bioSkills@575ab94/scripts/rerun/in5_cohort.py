'''DIA Input 5 (regression, stress): 600 plasma runs. Rebuild the pre-fix SYNTHETIC 600-run cohort report with its seeded
generator (written into rerun/cohort), then run block b03 verbatim and the per-run QC. Deletes the 140 MB parquet afterwards.'''
import os, time, runpy, shutil, numpy as np, pandas as pd
A = 'F:/OpenScience/audits/bio-proteomics-dia-analysis'
src = open(f'{A}/runs/in5_make_cohort.py', encoding='utf-8').read()
os.chdir(f'{A}/rerun/cohort')
g = {'__name__': '__main__', '__file__': f'{A}/rerun/cohort/gen/in5_make_cohort.py'}
exec(compile(src, 'in5_make_cohort.py', 'exec'), g)
os.makedirs('diann_out', exist_ok=True); pq = ['data/cohort600_report.parquet']
print('generated:', pq)
if not os.path.exists('diann_out/report.parquet'):
    shutil.move(pq[0], 'diann_out/report.parquet')
cols = pd.read_parquet('diann_out/report.parquet').columns.tolist()
print('columns:', cols)
t0 = time.time(); ns = {}
try:
    with open(f'{A}/rerun/blocks/b03_DIA_NN_Output_and_Correct_Filtering.py', encoding='utf-8') as fh:
        exec(fh.read(), ns)
    pg = ns['pg']
    print(f'Skill block: {time.time() - t0:.1f} s | matrix {pg.shape} | -inf {int(np.isinf(pg.values).sum())} | missing {100 * pg.isna().mean().mean():.1f}%')
    print('false (FALSE*) groups in matrix:', int(pg.index.str.startswith('FALSE').sum()))
    per = pg.notna().sum(); med, mad = per.median(), (per - per.median()).abs().median()
    print(f'per-run groups: median {med:.0f}, MAD {mad:.0f}, min {per.min()}, max {per.max()}, flagged (>3 MAD low): {int((per < med - 3 * 1.4826 * mad).sum())}')
except Exception as e:
    print('Skill block ->', type(e).__name__, e)
finally:
    shutil.rmtree('diann_out', ignore_errors=True); shutil.rmtree('data', ignore_errors=True)
