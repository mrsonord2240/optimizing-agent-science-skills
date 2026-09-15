"""Input 2 (Variant A) - after the Skill's filter (in1_skill_filter.py, same code), characterise what the global
protein-group filter removed and what the hand-off matrix looks like. Agent-written around the Skill's pattern."""
import os
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, '..'))
report = pd.read_parquet('data/report.parquet')

run_level = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)]
skill = run_level[run_level['Global.PG.Q.Value'] <= 0.01]          # the Skill's three-column filter
dropped = sorted(set(run_level['Protein.Group']) - set(skill['Protein.Group']))
runs_seen = run_level[run_level['Protein.Group'].isin(dropped)].groupby('Protein.Group')['Run'].nunique()
print('groups passing run-level filters:', run_level['Protein.Group'].nunique())
print('groups removed by Global.PG.Q.Value <= 0.01:', len(dropped), '| all LOWCONF*:', all(g.startswith('LOWCONF') for g in dropped))
print('runs in which the removed groups had passed run-level 1% PG FDR:', runs_seen.value_counts().sort_index().to_dict())
print('Global.PG.Q.Value of removed groups:', sorted(run_level.loc[run_level['Protein.Group'].isin(dropped), 'Global.PG.Q.Value'].unique()))

pg = skill.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')
zero_cells = int((pg == 0).sum().sum())
pg = np.log2(pg.replace(0, np.nan))
cond = np.where(pg.columns.str.startswith('C'), 'Control', 'Treatment')
valid = pg.notna().T.groupby(cond).sum().T
print('zero cells converted to NaN before log2:', zero_cells, '| -inf after log2:', int(np.isinf(pg.to_numpy()).sum()))
print('groups with >= 3 valid values in both conditions:', int(((valid >= 3).all(axis=1)).sum()), 'of', len(pg))
print('groups completely absent in one condition (candidate on/off, not imputable as MAR):',
      int(((valid == 0).any(axis=1)).sum()))
