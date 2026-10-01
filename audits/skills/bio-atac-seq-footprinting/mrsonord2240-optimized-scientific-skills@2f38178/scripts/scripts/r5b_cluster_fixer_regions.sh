#!/bin/bash
# Reproduce the usage-guide per-cluster numbers exactly: same command as r5 C but on the fix-phase region set
# (fix-run/scp/regions.bed, 400 CTCF sites) with this re-audit's fresh env and bias; labels from the fix-phase label table.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
Q=bio-atac-seq-footprinting; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q; S=$SKILL/scripts/scprinter_footprint.py
E=/mnt/openscience/audit-envs/$Q; PD=/mnt/openscience/audit-envs/atac-seq/public-data; W=$E/reaudit-final/scp; cd $W
PY=/home/sci/micromamba/envs/footprint-scprinter/bin/python; export SCPRINTER_DATA=$E/scprinter
FA=$PD/reference/hg38.chr1.fa; GTF=$E/scprinter/gencode.v29.chr1.gtf; BL=$E/scprinter/hg38-blacklist.v2.bed
( time $PY $S --fragments $PD/scatac/outs/fragments.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions $E/fix-run/scp/regions.bed --outdir CF \
    --groups cells.tsv --shift 4,-5 --min-fragments 1 --modes 10,20,30,50 --bias B0/bias.h5 --jobs 2 ) > /mnt/openscience/audits/$Q/reaudit-final-20260930/logs/r5b_CF.log 2>&1; echo "CF rc=$?"
$PY - <<'PY'
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu
lab = pd.read_csv("/mnt/openscience/audit-envs/bio-atac-seq-footprinting/fix-run/scp/regions_labels.tsv", sep="\t")
z = np.load("CF/footprints.npz"); S4, modes, groups = z["scores"], z["modes"], z["groups"]
mids = [(int(k.split(":")[1].split("-")[0]) + int(k.split("-")[-1])) // 2 for k in z["keys"]]
cls = np.array([lab[(lab.s - m).abs() <= 1].cls.iloc[0] for m in mids]); b, u = cls == "bound", cls == "unbound"
n = sig = 0
for gi in range(len(groups)):
    for mi in range(len(modes)):
        cb, cu = S4[b, gi, mi, 90:110].mean(1), S4[u, gi, mi, 90:110].mean(1); n += cb.mean() > cu.mean(); sig += mannwhitneyu(cb, cu, alternative="greater").pvalue < 0.05
prof = S4[b][:, :, list(modes).index(10)].mean(0); rr = np.corrcoef(prof); off = rr[~np.eye(len(rr), dtype=bool)]
print(f"fix-phase regions: bound {b.sum()} unbound {u.sum()}; bound > unbound in {n}/20 cells; p < 0.05 in {sig}; cross-cluster r {off.min():.2f}..{off.max():.2f}")
PY
