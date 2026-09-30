"""Smoke assertions for ABC HEAD chr22 official run: compare to shipped expected_output and check scientific invariants."""
import sys,glob,os,numpy as np,pandas as pd
R='/mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/src/'+os.environ.get('ABC_DIR','abc')+'/tests/'
cols={"chr":str,"start":np.int64,"end":np.int64,"name":str,"class":str,"TargetGene":str,"ABC.Score.Numerator":np.float64,"ABC.Score":np.float64,"powerlaw.Score":np.float64}
ok=True
def chk(n,c):
    global ok; print(('PASS' if c else 'FAIL'),n); ok&=bool(c)
for b in ['K562_chr22','K562_chr22_tagAlign']:
    t=R+'test_output/generic/'+b; e=R+'expected_output/generic/'+b
    a=pd.read_csv(t+'/Predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='\t',dtype=cols,usecols=cols.keys())
    x=pd.read_csv(e+'/Predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='\t',dtype=cols,usecols=cols.keys())
    try: pd.testing.assert_frame_equal(a,x); same=True
    except AssertionError as ex: same=False; print(str(ex)[:300])
    chk(f'{b}: AllPutative identical to shipped expected ({len(a)} rows)',same)
    tf=glob.glob(t+'/Predictions/EnhancerPredictionsFull_threshold*_self_promoter.tsv')[0]; ef=glob.glob(e+'/Predictions/EnhancerPredictionsFull_threshold*_self_promoter.tsv')[0]
    ta=pd.read_csv(tf,sep='\t',dtype=cols,usecols=cols.keys()); ea=pd.read_csv(ef,sep='\t',dtype=cols,usecols=cols.keys())
    try: pd.testing.assert_frame_equal(ta,ea); s2=True
    except AssertionError: s2=False
    chk(f'{b}: thresholded identical ({len(ta)} rows, {os.path.basename(tf)})',s2)
    # invariant: ABC.Score = Numerator / per-gene sum(Numerator) (file rounds scores to 3 decimals, so per-gene score sums drift above 1)
    a2=pd.read_csv(t+'/Predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='	',usecols=['TargetGene','TargetGeneTSS','isSelfPromoter','ABC.Score','ABC.Score.Numerator'])
    num=a2.groupby(['TargetGene','TargetGeneTSS'])['ABC.Score.Numerator'].transform('sum')
    ns=~a2['isSelfPromoter']   # self-promoters are forced to score 1 by predictor.compute_score
    err=(a2['ABC.Score.Numerator']/num-a2['ABC.Score'])[ns].abs().max()
    chk(f'{b}: self-promoter rows forced to 1 ({int((~ns).sum())} rows)', (a2.loc[~ns,'ABC.Score']==1).all() and (~ns).sum()>0)
    chk(f'{b}: ABC.Score == Numerator/sum_e(Numerator) per (gene,TSS) within 5e-4 (non-self-promoter rows) (max err {err:.2e})', err<5e-4)
    chk(f'{b}: scores in [0,1]', a['ABC.Score'].between(0,1).all())
    chk(f'{b}: thresholded all >= threshold', ta['ABC.Score'].min()>=float(os.path.basename(tf).split('threshold')[1].split('_')[0])-1e-9)
sys.exit(0 if ok else 1)
