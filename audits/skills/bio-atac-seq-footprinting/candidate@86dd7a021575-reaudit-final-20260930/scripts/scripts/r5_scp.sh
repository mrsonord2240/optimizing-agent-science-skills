#!/bin/bash
# Re-audit scPrinter surfaces with the candidate scripts/scprinter_footprint.py, unmodified, in the FRESH usage-guide env
# footprint-scprinter (r2_scp_env.sh). Regions/labels come from this re-audit's own TOBIAS run A (r3).
#  G  guards: missing --fragments, missing --groups, malformed --shift -> rc 2, no outdir
#  D  scPrinter detect_shift on the usage-guide raw fragments (claim: returns 0,0)
#  B0 bulk, --shift 0,0 (documented for raw BAM fragments), modes 2-100, Tn5 bias predicted on GPU (no --bias)
#  B45 bulk, --shift 4,-5 (the Cell Ranger setting, wrong for raw fragments) -> contrast/centering comparison
#  C  per-cluster (--groups) usage-guide command on 10x PBMC 5k chr1:1-30 Mb, --shift 4,-5 --min-fragments 1 --modes 10,20,30,50
#  CA C with --shift auto (claim: implausible 22/12 on sparse 10x fragments)
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
Q=bio-atac-seq-footprinting; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q; S=$SKILL/scripts/scprinter_footprint.py
E=/mnt/openscience/audit-envs/$Q; PD=/mnt/openscience/audit-envs/atac-seq/public-data
W=$E/reaudit-final/scp; mkdir -p $W; cd $W
L=/mnt/openscience/audits/$Q/reaudit-final-20260930/logs
PY=/home/sci/micromamba/envs/footprint-scprinter/bin/python
MAIN=/home/sci/micromamba/envs/bio-atac-seq-footprinting/bin
export SCPRINTER_DATA=$E/scprinter          # existing pooch model cache (models already downloaded)
FA=$PD/reference/hg38.chr1.fa; GTF=$E/scprinter/gencode.v29.chr1.gtf; BL=$E/scprinter/hg38-blacklist.v2.bed
$PY -c "import scprinter, torch; print('scprinter', scprinter.__version__, 'torch', torch.__version__, 'cuda', torch.cuda.is_available())" 2>&1 | tail -1
# 1. fragments: usage-guide recipe extracted verbatim, main env samtools/bgzip/tabix
if [ ! -s frags.tsv.gz.tbi ]; then
  rm -f frags.tsv frags.tsv.gz*
  awk '/^### Fragment file for scPrinter/{s=1} /^### scPrinter per-cluster/{s=0} s' $SKILL/references/usage-guide.md | \
    awk '/^```bash/{f=1; next} /^```/{f=0} f' > frag_recipe.sh
  cat frag_recipe.sh
  sed -i 's#sample.bam#/mnt/openscience/audit-envs/bio-atac-seq-footprinting/run_tobias/cond1.bam#' frag_recipe.sh
  PATH=$MAIN:$PATH bash -e frag_recipe.sh; echo "fragment recipe rc=$?"
fi
echo "fragments: $(zcat frags.tsv.gz | wc -l)"; zcat frags.tsv.gz | head -2
# 2. regions: 200 bound + 200 unbound CTCF MA0139.2 cond1 sites from r3 run A, 1-bp motif centres
python3 - <<'PY'
import random
B = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/rt/A/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_cond1_"
random.seed(11); rows = []
for cls in ("bound", "unbound"):
    sites = [l.split("\t") for l in open(B + cls + ".bed")]
    for s in random.sample(sites, 200):
        m = (int(s[1]) + int(s[2])) // 2; rows.append((s[0], m, m + 1, cls))
rows.sort(key=lambda x: x[1])
open("regions.bed", "w").write("".join(f"{c}\t{a}\t{b}\n" for c, a, b, _ in rows))
open("labels.tsv", "w").write("chrom\ts\tcls\n" + "".join(f"{c}\t{a}\t{k}\n" for c, a, b, k in rows))
print("regions", len(rows))
PY
# 3. guards
$PY $S --fragments nope.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir g1 > $L/r5_G1.log 2>&1; echo "G missing-fragments rc=$?"; tail -1 $L/r5_G1.log
$PY $S --fragments frags.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir g2 --groups nope.tsv > $L/r5_G2.log 2>&1; echo "G missing-groups rc=$?"; tail -1 $L/r5_G2.log
$PY $S --fragments frags.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir g3 --shift 4 > $L/r5_G3.log 2>&1; echo "G bad-shift rc=$?"; tail -1 $L/r5_G3.log
for d in g1 g2 g3; do [ -e $d ] && echo "$d created" || echo "$d not created"; done
# 4. detect_shift on the raw fragments
$PY - <<'PY' > $L/r5_D.log 2>&1; echo "D rc=$?"; grep -i "shift\|result" $L/r5_D.log | tail -3
import os, scprinter as scp
from scprinter.shift_detection import detect_shift
E = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting"
g = scp.genome.Genome(name="custom", fa_file="/mnt/openscience/audit-envs/atac-seq/public-data/reference/hg38.chr1.fa",
                      gff_file=f"{E}/scprinter/gencode.v29.chr1.gtf", bias_file=f"{E}/scprinter/bias.h5", blacklist_file=f"{E}/scprinter/hg38-blacklist.v2.bed")
print("RESULT raw fragments detect_shift:", detect_shift("frags.tsv.gz", g))
PY
# 5. bulk runs
nvidia-smi --query-gpu=memory.used --format=csv,noheader
( time $PY $S --fragments frags.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir B0 --jobs 2 ) > $L/r5_B0.log 2>&1; echo "B0 rc=$?"; grep -v "it/s\|%|" $L/r5_B0.log | tail -4
( time $PY $S --fragments frags.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir B45 --shift 4,-5 --bias B0/bias.h5 --jobs 2 ) > $L/r5_B45.log 2>&1; echo "B45 rc=$?"; grep -v "it/s\|%|" $L/r5_B45.log | tail -3
# 6. per-cluster: groups TSV from the tooling snapatac2 leiden clusters (barcode, cluster)
tail -n +2 $E/tooling-scprinter/sc/clusters.csv | awk -F, 'BEGIN{OFS="\t"} {print $1, "cl"$2}' > cells.tsv; echo "cells $(wc -l < cells.tsv)"; cut -f2 cells.tsv | sort | uniq -c
( time $PY $S --fragments $PD/scatac/outs/fragments.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir C \
    --groups cells.tsv --shift 4,-5 --min-fragments 1 --modes 10,20,30,50 --bias B0/bias.h5 --jobs 2 ) > $L/r5_C.log 2>&1; echo "C rc=$?"; grep -v "it/s\|%|" $L/r5_C.log | tail -5
( time $PY $S --fragments $PD/scatac/outs/fragments.tsv.gz --fasta $FA --gtf $GTF --blacklist $BL --regions regions.bed --outdir CA \
    --groups cells.tsv --shift auto --min-fragments 1 --modes 10,20,30,50 --bias B0/bias.h5 --jobs 2 ) > $L/r5_CA.log 2>&1; echo "CA rc=$?"; grep -i "detected" $L/r5_CA.log | head -2
echo alldone
