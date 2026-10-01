#!/usr/bin/env bash
# Delta test for ATACPC-016 on real data: ENCODE GM12878 rep1 UNFILTERED chr1:1-30Mb slice
# (ENCSR095QNB). Reads whose mate maps to chrM are real aligner output (ENCODE bowtie2).
# 1) count chr1 reads whose mate is on chrM and their proper-pair bit
# 2) documented idxstats recipe, then documented `samtools view -b -f 2`
# 3) macs3 callpeak -f BAMPE and macs3 hmmratac -f BAMPE on both; compare outputs
set -uo pipefail
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
SK=/home/sci/micromamba/envs/bio-atac-seq-atac-peak-calling/bin
export PATH=$SK:$PATH
LOGDIR=/mnt/openscience/audits/bio-atac-seq-atac-peak-calling/delta-cat-20260930/logs
IN=/mnt/openscience/audit-envs/atac-seq/public-data/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam
W=/home/sci/delta-cat-20260930-apc-real
rm -rf "$W"; mkdir -p "$W"; cd "$W"
exec > "$W/run.log" 2>&1
echo "samtools: $(samtools --version | head -1)  macs3: $(macs3 --version)"
echo "input: $IN"; echo "reads: $(samtools view -c $IN)"
echo "@SQ chrM in header: $(samtools view -H $IN | grep -c 'SN:chrM\b')"
echo "chr1 reads with mate on chrM, by proper-pair bit:"
samtools view $IN | awk '$7=="chrM" {p=(and($2,2)?1:0); c["proper="p]++} END{for(k in c) print "  "k, c[k]}'
echo "all reads without 0x2 (any reason): $(samtools view -c -F 2 $IN)"

samtools idxstats $IN | cut -f1 | grep -v -e '^chrM$' -e '^\*$' | xargs samtools view -b -o noM.bam $IN
samtools index noM.bam
echo "after recipe: reads=$(samtools view -c noM.bam) mate_on_chrM=$(samtools view noM.bam | awk '$7=="chrM"' | wc -l)"
samtools view -b -f 2 -o noM.f2.bam noM.bam; samtools index noM.f2.bam
echo "after -f 2: reads=$(samtools view -c noM.f2.bam) mate_on_chrM=$(samtools view noM.f2.bam | awk '$7=="chrM"' | wc -l) @SQ=$(samtools view -H noM.f2.bam | grep -c '^@SQ')"

for B in noM noM.f2; do
  macs3 callpeak -t $B.bam -f BAMPE -g 2.7e9 -n cp_$B --outdir cp --keep-dup all -p 0.01 > cp_$B.log 2>&1
  echo "callpeak BAMPE $B: rc=$? peaks=$(cat cp/cp_${B}_peaks.narrowPeak 2>/dev/null | wc -l) | $(grep -m1 'total fragments in treatment' cp_$B.log | sed 's/.*: *#1 *//')"
done
cmp <(cut -f1-3,5,7- cp/cp_noM_peaks.narrowPeak) <(cut -f1-3,5,7- cp/cp_noM.f2_peaks.narrowPeak) && echo "callpeak narrowPeak (coords+scores) identical with and without -f 2"

for B in noM noM.f2; do
  macs3 hmmratac -i $B.bam -f BAMPE -n hm_$B --outdir hm > hm_$B.log 2>&1
  echo "hmmratac BAMPE $B: rc=$? regions=$(cat hm/hm_${B}_accessible_regions.narrowPeak 2>/dev/null | wc -l) | $(grep -m1 -iE 'fragments|total' hm_$B.log | cut -c1-140)"
done
cmp <(cut -f1-3,5,7- hm/hm_noM_accessible_regions.narrowPeak) <(cut -f1-3,5,7- hm/hm_noM.f2_accessible_regions.narrowPeak) && echo "hmmratac regions identical with and without -f 2"
echo DONE
cp -f cp_*.log hm_*.log "$LOGDIR/" 2>/dev/null
cp -f "$W/run.log" "$LOGDIR/test_f2_real.log"
