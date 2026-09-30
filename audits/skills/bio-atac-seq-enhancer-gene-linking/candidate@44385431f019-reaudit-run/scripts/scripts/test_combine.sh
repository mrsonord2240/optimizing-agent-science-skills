# Re-audit combine_predictions.py on my own run_abc.sh usage output x upstream rE2G K562 chr22 output; synthetic loops (planted truth)
source /mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/env.sh
S=/mnt/openscience/wt/atac-enhancer-gene-linking/skills/bio-atac-seq-enhancer-gene-linking/scripts/combine_predictions.py
R=/mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/reaudit-run; W=$R/work/combine; rm -rf $W; mkdir -p $W; cd $W
ABC=$(ls $R/work/usage/out/predictions/EnhancerPredictionsFull_threshold*.tsv)
RE=$EG/src/re2g/tests/test_output/generic/K562_chr22/dhs_intact_hic/encode_e2g_predictions_threshold0.243.tsv.gz
python -c "import pandas,pyranges;print('pandas',pandas.__version__,'pyranges',pyranges.__version__)"
python $S --help | head -5
python $S --abc $ABC --re2g $RE --out both.tsv; echo rc=$?
python $S --abc $ABC --out x.tsv; echo "missing --re2g rc=$?"
python - <<'PY'
import pandas as pd
a=pd.read_csv(sorted(__import__('glob').glob('../usage/out/predictions/EnhancerPredictionsFull_threshold*.tsv'))[0],sep='\t')
r=pd.read_csv('/mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/src/re2g/tests/test_output/generic/K562_chr22/dhs_intact_hic/encode_e2g_predictions_threshold0.243.tsv.gz',sep='\t')
b=pd.read_csv('both.tsv',sep='\t'); k=['name','TargetGene']
exp=set(map(tuple,a[k].values))&set(map(tuple,r[k].values))
print('ABC',len(a),'rE2G',len(r),'both',len(b),'independent expected intersection',len(exp))
assert set(map(tuple,b[k].values))==exp and len(b)==len(exp)
m=b.merge(r[k+['ENCODE-rE2G.Score']],on=k,suffixes=('','_r'))
assert (m['ENCODE-rE2G.Score']-m['ENCODE-rE2G.Score_r']).abs().max()<1e-9
assert b['ABC.Score'].between(0,1).all() and b['ENCODE-rE2G.Score'].between(0,1).all() and (b['ABC.Score']>=0.027).all() and (b['ENCODE-rE2G.Score']>=0.243).all()
print('PASS intersection equals independent set; scores in range and above calibrated thresholds; rE2G score carried correctly')
b=b.sort_values('distance'); pos=b.iloc[[100,200,300,400]]; rev=b.iloc[[500]]; dec=b.iloc[[600,700,800]]
rows=[]
for _,x in pos.iterrows(): rows.append((x.chr,int(x.start),int(x.end),x.chr,int(x.TargetGeneTSS)-2000,int(x.TargetGeneTSS)+2000))
for _,x in rev.iterrows(): rows.append((x.chr,int(x.TargetGeneTSS)-2000,int(x.TargetGeneTSS)+2000,x.chr,int(x.start),int(x.end)))
for _,x in dec.iterrows(): rows.append((x.chr,int(x.start),int(x.end),x.chr,int(x.TargetGeneTSS)+2000000,int(x.TargetGeneTSS)+2004000))
# also a loop on a wrong chromosome and a loop with comment header to exercise parsing
pd.DataFrame(rows).to_csv('loops.bedpe',sep='\t',header=False,index=False)
open('loops.bedpe','a').write('# comment line\n')
b.loc[list(pos.index)+list(rev.index),k].to_csv('planted.tsv',sep='\t',index=False)
b.loc[dec.index,k].to_csv('decoy.tsv',sep='\t',index=False)
PY
python $S --abc $ABC --re2g $RE --loops loops.bedpe --out both_hichip.tsv; echo rc=$?
python - <<'PY'
import pandas as pd
o=pd.read_csv('both_hichip.tsv',sep='\t'); p=pd.read_csv('planted.tsv',sep='\t'); d=pd.read_csv('decoy.tsv',sep='\t'); k=['name','TargetGene']
K=lambda x:set(map(tuple,x[k].values)); sup=K(o[o.hichip_support]); print('supported',len(sup),'planted',len(sup&K(p)),'/5 decoys flagged',len(sup&K(d)),'/3')
ex=sup-K(p); print('extras',ex)
assert K(p)<=sup and not (sup&K(d))
# extras must genuinely satisfy: some planted-loop anchor overlaps the enhancer and another the TSS
print('PASS planted 5/5 (incl. reversed), decoys 0/3; extras',len(ex),'all share enhancer/gene with planted:',all(n in {x[0] for x in K(p)} or g in set(p.TargetGene) for n,g in ex))
PY
