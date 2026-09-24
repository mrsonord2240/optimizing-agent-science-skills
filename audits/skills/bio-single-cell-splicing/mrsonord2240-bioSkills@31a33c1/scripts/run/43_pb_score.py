"""INPUT 5: score leafcutter output from S14 against planted cluster truth; compare with the pooled n=1 (one pseudobulk per cell type) Fisher approach the Skill warns against."""
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'; D = f'{R}/data/pb_v2'
truth = pd.read_csv(f'{D}/truth.tsv', sep='\t', keep_default_na=False)
s = pd.read_csv(f'{R}/out/in5/pb_ds_cluster_significance.txt', sep='\t'); s['clu'] = s.cluster.str.split(':').str[-1]
s = s.merge(truth, left_on='clu', right_on='cluster'); t = s[s.status == 'Success']
print('clusters tested', len(t), 'of', len(truth), '; status counts', s.status.value_counts().to_dict())
print(t.groupby('cls').agg(n=('p', 'size'), p05=('p', lambda x: int((x < .05).sum())), fdr05=('p.adjust', lambda x: int((x < .05).sum()))).to_string())
eff = pd.read_csv(f'{R}/out/in5/pb_ds_effect_sizes.txt', sep='\t'); print('effect-size file columns:', list(eff.columns)); eff['clu'] = eff.intron.str.split(':').str[-1]
# direction: the skipping junction (3rd, longest) deltapsi; inclusion junctions negative of it. planted dPSI_incl = psi_T2 - psi_T1 ; leafcutter groups sorted alphabetically (T1, T2): deltapsi = T2 - T1 (per its output)
eff = eff.merge(truth, left_on='clu', right_on='cluster'); eff['len'] = eff.intron.str.split(':').str[2].astype(int) - eff.intron.str.split(':').str[1].astype(int)
skip = eff.loc[eff.groupby('clu').len.idxmax()]; skip = skip[skip.cls != 'null']; skip = skip[skip.clu.isin(t[(t['p.adjust'] < .05) & (t.cls != 'null')].clu)]
print('direction: sign(deltapsi of skip junction) == -sign(planted dPSI_incl T2-T1) among planted hits:', (np.sign(skip.deltapsi) == -np.sign(skip.psi_T2 - skip.psi_T1)).mean().round(3), 'n', len(skip))
# independent second method: Fisher on the pooled counts of the same pseudobulks, n=1 per type (what the SKILL says NOT to do)
pb = pd.read_csv(f'{R}/out/in5/pb_counts.txt.gz', sep=' ', index_col=0); g = pd.read_csv(f'{R}/out/in5/pb_groups.txt', sep='\t', header=None, names=['sample', 'group'])
ps = []
for i, r in truth.iterrows():
    rows = [x for x in pb.index if x.endswith(r.cluster)]; inc = pb.loc[rows[:2]].sum(0) / 2; sk = pb.loc[rows[2]]
    T1 = [c for c in pb.columns if c.startswith('T1')]; T2 = [c for c in pb.columns if c.startswith('T2')]
    tab = np.round([[inc[T1].sum(), sk[T1].sum()], [inc[T2].sum(), sk[T2].sum()]]).astype(int); ps.append(stats.fisher_exact(tab)[1])
truth['p_pool'] = ps; truth['fdr_pool'] = multipletests(ps, method='fdr_bh')[1]
print('POOLED n=1 vs n=1 Fisher:'); print(truth.groupby('cls').agg(n=('p_pool', 'size'), p05=('p_pool', lambda x: int((x < .05).sum())), fdr05=('fdr_pool', lambda x: int((x < .05).sum()))).to_string())
assert (t[t.cls == 'big']['p.adjust'] < .05).mean() >= .8
print('ASSERT OK: leafcutter on replicate pseudobulks detects >=80% of big planted events')
