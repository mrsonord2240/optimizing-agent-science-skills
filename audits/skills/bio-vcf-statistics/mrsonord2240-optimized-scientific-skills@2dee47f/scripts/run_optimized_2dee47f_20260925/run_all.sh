#!/usr/bin/env bash
set -euo pipefail

readonly BASE='/mnt/openscience/audits/bio-vcf-statistics/reaudit-optimized-scientific-skills@2dee47f-20260925'
readonly RUN="$BASE/run"
readonly DATA="$BASE/data"
readonly OUT="$BASE/outputs"
readonly SOURCE='/mnt/openscience/audit-sources/optimized-scientific-skills-2dee47f/skills/bio-vcf-statistics'
readonly EXPECTED_SHA='2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db'
readonly VCFTOOLS='/home/sci/micromamba/envs/atac-jvm/bin/vcftools'

source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
mkdir -p "$DATA" "$OUT"

checks=0
passes=0
check() {
  local label="$1"
  shift
  checks=$((checks + 1))
  if "$@"; then
    passes=$((passes + 1))
    printf 'PASS | %s\n' "$label"
  else
    printf 'FAIL | %s\n' "$label"
  fi
}

value() { printf 'VALUE | %s\n' "$*"; }

printf 'SOURCE | mrsonord2240/optimized-scientific-skills@%s:skills/bio-vcf-statistics\n' "$EXPECTED_SHA"
bcftools --version | head -2
"$VCFTOOLS" --version
/usr/bin/python3 - <<'PY'
import cyvcf2
print(f"cyvcf2 {cyvcf2.__version__}")
PY

/usr/bin/python3 "$RUN/generate_fixtures.py"
cp "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py"
sha256sum "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py" > "$OUT/source_copy.sha256"
check 'source example copy is byte-identical' cmp -s "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py"

for stem in cohort callerA callerB core_regression filter_semantics empty transitions_only; do
  bgzip -f -c "$DATA/$stem.vcf" > "$OUT/$stem.vcf.gz"
  bcftools index -f -t "$OUT/$stem.vcf.gz"
done

printf '\n=== INPUT 1: prior canonical cohort statistics regression ===\n'
bcftools stats -s - "$OUT/cohort.vcf.gz" > "$OUT/input1_cohort.stats.txt"
/usr/bin/python3 "$RUN/vcf_stats.source-copy.py" "$OUT/cohort.vcf.gz" > "$OUT/input1_vcf_stats.txt"
input1_psc=$(grep -c '^PSC' "$OUT/input1_cohort.stats.txt")
input1_tstv=$(awk -F '\t' '/^TSTV/{print $5; exit}' "$OUT/input1_cohort.stats.txt")
input1_strict=$(bcftools view -f PASS -H "$OUT/cohort.vcf.gz" | wc -l)
input1_notfailed=$(bcftools view -f .,PASS -H "$OUT/cohort.vcf.gz" | wc -l)
check 'prior cohort has eight PSC sample rows' test "$input1_psc" -eq 8
check 'prior cohort Ti/Tv is 1.43' test "$input1_tstv" = '1.43'
check 'strict PASS excludes all 361 unfiltered-dot records' test "$input1_strict" -eq 0
check 'not-failed includes all 361 unfiltered-dot records' test "$input1_notfailed" -eq 361
check 'example processes prior cohort record count' grep -Eq 'Total variants:[[:space:]]+361$' "$OUT/input1_vcf_stats.txt"
value "input1 psc=$input1_psc tstv=$input1_tstv strict_pass=$input1_strict not_failed=$input1_notfailed"

printf '\n=== INPUT 2: prior orientation-mixed allele-balance regression ===\n'
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' "$OUT/cohort.vcf.gz" |
  awk -F '\t' 'BEGIN {OFS="\t"} {if ($2 == "0/1" && (++flip[$1] % 2) == 0) $2 = "1/0"; print}' > "$OUT/input2_orientation_mixed.tsv"
