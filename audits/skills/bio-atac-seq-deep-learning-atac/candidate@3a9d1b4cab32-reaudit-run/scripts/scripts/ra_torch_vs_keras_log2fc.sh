source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH HF_HUB_OFFLINE=1 HF_HOME=$AS/cache/hf
S=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts
R=$ME/run/reaudit; mkdir -p $R/l2; M=$ME/public-cache/encode_model/fold_1/model.chrombpnet_nobias.fold_1.ENCSR095QNB.h5
echo "== independent Keras"; py_tf $(dirname $0)/ra_keras_log2fc.py $R/l2/keras.tsv 200 2>&1 | grep -v -E "Warning|warn"
echo "== shipped score_variants_torch.py (GPU) on same 200"; py_torch $S/score_variants_torch.py $M $D/reference/hg38.chr1.fa $ME/run/variant_scorer/variants5.tsv $R/l2/torch.tsv 2>&1 | grep -v -E "Warning|warn"
echo "== shipped Enformer script sanity handled elsewhere"
py_torch - <<PY
import pandas as pd, numpy as np
k=pd.read_csv("$R/l2/keras.tsv",sep="\t"); t=pd.read_csv("$R/l2/torch.tsv",sep="\t")
m=k.merge(t,on=["chr","pos","ref","alt"])
print("merged",len(m),"of",len(k),len(t))
print("corr",np.corrcoef(m.log2fc,m.log2fc_keras)[0,1],"max|diff|",(m.log2fc-m.log2fc_keras).abs().max())
print("max|diff| logcount ref",(m.logcount_ref_x-m.logcount_ref_y).abs().max() if "logcount_ref_x" in m else "n/a")
# variant-scorer forward_only (fixer output, real counts head) is a third method
b=pd.read_csv("/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/fix-run/vs_fo/v5fo.variant_scores.tsv",sep="\t")
mm=m.merge(b,left_on=["chr","pos","ref","alt"],right_on=["chr","pos","allele1","allele2"])
print("vs variant-scorer fwd-only n",len(mm),"corr",np.corrcoef(mm.log2fc_keras,mm.logfc)[0,1],"max|diff|",(mm.log2fc_keras-mm.logfc).abs().max())
print("scorer logfc == log2(a2/a1)?",float(np.abs(np.log2(mm.allele2_pred_counts/mm.allele1_pred_counts)-mm.logfc).max()))
print("n|log2fc|>1 keras",int((m.log2fc_keras.abs()>1).sum()),"OLD formula",int((m.log2fc_OLD_formula.abs()>1).sum()))
print("ratio of mean|fixed| to mean|OLD|",float(m.log2fc_keras.abs().mean()/m.log2fc_OLD_formula.abs().mean()))
PY
