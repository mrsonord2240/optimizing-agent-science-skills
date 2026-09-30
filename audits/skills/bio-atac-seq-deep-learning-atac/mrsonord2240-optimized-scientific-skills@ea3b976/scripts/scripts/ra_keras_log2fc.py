"""Independent recomputation of variant log2FC with raw Keras (TF 2.8), no bpnet-lite/tangermeme/variant-scorer code.
For the first N SNPs of variants5.tsv (real NA12878 SNPs, hg38 chr1): one-hot the 2114 bp window centred on the SNP (index 1057), predict
log-count head for ref and alt. Writes truth = log2(exp(alt)/exp(ref)) = (alt-ref)/ln2 and the OLD formula log2(alt/ref) for contrast."""
import os, sys, numpy as np, pandas as pd
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from pyfaidx import Fasta
from chrombpnet.training.utils.losses import multinomial_nll
from tensorflow.keras.utils import get_custom_objects
get_custom_objects()["multinomial_nll"] = multinomial_nll; get_custom_objects()["tf"] = tf
ME = "/mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac"; D = "/mnt/openscience/audit-envs/atac-seq/public-data"
N = int(sys.argv[2]); out = sys.argv[1]
m = tf.keras.models.load_model(f"{ME}/public-cache/encode_model/fold_1/model.chrombpnet_nobias.fold_1.ENCSR095QNB.h5", compile=False)
fa = Fasta(f"{D}/reference/hg38.chr1.fa")
v = pd.read_csv(f"{ME}/run/variant_scorer/variants5.tsv", sep="\t", header=None, names=["chr","pos","ref","alt","id"]).head(N)
idx = {"A":0,"C":1,"G":2,"T":3}
def oh(s):
    a = np.zeros((len(s),4), np.float32)
    for i,c in enumerate(s): a[i, idx[c]] = 1
    return a
R=[];A=[]
for _,r in v.iterrows():
    s = int(r.pos)-1-1057; seq = str(fa[r.chr][s:s+2114]).upper(); assert seq[1057]==r.ref, r
    R.append(oh(seq)); alt = seq[:1057]+r.alt+seq[1058:]; A.append(oh(alt))
_, cr = m.predict(np.stack(R), batch_size=32, verbose=0); _, ca = m.predict(np.stack(A), batch_size=32, verbose=0)
cr, ca = cr.ravel(), ca.ravel()
v["logcount_ref"]=cr; v["logcount_alt"]=ca
v["log2fc_keras"]=(ca-cr)/np.log(2); v["log2fc_via_exp"]=np.log2(np.exp(ca)/np.exp(cr)); v["log2fc_OLD_formula"]=np.log2(ca/cr)
v.to_csv(out, sep="\t", index=False)
print("n",len(v),"formula identity max diff",float(np.abs(v.log2fc_keras-v.log2fc_via_exp).max()))
print("abs mean fixed",float(v.log2fc_keras.abs().mean()),"abs mean OLD",float(v.log2fc_OLD_formula.abs().mean()))
