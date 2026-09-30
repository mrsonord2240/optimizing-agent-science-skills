#!/bin/bash
# Re-audit: RGT data recipe from usage-guide in FRESH ra-footprint-rgt env: (1) old plain pip no-op negative control, (2) the documented recipe, (3) HINT-ATAC, Wellington -A, concordance.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
Q=bio-atac-seq-footprinting; E=/mnt/openscience/audit-envs/$Q; D=/mnt/openscience/audit-envs/atac-seq/public-data
SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q
L=/mnt/openscience/audits/$Q/reaudit-run/logs
W=$E/reaudit-run/hint; rm -rf $W; mkdir -p $W; cd $W
R="micromamba run -n ra-footprint-rgt"
LK=/mnt/openscience/runtime/locks/micromamba-mutate.lock
cp $E/fix-run/hint/pk60.bed $E/fix-run/hint/w.bam $E/fix-run/hint/w.bam.bai .
cp $D/reference/hg38.chr1.fa hg38.fa; cp $D/annotation/gencode.v29.chr1.gtf.gz . && gunzip gencode.v29.chr1.gtf.gz && mv gencode.v29.chr1.gtf gencode.gtf
echo "== 1. negative control: plain pip install (bioconda copy present)"
export RGTDATA=$W/rgtdata_plain
flock $LK $R pip install --no-deps rgt==1.0.2 2>&1 | tail -2 | cut -c1-160; ls $RGTDATA 2>&1 | head -3
echo "== 2. documented recipe"
export RGTDATA=$W/rgtdata
flock $LK $R pip install --no-deps --force-reinstall --no-cache-dir rgt==1.0.2 > $L/r4_rgt_pip.log 2>&1; echo "pip rc=$?"; tail -2 $L/r4_rgt_pip.log | cut -c1-160
ls $RGTDATA | head; head -5 $RGTDATA/data.config
( cd "$RGTDATA" && $R python setupGenomicData.py --hg38 --hg38-genome-path $W/hg38.fa --hg38-gtf-path $W/gencode.gtf > $W/setup.log 2>&1; echo "setupGenomicData rc=$?"; tail -3 $W/setup.log | cut -c1-160 )
mkdir out; $R rgt-hint footprinting --atac-seq --paired-end --organism=hg38 --output-location out --output-prefix sample w.bam pk60.bed > hint.log 2>&1; echo "hint rc=$?"; tail -2 hint.log | cut -c1-160
wc -l out/sample.bed; head -3 out/sample.bed
mkdir wl_A; micromamba run -n ra-footprint-pydnase wellington_footprints.py -A pk60.bed w.bam wl_A/ > wl_A.log 2>&1; echo "wellington -A rc=$?"; ls wl_A | head; wc -l wl_A/*FDR*.bed
export PATH=/home/sci/micromamba/envs/ra-footprint/bin:$PATH
B=$E/reaudit-run/rt/A/bindetect
cat $B/*/beds/*_cond1_bound.bed > all_bound.bed; cat $B/*/beds/*_cond1_unbound.bed > all_unbound.bed
echo "### HINT vs TOBIAS"; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed out/sample.bed pk60.bed
echo "### Wellington -A vs TOBIAS"; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed wl_A/*FDR*.bed pk60.bed
echo "### guard: empty input"; : > empty.bed; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed empty.bed; echo "rc=$?"
