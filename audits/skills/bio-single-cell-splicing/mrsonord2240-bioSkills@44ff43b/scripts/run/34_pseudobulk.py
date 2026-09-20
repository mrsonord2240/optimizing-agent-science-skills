"""Input 7: SKILL's pseudobulk_junctions() (literal) on the SYNTHETIC planted junction matrix (marvel_planted_SJ.tsv, 200 events x 60 cells),
then a cluster-level PSI test from the pseudobulk. Also the default-RangeIndex trap."""
import numpy as np, pandas as pd
from scipy import stats
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
# ---- verbatim from SKILL.md
def pseudobulk_junctions(junction_counts, cell_metadata, groupby='cell_type'):
    out = {}
    for group, cells in cell_metadata.groupby(groupby).groups.items():
        mask = junction_counts.columns.isin(cells)
        out[group] = junction_counts.loc[:, mask].sum(axis=1)
    return pd.DataFrame(out)
# ----
J = pd.read_csv(f'{R}/data/marvel_planted_SJ.tsv', sep='\t', index_col=0)            # junctions x cells (SYNTHETIC)
truth = pd.read_csv(f'{R}/data/marvel_planted_truth.tsv', sep='\t', keep_default_na=False)
cells = list(J.columns); grp = ['A']*30+['B']*30
meta_ok = pd.DataFrame({'cell_type':grp}, index=cells)
pb = pseudobulk_junctions(J, meta_ok)
print('pseudobulk shape', pb.shape, 'column sums', pb.sum().to_dict(), ' == matrix total', int(J.values.sum()))
assert int(pb.values.sum()) == int(J.values.sum()); print('ASSERT OK: pseudobulk conserves counts when metadata index = cell ids')
# trap: metadata read from a table without index_col (RangeIndex) -- the usual pandas situation
meta_bad = pd.DataFrame({'cell':cells,'cell_type':grp})
pb_bad = pseudobulk_junctions(J, meta_bad)
print('RangeIndex metadata -> pseudobulk column sums', pb_bad.sum().to_dict(), '(silent zeros: no error, no warning)')
# cluster-level test: for each SE event, PSI_A vs PSI_B by Fisher on (inc,skip) pseudobulk counts
res=[]
for _,r in truth.iterrows():
    p=r.tran_id.split('@'); c=[x.split(':') for x in p]; chr_=c[0][0]
    if ':-@' in r.tran_id:  # minus strand listing order reversed
        e=[(int(x[1]),int(x[2])) for x in c][::-1]
    else:
        e=[(int(x[1]),int(x[2])) for x in c]
    j1=f'{chr_}:{e[0][1]+1}:{e[1][0]-1}'; j2=f'{chr_}:{e[1][1]+1}:{e[2][0]-1}'; js=f'{chr_}:{e[0][1]+1}:{e[2][0]-1}'
    inc=(pb.loc[j1]+pb.loc[j2])/2; sk=pb.loc[js]
    tab=[[inc['A'],sk['A']],[inc['B'],sk['B']]]
    tab=np.round(np.array(tab)).astype(int)
    _,p=stats.fisher_exact(tab)
    res.append((r.cls,p,inc['B']/(inc['B']+sk['B'])-inc['A']/(inc['A']+sk['A']), r.psiB-r.psiA))
d=pd.DataFrame(res,columns=['cls','p','dpsi_obs','dpsi_true'])
from statsmodels.stats.multitest import multipletests
d['fdr']=multipletests(d.p,method='fdr_bh')[1]
print(d.groupby('cls').agg(n=('p','size'),sig_fdr05=('fdr',lambda x:(x<.05).sum())))
print('direction agreement planted:', (np.sign(d.dpsi_obs)==np.sign(d.dpsi_true))[d.cls!='null'].mean())
print('NOTE: cell-level (PSI) tests on the same data: MARVEL wilcox big 40/40, mid 20/20, null 0/140 (see 28_marvel_planted.log)')
# naive Fisher on pseudobulk is anti-conservative under between-cell overdispersion?
print('null raw p<0.05 fraction (Fisher on pooled counts):', (d.p[d.cls=='null']<.05).mean().round(3), ' <- nominal 0.05; cells are beta-overdispersed (conc=20)')
