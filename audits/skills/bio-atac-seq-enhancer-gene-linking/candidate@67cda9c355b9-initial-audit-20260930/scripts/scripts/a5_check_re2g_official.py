"""ENCODE-rE2G chr22 official run: compare to shipped expected_output + score sanity; then run the Skill's combine snippet against real ABC + rE2G outputs."""
import os,glob,sys,numpy as np,pandas as pd
EG=os.environ['EG']; R=EG+'/src/re2g/tests/'
cols={"chr":str,"start":np.int64,"end":np.int64,"name":str,"class":str,"TargetGene":str,"ABC.Score":np.float64,"ENCODE-rE2G.Score":np.float64}
ok=True
def chk(n,c):
    global ok; print(('PASS' if c else 'FAIL'),n); ok&=bool(c)
b='K562_chr22'; t=R+'test_output/generic/'+b+'/dhs_intact_hic/'; e=R+'expected_output/generic/'+b+'/dhs_intact_hic/'
a=pd.read_csv(t+'encode_e2g_predictions.tsv.gz',sep='\t',dtype=cols,usecols=cols.keys()); x=pd.read_csv(e+'encode_e2g_predictions.tsv.gz',sep='\t',dtype=cols,usecols=cols.keys())
try: pd.testing.assert_frame_equal(a,x); same=True
except AssertionError as ex: same=False; print(str(ex)[:300])
chk(f'rE2G all-putative identical to shipped expected ({len(a)} rows)',same)
tf=glob.glob(t+'encode_e2g_predictions_threshold*[0-9].tsv.gz')[0]; ef=glob.glob(e+'encode_e2g_predictions_threshold*[0-9].tsv.gz')[0]
ta=pd.read_csv(tf,sep='\t',dtype=cols,usecols=cols.keys()); ea=pd.read_csv(ef,sep='\t',dtype=cols,usecols=cols.keys())
try: pd.testing.assert_frame_equal(ta,ea); s2=True
except AssertionError: s2=False
chk(f'thresholded identical ({len(ta)} rows, {os.path.basename(tf)})',s2)
s=a['ENCODE-rE2G.Score']
chk(f'rE2G scores are probabilities in [0,1] (min {s.min():.3g}, max {s.max():.3g}, n>=0.5: {(s>=0.5).sum()})',s.between(0,1).all())
chk('rE2G.Score >= 0.5 links exist and rank positively with ABC (spearman>0; arbitrary bounds avoided)',(s>=0.5).sum()>0 and a[['ABC.Score','ENCODE-rE2G.Score']].corr('spearman').iloc[0,1]>0)
print('INFO spearman(ABC.Score, rE2G.Score) =',round(a[['ABC.Score','ENCODE-rE2G.Score']].corr('spearman').iloc[0,1],3))
# --- Skill combine snippet, run against real outputs (chr22)
abc=pd.read_csv(EG+'/src/abc-head/tests/test_output/generic/K562_chr22/Predictions/EnhancerPredictionsAllPutative.tsv.gz',sep='\t')
re2g=pd.read_csv(t+'encode_e2g_predictions.tsv.gz',sep='\t')
print('INFO ABC columns with id/gene:',[c for c in abc.columns if c in('name','TargetGene','enhancer_id','gene')],'| rE2G:',[c for c in re2g.columns if c in('name','TargetGene','enhancer_id','gene')])
try:
    hc=abc[abc['ABC.Score']>=0.02].merge(re2g[re2g['ENCODE-rE2G.Score']>=0.5],on=['enhancer_id','gene']); chk('Skill snippet merge on [enhancer_id, gene] runs',True)
except KeyError as ex: chk(f'Skill snippet merge on [enhancer_id, gene] runs (KeyError {ex})',False)
hc=abc[abc['ABC.Score']>=0.02].merge(re2g[re2g['ENCODE-rE2G.Score']>=0.5],on=['name','TargetGene'],suffixes=('_abc','_re2g'))
chk(f'merge on real keys [name, TargetGene] gives high-confidence set ({len(hc)} pairs)',len(hc)>0)
sys.exit(0 if ok else 1)