expected_hets=$(bcftools query -f '[%GT\n]' "$OUT/cohort.vcf.gz" | grep -Ec '^(0/1|0\|1|1/0|1\|0)$')
observed_hets=$(awk -F '\t' '$2 ~ /^(0[\/|]1|1[\/|]0)$/ {split($3,a,","); if (a[1]+a[2] > 0) n++} END {print n+0}' "$OUT/input2_orientation_mixed.tsv")
reversed_hets=$(awk -F '\t' '$2 == "1/0" {n++} END {print n+0}' "$OUT/input2_orientation_mixed.tsv")
check 'orientation fixture has 747 biallelic heterozygotes' test "$expected_hets" -eq 747
check 'documented matcher retains all orientation-mixed heterozygotes' test "$observed_hets" -eq "$expected_hets"
check 'orientation fixture includes reversed unphased heterozygotes' test "$reversed_hets" -eq 372
check 'Skill documents multiallelic AD boundary' grep -Fq 'multiallelic-aware parser' "$SOURCE/SKILL.md"
value "input2 expected=$expected_hets observed=$observed_hets reversed=$reversed_hets"

printf '\n=== INPUT 3: multiallelic Ti/Tv, QUAL=0, and FILTER semantics ===\n'
/usr/bin/python3 "$RUN/vcf_stats.source-copy.py" "$OUT/core_regression.vcf.gz" > "$OUT/input3_core_vcf_stats.txt"
bcftools stats "$OUT/core_regression.vcf.gz" > "$OUT/input3_core_bcftools.stats.txt"
input3_ts=$(awk -F '\t' '/^TSTV/{print $3; exit}' "$OUT/input3_core_bcftools.stats.txt")
input3_tv=$(awk -F '\t' '/^TSTV/{print $4; exit}' "$OUT/input3_core_bcftools.stats.txt")
input3_strict=$(bcftools view -f PASS -H "$OUT/core_regression.vcf.gz" | wc -l)
input3_notfailed=$(bcftools view -f .,PASS -H "$OUT/core_regression.vcf.gz" | wc -l)
check 'example counts every multiallelic SNP alternate allele' grep -Eq 'Transitions:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'example counts both multiallelic transversions' grep -Eq 'Transversions:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'bcftools independently agrees on two transitions' test "$input3_ts" -eq 2
check 'bcftools independently agrees on two transversions' test "$input3_tv" -eq 2
check 'QUAL=0 is retained in the three-observation mean of 20.0' grep -Eq 'Mean QUAL:[[:space:]]+20\.0$' "$OUT/input3_core_vcf_stats.txt"
check 'example distinguishes strict PASS from unfiltered-dot records' grep -Eq 'PASS variants:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'strict PASS count is two' test "$input3_strict" -eq 2
check 'not-failed PASS-or-dot count is three' test "$input3_notfailed" -eq 3
value "input3 bcftools_ts=$input3_ts bcftools_tv=$input3_tv strict_pass=$input3_strict not_failed=$input3_notfailed"

printf '\n=== INPUT 4: empty and zero-transversion edge records ===\n'
/usr/bin/python3 "$RUN/vcf_stats.source-copy.py" "$OUT/empty.vcf.gz" > "$OUT/input4_empty.txt"
/usr/bin/python3 "$RUN/vcf_stats.source-copy.py" "$OUT/transitions_only.vcf.gz" > "$OUT/input4_transitions_only.txt"
check 'empty VCF completes with zero records' grep -Eq 'Total variants:[[:space:]]+0$' "$OUT/input4_empty.txt"
check 'empty VCF emits no fabricated mean quality' bash -c "! grep -q 'Mean QUAL' '$OUT/input4_empty.txt'"
check 'transition-only VCF retains QUAL=0 in mean 5.0' grep -Eq 'Mean QUAL:[[:space:]]+5\.0$' "$OUT/input4_transitions_only.txt"
check 'transition-only output reports the two transitions' grep -Eq 'Transitions:[[:space:]]+2$' "$OUT/input4_transitions_only.txt"
check 'transition-only output reports zero transversions' grep -Eq 'Transversions:[[:space:]]+0$' "$OUT/input4_transitions_only.txt"

