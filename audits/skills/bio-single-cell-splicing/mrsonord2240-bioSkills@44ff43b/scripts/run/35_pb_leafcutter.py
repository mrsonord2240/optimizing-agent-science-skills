"""Input 7b: pseudobulk -> leafcutter. (a) the Skill's own pseudobulk_junctions() output (ONE pseudobulk per cell type, i.e. n=1 vs n=1);
(b) replicate pseudobulks (5 random cell subsets per group). Writes leafcutter count tables + groups for leafcutter_ds.R (SYNTHETIC input)."""
import numpy as np, pandas as pd, gzip, os
R='/mnt/openscience/audits/bio-single-cell-splicing/run'; O=f'{R}/out/pb_lc'; os.makedirs(O,exist_ok=True)
J = pd.read_csv(f'{R}/data/marvel_planted_SJ.tsv', sep='\t', index_col=0)
truth = pd.read_csv(f'{R}/data/marvel_planted_truth.tsv', sep='\t', keep_default_na=False)
cells=list(J.columns); grp=np.array(['A']*30+['B']*30)
def name_rows(idx):
    out=[]; 
    for k,j in enumerate(idx):
        i=k%200   # J rows order: j1(200), j2(200), js(200)
        out.append(f'{j}:clu_{i+1}_+')
    return out
def write(df, path):
    df=df.copy(); df.index=name_rows(df.index)
    with gzip.open(path,'wt') as f: df.to_csv(f,sep=' ')
# (a) n=1 vs 1
pa=pd.DataFrame({'A':J.loc[:,grp=='A'].sum(1),'B':J.loc[:,grp=='B'].sum(1)}); write(pa,f'{O}/a_counts.gz')
open(f'{O}/a_groups.txt','w').write('A\tA\nB\tB\n')
# (b) 5 v 5 replicate pseudobulks
rng=np.random.default_rng(5); cols={}; grpf=[]
for g in 'AB':
    idx=rng.permutation(np.where(grp==g)[0]).reshape(5,6)
    for r,ix in enumerate(idx):
        nm=f'{g}{r+1}'; cols[nm]=J.iloc[:,ix].sum(1); grpf.append(f'{nm}\t{g}')
pb=pd.DataFrame(cols); write(pb,f'{O}/b_counts.gz'); open(f'{O}/b_groups.txt','w').write('\n'.join(grpf)+'\n')
print('written', os.listdir(O))
