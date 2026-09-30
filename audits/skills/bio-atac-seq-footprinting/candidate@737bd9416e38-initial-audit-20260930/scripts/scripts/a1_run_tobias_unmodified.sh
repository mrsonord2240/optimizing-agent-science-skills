#!/bin/bash
# A1: Skill's scripts/run_tobias.sh, UNMODIFIED, on ENCODE GM12878 (cond1) vs K562 (cond2), chr1:1-30Mb, 11-TF JASPAR2024 subset.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/a1; rm -rf $R; mkdir -p $R; prep_inputs $R; cd $R
awk 'BEGIN{keep=0} /^>/{n=$2; keep=(n=="CTCF"||n=="SPI1"||n=="GATA1"||n=="GATA1::TAL1"||n=="EBF1"||n=="IRF4"||n=="RUNX1"||n=="CEBPA"||n=="JUN::JUNB"||n=="FOS::JUN"||n=="TAL1::TCF3")} keep{print}' $D/motifs/JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt > motifs_subset.pfm
grep -c '>' motifs_subset.pfm
TOBIAS --version; sha256sum $SKILL/scripts/run_tobias.sh
time bash $SKILL/scripts/run_tobias.sh cond1.bam cond2.bam peaks.bed $D/reference/hg38.chr1.fa hg38-blacklist.v2.bed motifs_subset.pfm out 8 > run.log 2>&1
echo "run_tobias.sh rc=$?"
tail -16 run.log | cut -c1-200
