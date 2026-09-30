"""Execute the two method-reference snippets VERBATIM (extracted from the Skill file) against real ABC/rE2G chr22 outputs. HiChIP file is a SYNTHETIC 2-row fixture (labelled)."""
import os,re,glob,subprocess,shutil,traceback,pandas as pd
RUN=os.environ['RUN']; EG=os.environ['EG']; SK=os.environ['SKILL']
md=open(SK+'/references/method-reference.md',encoding='utf-8').read()
blocks=re.findall(r"```(bash|python)\n(.*?)```",md,re.S)
awk=[b for l,b in blocks if l=='bash' and 'awk' in b][0]; py=[b for l,b in blocks if l=='python'][0]
S=RUN+'/outputs/a6_snippets'; shutil.rmtree(S,ignore_errors=True); os.makedirs(S+'/abc_out/Predictions')
ok=True
def chk(n,c):
    global ok; print(('PASS' if c else 'FAIL'),n); ok&=bool(c)
# awk snippet on the run_abc.sh (patched) output
src=RUN+'/outputs/a2_patched/abc_out/predictions/EnhancerPredictionsAllPutative.tsv.gz'
shutil.copy(src,S+'/abc_out/Predictions/')
r=subprocess.run(['bash','-c',awk],cwd=S,capture_output=True,text=True); print('awk rc',r.returncode,r.stderr[:200])
t=pd.read_csv(S+'/abc_out/Predictions/EnhancerPredictions_thresholded.tsv',sep='\t')
chk(f'awk snippet: header retained, {len(t)} rows all ABC.Score>=0.02 (== 3000)',len(t)==3000 and t['ABC.Score'].min()>=0.02)
# combine snippet, verbatim
A=EG+'/src/abc-head/tests/test_output/generic/K562_chr22/Predictions/'
abcf=glob.glob(A+'EnhancerPredictionsFull_threshold*_self_promoter.tsv')[0]
r2f=EG+'/src/re2g/tests/test_output/generic/K562_chr22/dhs_intact_hic/encode_e2g_predictions.tsv.gz'  # full (unthresholded) table
shutil.copy(abcf,S+'/abc_predictions.tsv'); shutil.copy(r2f,S+'/encode_re2g.tsv.gz')
a=pd.read_csv(S+'/abc_predictions.tsv',sep='\t'); r=pd.read_csv(S+'/encode_re2g.tsv.gz',sep='\t')
print('ABC cols:',list(a.columns)[:8],'... rE2G cols:',[c for c in r.columns if c in('name','TargetGene','ENCODE-rE2G.Score','chr','start','end')])
chk('ABC/rE2G outputs do NOT contain columns enhancer_id/gene (snippet keys)',not({'enhancer_id','gene'}&set(a.columns)) or not({'enhancer_id','gene'}&set(r.columns)))
pd.DataFrame([['chr22',1,2,'chr22',5,6,'l1',3],['chr22',7,8,'chr22',9,10,'l2',4]]).to_csv(S+'/fithichip_loops.bedpe',sep='\t',header=False,index=False)  # SYNTHETIC
os.chdir(S)
try: exec(compile(py,'method-reference.py','exec'),{}); chk('combine snippet runs as written',True)
except Exception as e: print('EXC',type(e).__name__,e); chk('combine snippet runs as written (expect FAIL: KeyError enhancer_id)',False)
# Corrected mapping: real keys
m=a[a['ABC.Score']>=0.02].merge(r[r['ENCODE-rE2G.Score']>=0.5],on=['name','TargetGene'],suffixes=('_abc','_re2g'))
print('INFO merge on real keys (name,TargetGene): high-confidence pairs',len(m),'of ABC',int((a['ABC.Score']>=0.02).sum()),'rE2G>=0.5',int((r['ENCODE-rE2G.Score']>=0.5).sum()),'rE2G file rows',len(r),'min score',round(r['ENCODE-rE2G.Score'].min(),3))
try: m['x']=m['name'].isin(...); print('placeholder ok?')
except Exception as e: print('INFO placeholder `hichip_anchors = ...` then isin ->',type(e).__name__,str(e)[:80])
print('OVERALL(expected FAIL on the snippet)')
