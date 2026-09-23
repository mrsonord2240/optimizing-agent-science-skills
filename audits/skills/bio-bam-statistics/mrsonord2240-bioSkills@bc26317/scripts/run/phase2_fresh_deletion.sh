#!/bin/bash
# Fresh Phase-2 input: assert the current SKILL.md's documented bcftools/samtools
# deletion distinction on the synthetic 20-read, 20-base deletion fixture.
set -euo pipefail
export LC_ALL=C
R=/mnt/openscience/audits/bio-bam-statistics/run
B=$R/data/new/own_del.bam
F=$R/data/new/own_del.fa
cd "$R/work"

samtools view -H "$B" | grep '^@SQ' | grep 'SN:del' >/dev/null
samtools mpileup -aa -Q 0 -f "$F" -r del:541-560 "$B" > phase2_samtools_del.tsv
bcftools mpileup -a FORMAT/DP,FORMAT/AD -f "$F" -r del:541-560 "$B" \
  | bcftools query -f '%POS\t%DP\t[%DP]\n' > phase2_bcftools_del.tsv

test "$(awk 'END {print NR}' phase2_samtools_del.tsv)" = 20
test "$(awk '$4 != 20 {bad=1} END {print bad ? 1 : 0}' phase2_samtools_del.tsv)" = 0
test "$(awk 'END {print NR}' phase2_bcftools_del.tsv)" = 20
test "$(awk '$2 != 0 || $3 != 0 {bad=1} END {print bad ? 1 : 0}' phase2_bcftools_del.tsv)" = 0

echo 'ASSERT samtools_mpileup_depth_541_560=20_at_all_20_positions PASS'
echo 'ASSERT bcftools_INFO_DP_and_FORMAT_DP_541_560=0_at_all_20_positions PASS'
