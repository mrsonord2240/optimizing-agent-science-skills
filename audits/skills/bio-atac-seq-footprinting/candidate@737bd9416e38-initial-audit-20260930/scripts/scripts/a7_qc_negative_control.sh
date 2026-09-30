#!/bin/bash
# A7: is the SKILL's CTCF-dip gate ("clean dip = correction worked") discriminating? Negative control: build footprints from the
# UNCORRECTED signal (a1 run), classify CTCF bound sites from them, and compare the aggregate dip with the corrected pipeline.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/a1; N=$W/a7; rm -rf $N; mkdir -p $N; cd $N
awk 'BEGIN{keep=0} /^>/{keep=($2=="CTCF" && $1==">MA0139.2")} keep{print}' $R/motifs_subset.pfm > ctcf.pfm; grep -c '>' ctcf.pfm
for c in cond1 cond2; do
  ls $R/out/$c/*_uncorrected.bw
  TOBIAS ScoreBigwig --signal $R/out/$c/${c}_uncorrected.bw --regions $R/peaks.bed --output ${c}_unc_footprints.bw --cores 6 > sb_$c.log 2>&1; echo "ScoreBigwig $c rc=$?"
done
TOBIAS BINDetect --motifs ctcf.pfm --signals cond1_unc_footprints.bw cond2_unc_footprints.bw --genome $D/reference/hg38.chr1.fa --peaks $R/peaks.bed \
  --outdir bd_unc --cond-names cond1 cond2 --cores 6 > bd_unc.log 2>&1; echo "BINDetect(uncorrected) rc=$?"
ls bd_unc/CTCF_MA0139.2/beds/
