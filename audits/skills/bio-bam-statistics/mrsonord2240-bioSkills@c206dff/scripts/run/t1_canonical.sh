#!/bin/bash
# INPUT 1 (canonical, REAL data): human nf-core test BAM. Skill commands + independent hand-count.
cd /mnt/openscience/audits/bio-bam-statistics/run
D=/mnt/openscience/audit-envs/alignment-files/public-data
mkdir -p work && cp $D/human/test.paired_end.sorted.bam $D/human/test.paired_end.sorted.bam.bai work/ && cp $D/human/genome.fasta* work/
B=work/test.paired_end.sorted.bam
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
{
echo "##### checked counts"; python check_counts.py $B
echo "##### Skill awk: total mapped from idxstats"; samtools idxstats $B | awk '{sum += $3} END {print sum}'
echo "##### Skill awk: mitochondrial percentage (no chrM in this slice)"
samtools idxstats $B | awk '/^chrM/ {mt = $3} {total += $3} END {print mt/total*100 "% mitochondrial"}'
echo "##### stats SN summary numbers"; samtools stats -r work/genome.fasta $B | grep "^SN" | cut -f 2- | grep -E "raw total|reads mapped|properly|insert size|average length|error rate"
echo "##### samtools coverage"; samtools coverage $B
echo "##### samtools coverage -m (histogram)"; samtools coverage -m -A -w 60 $B | head -20
echo "##### Skill pysam: count reads"; python -c "
import skill_snippets as s; s.skill_count_reads('$B')"
echo "##### Skill pysam: per-chrom"; python -c "
import skill_snippets as s; s.skill_per_chrom('$B')"
echo "##### Skill pysam: insert size"; python -c "
import skill_snippets as s; s.skill_insert_size('$B')"
echo "##### shipped example qc_report.py (from a copy)"; python skill/examples/qc_report.py $B
} > out/t1_canonical.txt 2>&1
cat out/t1_canonical.txt
