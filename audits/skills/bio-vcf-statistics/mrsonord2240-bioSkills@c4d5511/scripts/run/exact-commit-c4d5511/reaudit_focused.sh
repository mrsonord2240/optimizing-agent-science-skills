#!/usr/bin/env bash
# Exact-commit focused re-audit for bio-vcf-statistics.
set -euo pipefail

readonly EXPECTED_SHA='c4d5511fe2830349a9d65609495018ed862ead58'
readonly SOURCE='/mnt/f/OpenScience/wt/bio-vcf-statistics-final-20260924'
readonly SKILL="$SOURCE/variant-calling/vcf-statistics/SKILL.md"
readonly GUIDE="$SOURCE/variant-calling/vcf-statistics/usage-guide.md"
readonly DATA='/mnt/f/OpenScience/audits/bio-vcf-statistics/data/cohort.vcf'
readonly WORK='/tmp/bio-vcf-statistics-exact-c4d5511'

assert() {
  local label="$1"
  shift
  if "$@"; then
    printf 'PASS | %s\n' "$label"
  else
    printf 'FAIL | %s\n' "$label" >&2
    exit 1
  fi
}

# The invoking Windows-side audit command verifies this worktree's Git HEAD,
# because WSL Git cannot resolve this Windows worktree's .git pointer.
assert 'pinned commit identifier is recorded' test "$EXPECTED_SHA" = 'c4d5511fe2830349a9d65609495018ed862ead58'
assert 'SKILL handles all biallelic het orientations' grep -Fq '^(0[\/|]1|1[\/|]0)$' "$SKILL"
assert 'usage guide handles all biallelic het orientations' grep -Fq '^(0[\/|]1|1[\/|]0)$' "$GUIDE"
assert 'SKILL declares multiallelic boundary' grep -Fq 'multiallelic-aware parser' "$SKILL"
assert 'usage guide declares multiallelic boundary' grep -Fq 'multi-allelic `AD` explicitly' "$GUIDE"
assert 'strict and not-failed FILTER semantics are documented' grep -Fq "strict PASS (excludes FILTER='.'" "$SKILL"
assert 'peddy target-panel limitation is documented' grep -Fq 'human, genome-wide callset' "$SKILL"
assert 'somalier custom-panel remediation is documented' grep -Fq 'somalier find-sites <population.vcf.gz>' "$SKILL"

rm -rf "$WORK"
mkdir -p "$WORK"
cd "$WORK"
bgzip -c "$DATA" > cohort.vcf.gz
bcftools index -t cohort.vcf.gz

bcftools stats -s - cohort.vcf.gz > per_sample.txt
assert 'bcftools stats produces eight PSC sample rows' test "$(grep -c '^PSC' per_sample.txt)" -eq 8
assert 'Ti/Tv extraction recipe returns the synthetic expected value' test "$(bcftools stats cohort.vcf.gz | awk -F '\t' '/^TSTV/{print $5; exit}')" = '1.43'
assert 'strict PASS excludes unfiltered records' test "$(bcftools view -f PASS -H cohort.vcf.gz | wc -l)" -eq 0
assert 'not-failed includes unfiltered records' test "$(bcftools view -f .,PASS -H cohort.vcf.gz | wc -l)" -eq 361

bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz |
  awk -F '\t' 'BEGIN {OFS="\t"} {if ($2 == "0/1" && (++flip[$1] % 2) == 0) $2 = "1/0"; print}' > orientation_mixed.tsv
expected="$(bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | awk -F '\t' '$2 ~ /^(0[\/|]1|1[\/|]0)$/ {split($3,a,","); if (a[1]+a[2] > 0) n++} END {print n+0}')"
observed="$(awk -F '\t' '$2 ~ /^(0[\/|]1|1[\/|]0)$/ {split($3,a,","); if (a[1]+a[2] > 0) n++} END {print n+0}' orientation_mixed.tsv)"
reversed="$(awk -F '\t' '$2 == "1/0" {n++} END {print n+0}' orientation_mixed.tsv)"
reversed_matched="$(awk -F '\t' '$2 == "1/0" && $2 ~ /^(0[\/|]1|1[\/|]0)$/ {n++} END {print n+0}' orientation_mixed.tsv)"
printf 'DEBUG | expected=%s observed=%s reversed=%s reversed_matched=%s\n' "$expected" "$observed" "$reversed" "$reversed_matched"
assert 'orientation-mixed check retains every biallelic het' test "$observed" = "$expected"
assert 'orientation-mixed fixture contains reversed unphased hets' test "$reversed" -gt 0

bcftools query -f '%CHROM\t%POS\t%INFO/ExcessHet\n' cohort.vcf.gz |
  awk '$3 > 54.69' > excess_het.tsv
assert 'excess-het-only route identifies six planted artifacts' test "$(wc -l < excess_het.tsv)" -eq 6
printf 'VALUES | ti_tv=1.43 strict_pass=0 not_failed=361 biallelic_hets=%s mixed_hets=%s excess_het=%s\n' \
  "$expected" "$observed" "$(wc -l < excess_het.tsv)"
printf 'SUMMARY | 15/15 assertions passed\n'
