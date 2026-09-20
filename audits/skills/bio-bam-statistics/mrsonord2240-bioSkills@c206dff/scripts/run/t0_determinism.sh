#!/bin/bash
# Skill Veto T3 (determinism) / T1 (repeat-call stability): run each headline command twice and compare md5 of the output
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
B=work/test.paired_end.sorted.bam
{
for c in "samtools flagstat $B" "samtools idxstats $B" "samtools stats $B" "samtools coverage $B" "samtools depth -a $B" "python skill/examples/qc_report.py $B"; do
  a=$($c 2>&1 | md5sum | cut -c1-12); b=$($c 2>&1 | md5sum | cut -c1-12)
  [ "$a" == "$b" ] && echo "SAME $a  $c" || echo "DIFF $a $b  $c"
done
mosdepth work/d1 $B; mosdepth work/d2 $B
[ "$(zcat work/d1.per-base.bed.gz | md5sum)" == "$(zcat work/d2.per-base.bed.gz | md5sum)" ] && echo "SAME mosdepth per-base" || echo "DIFF mosdepth"
echo "-- 10 consecutive qc_report.py calls (T1 failure-rate check):"; ok=0; for i in $(seq 10); do python skill/examples/qc_report.py $B >/dev/null 2>&1 && ok=$((ok+1)); done; echo "$ok/10 succeeded"
echo "-- static security scan of Skill files for eval/exec/os.system/shell=True/credentials:"
grep -nE "eval\(|exec\(|os\.system|subprocess|shell=True|password|token|api[_-]?key" skill/SKILL.md skill/usage-guide.md skill/examples/qc_report.py || echo "none found"
} > out/t0_determinism.txt 2>&1; cat out/t0_determinism.txt
