import pandas as pd
ev = pd.read_csv('../data/evidence.txt', sep='\t', low_memory=False)
g = ev.groupby('Raw file').agg(n=('Sequence','size'), tot=('Intensity','sum'))
g['tot_rel'] = g['tot']/g['tot'].median(); g['n_rel'] = g['n']/g['n'].median()
print(g.round(3).to_string())
pg = pd.read_csv('../data/proteinGroups.txt', sep='\t', low_memory=False)
pgf = pd.read_csv('../data/proteinGroups_failed.txt', sep='\t', low_memory=False)
ic = [c for c in pgf.columns if c.startswith('Intensity ')]
s = pgf[ic].sum(); print('\nfailed pG raw Intensity rel to median:'); print((s/s.median()).round(3).to_string())
print('\nclean pG raw Intensity rel to median:'); s2 = pg[[c for c in pg.columns if c.startswith('Intensity ')]].sum(); print((s2/s2.median()).round(3).to_string())
hm = pd.read_csv('qc2/report_v1.1.5_qc2_heatmap.txt', sep='\t')
hm.columns = [c.replace('EVD.','').replace('MSMS.','').replace('..','.') for c in hm.columns]
print('\nPTXQC heatmap:'); print(hm.round(3).to_string(index=False))
