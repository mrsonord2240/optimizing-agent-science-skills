#!/bin/bash
# A3: usage-guide request "filter to <100 bp fragments, run TOBIAS on the NFR BAM": SKILL.md NFR filter (verbatim) on both BAMs, then run_tobias.sh unmodified.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/a3; rm -rf $R; mkdir -p $R; prep_inputs $R; cd $R
for s in cond1 cond2; do
  cp $s.bam sample.bam
  # --- verbatim from SKILL.md ---
  samtools view -h sample.bam | \
    awk 'substr($0,1,1)=="@" || ($9 > 0 && $9 < 100) || ($9 < 0 && $9 > -100)' | \
    samtools view -b > sample.nfr.bam
  samtools index sample.nfr.bam
  # ------------------------------
  mv sample.nfr.bam $s.nfr.bam; mv sample.nfr.bam.bai $s.nfr.bam.bai; rm sample.bam*
  echo "$s all=$(samtools view -c $s.bam) nfr=$(samtools view -c $s.nfr.bam) expected=$(samtools view -c -e 'tlen>0 && tlen<100 || tlen<0 && tlen>-100' $s.bam)"
done
awk 'BEGIN{keep=0} /^>/{n=$2; keep=(n=="CTCF"||n=="GATA1"||n=="EBF1"||n=="IRF4"||n=="CEBPA")} keep{print}' $D/motifs/JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt > motifs_subset.pfm
time bash $SKILL/scripts/run_tobias.sh cond1.nfr.bam cond2.nfr.bam peaks.bed $D/reference/hg38.chr1.fa hg38-blacklist.v2.bed motifs_subset.pfm out 6 > run.log 2>&1
echo "run_tobias.sh (NFR BAMs) rc=$?"; tail -14 run.log | cut -c1-200
