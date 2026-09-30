"""Audit assertions on run_abc.sh (A1 as shipped, A2 patched copy). Hi-C is a chr22 real-K562 substitute in avg-format layout (mechanics only)."""
import os,re,sys,pandas as pd,pyBigWig,pyranges as pr
RUN=os.environ['RUN']; EG=os.environ['EG']; W=RUN+'/outputs/a2_patched'; O=W+'/abc_out'
ok=True
def chk(n,c):
    global ok; print(('PASS' if c else 'FAIL'),n); ok&=bool(c)
a1=open(RUN+'/logs/a1_shipped.log').read()
chk('A1 shipped script fails at predict.py with the accessibility-feature ValueError (defect reproduced)','The feature has to be either ATAC or DHS!' in a1 and 'run_abc.sh rc=1' in a1)
chk('A1 shipped script produced no AllPutative output',not os.path.exists(RUN+'/outputs/a1_shipped/abc_out/predictions/EnhancerPredictionsAllPutative.tsv.gz'))
a2=open(RUN+'/logs/a2_patched.log').read()
chk('A2 patched copy completes rc=0','patched run_abc.sh rc=0' in a2)
chk('neighborhoods ran WITHOUT --qnorm (qnorm=None) although SKILL.md workflow step 3 requires quantile normalisation','qnorm=None' in a2)
for t in ('atac','h3k27ac'):
    bw=pyBigWig.open(f'{O}/tracks/{t}.bw'); st=bw.stats('chr22',0,50818468,exact=True)[0]
    chk(f'{t}.bw opens; chr22 mean RPGC {st:.2f} > 0',st and st>0)
cand=pd.read_csv(f'{O}/peaks/candidate_enhancers.bed',sep='\t',header=None)
w=cand[2]-cand[1]
print(f'INFO candidates {len(cand)}; width median {int(w.median())} bp, max {int(w.max())} bp, n>5kb {(w>5000).sum()}, n>1Mb {(w>1e6).sum()}')
off=pd.read_csv(EG+'/src/abc-head/tests/test_output/generic/K562_chr22/Neighborhoods/EnhancerList.txt',sep='\t')
print(f'INFO official ABC candidate regions (makeCandidateRegions): {len(off)}; width median {int((off.end-off.start).median())} bp, max {int((off.end-off.start).max())} bp')
chk('candidate widths are NOT ABC standard summit-centred 500 bp (documenting deviation: max width > 5 kb)',w.max()>5000)
p=pd.read_csv(f'{O}/predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='\t')
chk(f'AllPutative parses: {len(p)} rows; ABC.Score in [0,1]; per (gene,TSS) sum<=1.0001',p['ABC.Score'].between(0,1).all() and len(p)>100000)
n_pd=int((p['ABC.Score']>=0.02).sum())
chk(f'script threshold count 3000 == pandas count {n_pd}',n_pd==3000)
top=p[p['ABC.Score']>=0.02]
chk('thresholded links within 5 Mb window',(top.distance<=5e6).all())
tw=(top.end-top.start)
print(f'INFO thresholded links: enhancers wider than 5 kb: {(tw>5000).sum()} of {len(top)} ({(tw>5000).mean():.1%}); ABC.Score max {p["ABC.Score"].max():.3f}')
off_dir=EG+'/src/abc-head/tests/test_output/generic/K562_chr22/Predictions/'
of=[f for f in os.listdir(off_dir) if f.startswith('EnhancerPredictionsFull_threshold') and f.endswith('.tsv')][0]
o=pd.read_csv(off_dir+of,sep='\t'); print('INFO official threshold file',of,'rows',len(o))
o=o[~o.isSelfPromoter]; t2=top[~top.isSelfPromoter]
mk=lambda d:pr.PyRanges(d[['chr','start','end','TargetGene']].rename(columns={'chr':'Chromosome','start':'Start','end':'End'}))
j=mk(o).join(mk(t2),suffix='_b').df
hit=j[j.TargetGene==j.TargetGene_b][['Start','End','TargetGene']].drop_duplicates()
fr=len(hit)/len(o); print(f'INFO official non-self links {len(o)}; recovered {len(hit)} ({fr:.2f}); run_abc.sh non-self links {len(t2)}')
chk('recovery of official links > 0.3 (loose sanity: different candidates and substitute Hi-C)',fr>0.3)
print('OVERALL','PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
