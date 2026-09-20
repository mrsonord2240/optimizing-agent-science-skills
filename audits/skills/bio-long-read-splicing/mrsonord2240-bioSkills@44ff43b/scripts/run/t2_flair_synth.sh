#!/bin/bash
# Input 1/7 part B + Input 6 DTU prep: FLAIR workflow from SKILL.md on SYNTHETIC HiFi-like reads (3 ctrl v 3 trt, planted truth).
# Step 0: minimap2 splice:hq -uf --secondary=no per sample (SKILL)  -> BAM -> bedtools bamtobed -bed12 (example script)
# Step 1: `flair correct` EXACTLY as SKILL.md (expected to fail on FLAIR 3.0.1), then with the flags that exist.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/flair; rm -rf $O; mkdir -p $O; cd $O
G=$D/chrS1.fa
LR="micromamba run -n as-lr"
S="ctrl1 ctrl2 ctrl3 trt1 trt2 trt3"
for s in $S; do
  $LR minimap2 -ax splice:hq -uf --secondary=no -t 4 $G $D/hifi/$s.fastq 2>/dev/null | $LR samtools sort -o $s.bam - 2>/dev/null
  $LR samtools index $s.bam
  $LR bedtools bamtobed -bed12 -i $s.bam > $s.bed
done
echo "bed12 lines ctrl1: $(wc -l < ctrl1.bed)  ; bam primary reads: $($LR samtools view -c -F 2308 ctrl1.bam)"
head -2 ctrl1.bed

echo "##### 1. SKILL.md flair correct (verbatim flags, incl --genome --shortread)"
# short-read junction bed as SKILL says (--shortread short_read_junctions.bed): make one from the truth chains via regtools-like bed
$LR flair correct --query ctrl1.bed --genome $G --gtf $D/ref.gtf --shortread sj.bed --output skill_corrected --threads 4 > skill_correct.log 2>&1
echo "rc=$?"; tail -4 skill_correct.log
ls skill_corrected* 2>&1 | head -3
echo "##### 1b. SKILL verbatim without the nonexistent --shortread but with --genome"
$LR flair correct --query ctrl1.bed --genome $G --gtf $D/ref.gtf --output skill2_corrected --threads 4 > skill2_correct.log 2>&1
echo "rc=$?"; tail -3 skill2_correct.log

echo "##### 2. flair correct with flags that exist in 3.0.1 (-q -f -o -t), all six samples"
for s in $S; do
  $LR flair correct -q $s.bed -f $D/ref.gtf -o corr_$s -t 4 > corr_$s.log 2>&1
  echo "$s correct rc=$? corrected=$(wc -l < corr_${s}_all_corrected.bed) inconsistent=$(wc -l < corr_${s}_all_inconsistent.bed)"
done
cat corr_*_all_corrected.bed > all_corrected.bed
cat $D/hifi/*.fastq > all_reads.fastq

echo "##### 3. flair collapse as SKILL (--query --reads --genome --gtf --output --threads)"
$LR flair collapse --query all_corrected.bed --reads all_reads.fastq --genome $G --gtf $D/ref.gtf --output collapsed --threads 4 --generate_map > collapse.log 2>&1
echo "rc=$?"; tail -3 collapse.log; ls collapsed* | head -20
echo "isoforms in collapsed.isoforms.fa: $(grep -c '>' collapsed.isoforms.fa)"
grep '>' collapsed.isoforms.fa
echo "##### 3b. collapse with default support -s 3 vs pooled reads only; also the SKILL's FLAIR 'unstranded' note"

echo "##### 4. flair quantify as SKILL (--reads_manifest --isoforms .fa --output --threads); manifest format is NOT given in SKILL"
printf "ctrl1\tctrl\tb1\t$D/hifi/ctrl1.fastq\nctrl2\tctrl\tb1\t$D/hifi/ctrl2.fastq\nctrl3\tctrl\tb1\t$D/hifi/ctrl3.fastq\ntrt1\ttrt\tb1\t$D/hifi/trt1.fastq\ntrt2\ttrt\tb1\t$D/hifi/trt2.fastq\ntrt3\ttrt\tb1\t$D/hifi/trt3.fastq\n" > reads_manifest.tsv
$LR flair quantify --reads_manifest reads_manifest.tsv --isoforms collapsed.isoforms.fa --output quantified --threads 4 > quant.log 2>&1
echo "rc=$?"; tail -3 quant.log; ls quantified* ; head -12 quantified.counts.tsv
echo "##### 5. flair diffSplice as SKILL (--isoforms collapsed.isoforms.bed --counts_matrix .counts.tsv --out_dir --test --threads)"
$LR flair diffSplice --isoforms collapsed.isoforms.bed --counts_matrix quantified.counts.tsv --out_dir diffsplice --test --threads 4 > diffsplice.log 2>&1
echo "rc=$?"; tail -8 diffsplice.log; ls diffsplice 2>&1 | head
echo "##### 5b. lowercase module name"
$LR flair diffsplice --isoforms collapsed.isoforms.bed --counts_matrix quantified.counts.tsv --out_dir diffsplice2 --test --threads 4 > diffsplice2.log 2>&1
echo "rc=$?"; tail -8 diffsplice2.log; ls diffsplice2 2>&1 | head
