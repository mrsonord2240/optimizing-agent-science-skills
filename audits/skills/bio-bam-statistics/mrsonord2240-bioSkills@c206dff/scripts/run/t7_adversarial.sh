#!/bin/bash
# INPUT 7 (adversarial/ambiguous, SYNTH): header-only BAM, single-end BAM, unindexed BAM, contig-naming (MT vs chrM) through the Skill's recipes
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
for b in data/empty.bam data/se.bam data/noindex.bam; do
  echo "=================== $b"
  echo "-- flagstat:"; samtools flagstat $b 2>&1 | head -8
  echo "-- idxstats (rc=$(samtools idxstats $b >/dev/null 2>&1; echo $?)):"; samtools idxstats $b 2>&1 | head -3
  echo "-- Skill pysam count reads:"; python -c "
import skill_snippets as s; s.skill_count_reads('$b')" 2>&1 | tail -2
  echo "-- Skill pysam per-chrom (get_index_statistics):"; python -c "
import skill_snippets as s; s.skill_per_chrom('$b')" 2>&1 | tail -2
  echo "-- shipped qc_report.py:"; python skill/examples/qc_report.py $b 2>&1 | tail -3
  echo "-- Skill awk mean depth (samtools depth | awk sum/n) rc:"; samtools depth $b 2>&1 | awk '{sum += $3; n++} END {print sum/n}' 2>&1 | tail -2
  echo "-- Skill awk mito%:"; samtools idxstats $b 2>&1 | awk '/^chrM/ {mt = $3} {total += $3} END {print mt/total*100 "% mitochondrial"}' 2>&1 | tail -2
  echo "-- samtools coverage:"; samtools coverage $b 2>&1 | head -3
  echo "-- Skill mosdepth:"; mosdepth work/t7_$(basename $b .bam) $b 2>&1 | tail -2
done
echo "=================== contig naming: chrM renamed MT (Ensembl style)"
samtools view -h data/synth.bam | sed 's/chrM/MT/g' | samtools view -b -o work/synth_MT.bam - && samtools index work/synth_MT.bam
echo -n "idxstats MT row: "; samtools idxstats work/synth_MT.bam | grep '^MT'
samtools idxstats work/synth_MT.bam | awk '/^chrM/ {mt = $3} {total += $3} END {print mt/total*100 "% mitochondrial   <-- Skill awk"}'
echo "=================== Skill/usage-guide sex-check awk on a BAM without chrX/chrY"
samtools idxstats data/synth.bam | awk '/^chrX/ {x=$3} /^chrY/ {y=$3} END {printf "X:Y = %.2f   <-- usage-guide awk\n", x/(y+1)}'
} > out/t7_adversarial.txt 2>&1
cat out/t7_adversarial.txt
