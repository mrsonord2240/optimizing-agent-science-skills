# Re-audit: shipped attributions_to_modisco_npz.py -> modisco motifs -> report (tomtom mode, both `-l` and `-t`), enformer_variant_effect.py, planted-truth log2FC regression
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
S=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts
export HF_HOME=$AS/cache/hf HF_HUB_OFFLINE=1
R=$ME/run/reaudit/t; rm -rf $R; mkdir -p $R
M=$ME/public-cache/encode_model/fold_1/model.chrombpnet_nobias.fold_1.ENCSR095QNB.h5
echo "== enformer_variant_effect.py, 40 SNPs"; head -40 $ME/run/variant_scorer/variants5.tsv > $R/v40.tsv
( time py_torch $S/enformer_variant_effect.py $D/reference/hg38.chr1.fa $R/v40.tsv 12,13 $R/enf.tsv ) 2>&1 | grep -v -E "Warning|warn" | tail -5
echo "== enformer: ref-mismatch guard (planted wrong REF row must be skipped, not scored)"
printf 'chr1\t976669\tA\tC\tbadref\n' > $R/badref.tsv; head -1 $ME/run/variant_scorer/variants5.tsv >> $R/badref.tsv
py_torch $S/enformer_variant_effect.py $D/reference/hg38.chr1.fa $R/badref.tsv 12 $R/enf_bad.tsv 2>&1 | grep -v -E "Warning|warn" | tail -2
py_torch - <<PY
import pandas as pd, numpy as np
e=pd.read_csv("$R/enf.tsv",sep="\t"); print(e.shape, list(e.columns)); print(e.describe().loc[["min","max","std"]].round(4).to_string())
print("finite",bool(np.isfinite(e.filter(like="log2fc")).all().all()))
# independent recompute for 1 SNP with raw model call: SNP row 0, tracks 12
import torch; from enformer_pytorch import Enformer; from pyfaidx import Fasta
m=Enformer.from_pretrained("EleutherAI/enformer-official-rough").cuda().eval(); fa=Fasta("$D/reference/hg38.chr1.fa")
r=e.iloc[0]; L=196608; s=int(r.pos)-1-L//2; ref=str(fa["chr1"][s:s+L]).upper(); alt=ref[:L//2]+r.alt+ref[L//2+1:]
C={"A":0,"C":1,"G":2,"T":3,"N":4}
with torch.no_grad(): y=m(torch.stack([torch.tensor([C[c] for c in ref]),torch.tensor([C[c] for c in alt])]).cuda())["human"].cpu().numpy()
# independent bin geometry: window centre = position L/2 -> output bin index floor((L/2 - 40960)/128)
cb=(L//2-(L-114688)//2)//128; print("centre bin",cb)
c=y[:,cb-1:cb+1,12].sum(1); print("independent log2fc bins",cb-1,cb,"->",np.log2((c[1]+1)/(c[0]+1)),"script",r.log2fc_track12)
PY
echo "== attributions_to_modisco_npz.py 400 peaks"; O=$R/modisco
( time py_torch $S/attributions_to_modisco_npz.py $M $D/reference/hg38.chr1.fa $ME/run/variant_scorer/peaks_chr1.bed $O 400 counts ) 2>&1 | grep -E "wrote|real|Error|Traceback"
py_torch - <<PY
import numpy as np
a=np.load("$O/ohe.npz")["arr_0"]; b=np.load("$O/attr.npz")["arr_0"]
print("ohe",a.shape,a.dtype,"attr",b.shape,"finite",bool(np.isfinite(b).all()),"onehot ok",bool((a.sum(1)==1).all()),"nonzero frac",float((b!=0).mean()))
# attribution sanity: hypothetical contribs of profile vs actual-base; mean |attr| higher at centre than flanks
ab=np.abs(b).sum(1).mean(0); print("mean|attr| centre 400bp",float(ab[300:700].mean()),"flanks",float(np.r_[ab[:200],ab[-200:]].mean()))
PY
export PATH=/home/sci/micromamba/envs/dlatac-torch/bin:$PATH
cd $O; ( time modisco motifs -s ohe.npz -a attr.npz -n 2000 -w 500 -o modisco_results.h5 ) 2>&1 | grep -E "real|Error|pos_patterns|neg_patterns" | tail -4
( time modisco report -i modisco_results.h5 -o report_lite/ -s report_lite/ -m $ME/public-cache/jaspar2024_core.meme -l ) 2>&1 | grep -E "real|Error"
ls report_lite | head; 
( time env PATH=$PATH:/home/sci/micromamba/envs/dlatac-tf/bin modisco report -i modisco_results.h5 -o report_t/ -s report_t/ -m $ME/public-cache/jaspar2024_core.meme -t ) 2>&1 | grep -E "real|Error"
python - <<'PY'
import glob, pandas as pd
for f in sorted(glob.glob("report_t/patterns.tsv")+glob.glob("report_lite/patterns.tsv")):
    d=pd.read_csv(f,sep="\t"); print(f, d.shape); print(d.iloc[:,:9].head(12).to_string()[:1800])
PY
echo "== report without tomtom on PATH: documented failure -> -l alternative"
( modisco report -i modisco_results.h5 -o report_notomtom/ -s report_notomtom/ -m $ME/public-cache/jaspar2024_core.meme -t 2>&1 | tail -1 | cut -c1-200 ) 
echo "== planted-truth log2FC regression"
py_torch /mnt/openscience/audits/bio-atac-seq-deep-learning-atac/fix-run/scripts/log2fc_regression.py $R/log2fc.json 2>&1 | grep -v -E "Warning|warn" | tail -9; echo exit=$?
