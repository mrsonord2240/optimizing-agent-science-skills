'''DIA Inputs 1-2 (regression): filter block b03 executed verbatim on the SYNTHETIC DIA-NN 1.9-style report (60 LOWCONF groups
fail Global.PG.Q.Value). Then what the filter removed.'''
import os, warnings, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-dia-analysis/rerun/work')
warnings.simplefilter('always'); ns = {}
with warnings.catch_warnings(record=True) as w:
    with open('../blocks/b03_DIA_NN_Output_and_Correct_Filtering.py', encoding='utf-8') as fh:
        exec(fh.read(), ns)
    print('warnings:', [str(x.message) for x in w])
rep, filt, pg = ns['report'], ns['filt'], ns['pg']
print(f'report rows {len(rep)} | runs {rep["Run"].nunique()} | groups {rep["Protein.Group"].nunique()}')
print(f'filtered rows {len(filt)} | matrix {pg.shape} | -inf {int(np.isinf(pg.values).sum())} | NaN cells {int(pg.isna().sum().sum())} ({100*pg.isna().mean().mean():.1f}%)')
lvl = rep[(rep['Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01)]
print('run-level-only groups:', lvl['Protein.Group'].nunique(), '| LOWCONF surviving run-level-only:', lvl.loc[lvl['Protein.Group'].str.startswith('LOWCONF'), 'Protein.Group'].nunique(),
      '| LOWCONF surviving Skill filter:', int(pg.index.str.startswith('LOWCONF').sum()))
print('rows removed by Global.Q.Value only (beyond the other three):', int(((rep['Q.Value'] <= 0.01) & (rep['PG.Q.Value'] <= 0.01) & (rep['Global.PG.Q.Value'] <= 0.01) & (rep['Global.Q.Value'] > 0.01)).sum()))
cond = np.array(['Control' if r.startswith('C') else 'Treatment' for r in pg.columns])
v = pd.DataFrame({c: pg.loc[:, cond == c].notna().sum(axis=1) for c in ['Control', 'Treatment']})
print('groups >=3 valid in both conditions:', int(((v >= 3).all(axis=1)).sum()), 'of', len(pg), '| absent in one condition:', int(((v == 0).any(axis=1)).sum()))
print('per-run protein groups:', pg.notna().sum().to_dict())
