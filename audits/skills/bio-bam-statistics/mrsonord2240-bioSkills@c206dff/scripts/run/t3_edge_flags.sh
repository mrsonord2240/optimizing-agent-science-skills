#!/bin/bash
# INPUT 3 (edge, SYNTHETIC): BAM with secondary/supplementary/QC-fail/dup/unmapped/singleton/mate-diff-chr, exact planted counts.
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
B=data/synth.bam
{
echo "##### planted truth (by construction)"; cat data/synth.truth.json | head -20
echo "##### checked counts"; python check_counts.py $B
echo "##### Skill awk: mitochondrial percentage (chrM present; 40 mito reads of 525 mapped-flag records)"
samtools idxstats $B | awk '/^chrM/ {mt = $3} {total += $3} END {print mt/total*100 "% mitochondrial"}'
echo "##### Skill pysam: count reads"; python -c "
import skill_snippets as s; print(s.skill_count_reads('$B'))"
echo "##### usage-guide pysam flagstat"; python -c "
import skill_snippets as s; print(s.guide_flagstat('$B'))"
echo "##### shipped example qc_report.py"; python skill/examples/qc_report.py $B
echo "##### mapped-and-MAPQ>=30 fraction (Skill view -c commands)"
echo -n "num (-F 2308 -q 30): "; samtools view -c -F 2308 -q 30 $B
echo -n "den (-F 2308)      : "; samtools view -c -F 2308 $B
} > out/t3_edge_flags.txt 2>&1
cat out/t3_edge_flags.txt