printf '\n=== INPUT 5: missingness and exact-HWE cohort workflow ===\n'
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --missing-indv --out "$OUT/input5_sample_miss" > "$OUT/input5_missing_indv.log" 2>&1
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --missing-site --out "$OUT/input5_site_miss" > "$OUT/input5_missing_site.log" 2>&1
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --hardy --out "$OUT/input5_hwe" > "$OUT/input5_hwe.log" 2>&1
/usr/bin/python3 "$RUN/validate_missingness.py" "$DATA/cohort.vcf" "$OUT/input5_sample_miss.imiss" "$OUT/input5_site_miss.lmiss" > "$OUT/input5_missingness_validation.txt"
check 'VCFtools per-sample missingness has eight data rows' test "$(($(wc -l < "$OUT/input5_sample_miss.imiss") - 1))" -eq 8
check 'VCFtools per-site missingness has 361 data rows' test "$(($(wc -l < "$OUT/input5_site_miss.lmiss") - 1))" -eq 361
check 'independent parser matches every sample and site missingness value' grep -Fq 'PASS missingness: 8 samples and 361 sites' "$OUT/input5_missingness_validation.txt"
check 'exact-HWE workflow emits one row per cohort site' test "$(($(wc -l < "$OUT/input5_hwe.hwe") - 1))" -eq 361

printf '\n=== INPUT 6: caller comparison and regional stratification ===\n'
bcftools stats "$OUT/callerA.vcf.gz" "$OUT/callerB.vcf.gz" > "$OUT/input6_callers_comparison.stats.txt"
bcftools stats -R "$DATA/easy_regions.bed" "$OUT/cohort.vcf.gz" > "$OUT/input6_easy.stats.txt"
bcftools stats -R "$DATA/difficult_regions.bed" "$OUT/cohort.vcf.gz" > "$OUT/input6_difficult.stats.txt"
caller_a_count=$(bcftools view -H "$OUT/callerA.vcf.gz" | wc -l)
caller_b_count=$(bcftools view -H "$OUT/callerB.vcf.gz" | wc -l)
comparison_ids=$(awk -F '\t' '$1=="ID" {n++} END {print n+0}' "$OUT/input6_callers_comparison.stats.txt")
easy_count=$(awk -F '\t' '$1=="SN" && $3=="number of records:" {print $4; exit}' "$OUT/input6_easy.stats.txt")
difficult_count=$(awk -F '\t' '$1=="SN" && $3=="number of records:" {print $4; exit}' "$OUT/input6_difficult.stats.txt")
check 'caller A fixture is non-empty' test "$caller_a_count" -gt 0
check 'caller B fixture is non-empty' test "$caller_b_count" -gt 0
check 'two-callset statistics contains three ID classes' test "$comparison_ids" -eq 3
check 'regional record counts partition all 361 cohort sites' test "$((easy_count + difficult_count))" -eq 361
check 'both regional strata contain records' test "$easy_count" -gt 0
check 'both regional strata contain records independently' test "$difficult_count" -gt 0
value "input6 callerA=$caller_a_count callerB=$caller_b_count comparison_ids=$comparison_ids easy=$easy_count difficult=$difficult_count"

printf '\n=== INPUT 7: identity and relatedness workflow ===\n'
bcftools gtcheck "$OUT/cohort.vcf.gz" > "$OUT/input7_gtcheck.txt" 2> "$OUT/input7_gtcheck.stderr.txt"
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --relatedness2 --out "$OUT/input7_kin" > "$OUT/input7_relatedness.log" 2>&1
gt_pairs=$(grep -c '^DC' "$OUT/input7_gtcheck.txt")
kin_pairs=$(($(wc -l < "$OUT/input7_kin.relatedness2") - 1))
check 'gtcheck emits all 28 unordered sample pairs' test "$gt_pairs" -eq 28
check 'KING-robust relatedness emits the full 8-by-8 matrix' test "$kin_pairs" -eq 64
check 'gtcheck reports 361 sites compared' grep -Fq $'INFO\tsites-compared\t361' "$OUT/input7_gtcheck.txt"
check 'relatedness output retains eight distinct sample IDs' test "$(tail -n +2 "$OUT/input7_kin.relatedness2" | cut -f1,2 | tr '\t' '\n' | sort -u | wc -l)" -eq 8
value "input7 gtcheck_pairs=$gt_pairs king_pairs=$kin_pairs"

printf '\nSUMMARY | %s/%s shell-level checks passed\n' "$passes" "$checks"
printf 'NOTE | Deliberate edge assertions may fail and are audit findings, not harness errors.\n'
