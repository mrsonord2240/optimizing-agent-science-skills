#!/bin/bash
# Re-audit: scBasset documented commands (preprocess, 1-epoch train, embedding) on real 10x PBMC 5k chr1-4 peaks; capped
# (scBasset preprocess needs >=1000 peaks in each of val/test, i.e. >~10k peaks in total; chr1-only 30 Mb slice is too small).
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
PY=/home/sci/micromamba/envs/dlatac-tf2k2/bin/python
W=$ME/run/reaudit/scb; rm -rf $W; mkdir -p $W; cd $W
SRC=$ME/src/scBasset
[ -f $ME/public-cache/ucsc/chr12.fa ] || true
(cat $D/reference/hg38.chr1.fa; zcat $ME/public-cache/ucsc/chr2.fa.gz $ME/public-cache/ucsc/chr3.fa.gz $ME/public-cache/ucsc/chr4.fa.gz) > chr12.fa
cat > mk_h5ad.py <<'PYEOF'
import numpy as np, scanpy as sc, scipy.sparse as sp, h5py, pandas as pd
D = "/mnt/openscience/audit-envs/atac-seq/public-data/scatac/raw"
with h5py.File(f"{D}/atac_v1_pbmc_5k_filtered_peak_bc_matrix.h5") as f:
    m = f["matrix"]
    X = sp.csc_matrix((m["data"][:], m["indices"][:], m["indptr"][:]), shape=tuple(m["shape"][:]))
    bc = [b.decode() for b in m["barcodes"][:]]
    ids = [i.decode() for i in m["features"]["id"][:]]
X = X.T.tocsr()
ad = sc.AnnData(X, obs=pd.DataFrame(index=bc), var=pd.DataFrame(index=ids))
ad.var["chr"] = [i.split(":")[0] for i in ids]
ad = ad[:, ad.var["chr"].isin(["chr1", "chr2", "chr3", "chr4"]).values].copy()
ad.var["start"] = [int(i.split(":")[1].split("-")[0]) for i in ad.var_names]
ad.var["end"] = [int(i.split(":")[1].split("-")[1]) for i in ad.var_names]
sc.pp.filter_cells(ad, min_counts=1000)
sc.pp.filter_genes(ad, min_cells=int(0.003 * ad.n_obs))   # README says 5%, but that leaves <1000 val/test peaks (preprocess crash)
print("h5ad", ad.shape)
ad.write("pbmc5k_chr12.h5ad")
PYEOF
$PY mk_h5ad.py 2>&1 | tail -2
$PY $SRC/bin/scbasset_preprocess.py --ad_file pbmc5k_chr12.h5ad --input_fasta chr12.fa --out_path processed 2>&1 | tail -3
ls processed
timeout 2400 $PY $SRC/bin/scbasset_train.py --input_folder processed --out_path out --epochs 1 --batch_size 128 2>&1 | grep -v -E "^\s*$|Warning|warn|I0000|W0000|E0000|│|├|└|┌|┏|┡|┗|━" | tail -25
ls -R out | head -20
cat > emb.py <<'PYEOF'
import glob, numpy as np, tensorflow as tf, anndata
from scbasset.utils import make_model
ad = anndata.read_h5ad("processed/ad.h5ad")
n = ad.shape[0]
h5 = sorted(glob.glob("out/*.h5"))
print("weights", h5)
model = make_model(32, n, show_summary=False)
model.load_weights(h5[0])
ker = [w for w in model.weights if len(w.shape) == 2 and w.shape[-1] == n][0].numpy()
print("cell embedding kernel", ker.shape, "finite", bool(np.isfinite(ker).all()), "std", float(ker.std()), "tf", tf.__version__)
print("PASS_EMB" if ker.shape == (32, n) and np.isfinite(ker).all() and ker.std() > 0 else "FAIL_EMB")
PYEOF
$PY emb.py 2>&1 | grep -E "weights|cell embedding|PASS_EMB|FAIL_EMB|Error" | cut -c1-250
