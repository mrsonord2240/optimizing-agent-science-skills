"""Re-audit assertions on run_abc.sh output. usage: check_case.py <case> [ABC_DIR]. Env EG required."""
import os,sys,glob,pandas as pd,numpy as np
EG=os.environ['EG']; case=sys.argv[1]; A=sys.argv[2] if len(sys.argv)>2 else 'abc-head'
W=f'/mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/reaudit-run/work/{case}/out'
EXP=f'{EG}/src/{A}/tests/expected_output/generic/K562_chr22/Predictions'
ok=True
def chk(n,c):
    global ok; print(('PASS' if c else 'FAIL'),n); ok&=bool(c)
sc={'usage':'ABC.Score','powerlaw':'ABC.Score','powerlaw_v112':'ABC.Score','avgsub':'ABC.Score','atac_only':'ABC.Score','macs3':'ABC.Score'}
# NOTE: run_abc.sh uses --score_column powerlaw.Score when HIC_TYPE=none
S='powerlaw.Score' if case in('powerlaw','powerlaw_v112','atac_only','macs3') else 'ABC.Score'
thr={'usage':'0.027','powerlaw':'0.017','powerlaw_v112':'0.017','avgsub':'0.016','atac_only':'0.013','macs3':'0.017'}[case]
p=pd.read_csv(f'{W}/predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='\t')
chk(f'AllPutative {len(p)} rows; score column {S} present, in [0,1]',S in p and p[S].between(0,1).all() and len(p)>100000)
num=[c for c in p.columns if c.endswith('Numerator')]; 
if num:
    n=p[num[0]]; d=n.groupby([p.TargetGene,p.TargetGeneTSS]).transform('sum'); m=(p[S]-n/d)[~p.isSelfPromoter].abs().max()
    chk(f'{S} == {num[0]}/sum per (gene,TSS), max err {m:.2e}, non-self',m<1e-4)
chk('self-promoter rows score 1',(p.loc[p.isSelfPromoter,S]==1).all() and p.isSelfPromoter.sum()>0)
chk('distance <= 5 Mb',(p.distance<=5e6).all())
f=glob.glob(f'{W}/predictions/EnhancerPredictionsFull_threshold*.tsv'); chk(f'threshold file uses {thr}: {[os.path.basename(x) for x in f]}',len(f)==1 and f'threshold{thr}.tsv' in f[0])
t=pd.read_csv(f[0],sep='\t')
chk(f'thresholded {len(t)} rows all {S} >= {thr}',(t[S]>=float(thr)).all() and len(t)>0)
chk('no non-self promoter links in thresholded table',((t['class']!='promoter')|t.isSelfPromoter).all())
ne=pd.read_csv(f'{W}/predictions/EnhancerPredictionsAllPutativeNonExpressedGenes.tsv.gz',sep='	'); q=pd.concat([p,ne]); n_exp=int(((q[S]>=float(thr))&((q["class"]!="promoter")|q.isSelfPromoter)).sum())
chk(f'thresholded == independent filter of AllPutative+NonExpressed ({n_exp} vs {len(t)})',n_exp==len(t))
c=pd.read_csv(f'{W}/peaks/peaks.sorted.narrowPeak.candidateRegions.bed',sep='\t',header=None)
w=c[2]-c[1]; print(f'INFO candidates {len(c)}, width median {int(w.median())} max {int(w.max())}')
if case in('usage','avgsub','powerlaw','powerlaw_v112','macs3'): chk('candidates 17,732 (= ABC official), median width 500',len(c)==17732 and int(w.median())==500)
if case=='atac_only': chk('no H3K27ac columns',not any('h3k27ac' in x.lower() for x in p.columns))
if case in('usage',):
    e=pd.read_csv(f'{EXP}/EnhancerPredictionsAllPutative.tsv.gz',sep='\t')
    chk(f'AllPutative rows equal expected {len(e)}',len(e)==len(p) and len(p)==1674535)
    k=['name','TargetGene']; m=e.merge(p,on=k,suffixes=('_e',''))
    chk(f'ABC.Score matches expected on all rows, max abs diff {(m["ABC.Score_e"]-m["ABC.Score"]).abs().max():.2e}',len(m)==len(e) and (m['ABC.Score_e']-m['ABC.Score']).abs().max()<1e-5)
    ex=pd.read_csv(glob.glob(f'{EXP}/EnhancerPredictionsFull_threshold*.tsv')[0],sep='\t'); chk(f'thresholded {len(t)} == expected {len(ex)} (1,353)',len(t)==len(ex)==1353)
if case=='powerlaw_v112' or case=='powerlaw':
    o=f'{EG}/src/abc/tests/test_output/generic/K562_chr22/Predictions/EnhancerPredictionsAllPutative.tsv.gz'
sys.exit(0 if ok else 1)
