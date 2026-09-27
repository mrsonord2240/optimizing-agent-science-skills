#!/usr/bin/env bash
set -euo pipefail

readonly BASE='/mnt/openscience/audits/bio-vcf-statistics/reaudit-ffa74e9-20260927'
readonly RUN="$BASE/run"
readonly DATA="$BASE/data"
readonly OUT="$BASE/outputs"
readonly SOURCE='/mnt/openscience/audit-sources/optimized-scientific-skills-ffa74e9/skills/bio-vcf-statistics'
readonly EXPECTED_SHA='ffa74e915d92da714bfd40ce2f0aa1fbb1e2cde4'
readonly VCFTOOLS='/home/sci/micromamba/envs/atac-jvm/bin/vcftools'
readonly PY='/usr/bin/python3'   # has cyvcf2 0.31.4 + numpy 2.5.3; bio env's python3 lacks cyvcf2

mkdir -p "$OUT"

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
"$PY" - <<'PY'
import cyvcf2, numpy
print(f"cyvcf2 {cyvcf2.__version__} numpy {numpy.__version__}")
PY

cp "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py"
sha256sum "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py" > "$OUT/source_copy.sha256"
check 'source example copy is byte-identical' cmp -s "$SOURCE/examples/vcf_stats.py" "$RUN/vcf_stats.source-copy.py"

for stem in cohort callerA callerB core_regression filter_semantics empty transitions_only; do
  bgzip -f -c "$DATA/$stem.vcf" > "$OUT/$stem.vcf.gz"
  bcftools index -f -t "$OUT/$stem.vcf.gz"
done
bgzip -f -c "$DATA/dbsnp_syn.vcf" > "$OUT/dbsnp_syn.vcf.gz" 2>/dev/null || true
if [ -f "$OUT/dbsnp_syn.vcf.gz" ]; then bcftools index -f -t "$OUT/dbsnp_syn.vcf.gz" 2>/dev/null || true; fi

printf '\n=== INPUT 1 (regression, Canonical): prior cohort statistics ===\n'
bcftools stats -s - "$OUT/cohort.vcf.gz" > "$OUT/input1_cohort.stats.txt"
"$PY" "$RUN/vcf_stats.source-copy.py" "$OUT/cohort.vcf.gz" > "$OUT/input1_vcf_stats.txt"
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

printf '\n=== INPUT 2 (regression, Variant A): orientation-mixed allele-balance ===\n'
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

printf '\n=== INPUT 3 (regression, Variant B): multiallelic Ti/Tv, QUAL=0, FILTER semantics ===\n'
"$PY" "$RUN/vcf_stats.source-copy.py" "$OUT/core_regression.vcf.gz" > "$OUT/input3_core_vcf_stats.txt"
bcftools stats "$OUT/core_regression.vcf.gz" > "$OUT/input3_core_bcftools.stats.txt"
input3_ts=$(awk -F '\t' '/^TSTV/{print $3; exit}' "$OUT/input3_core_bcftools.stats.txt")
input3_tv=$(awk -F '\t' '/^TSTV/{print $4; exit}' "$OUT/input3_core_bcftools.stats.txt")
input3_strict=$(bcftools view -f PASS -H "$OUT/core_regression.vcf.gz" | wc -l)
input3_notfailed=$(bcftools view -f .,PASS -H "$OUT/core_regression.vcf.gz" | wc -l)
check 'example counts every multiallelic SNP alternate allele (Ts)' grep -Eq 'Transitions:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'example counts both multiallelic transversions' grep -Eq 'Transversions:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'bcftools independently agrees on two transitions' test "$input3_ts" -eq 2
check 'bcftools independently agrees on two transversions' test "$input3_tv" -eq 2
check 'QUAL=0 is retained in the three-observation mean of 20.0' grep -Eq 'Mean QUAL:[[:space:]]+20\.0$' "$OUT/input3_core_vcf_stats.txt"
check 'example PASS label actually mixes strict-PASS and unfiltered-dot (known open P2)' grep -Eq 'PASS variants:[[:space:]]+2$' "$OUT/input3_core_vcf_stats.txt"
check 'strict PASS count is two' test "$input3_strict" -eq 2
check 'not-failed PASS-or-dot count is three' test "$input3_notfailed" -eq 3
value "input3 bcftools_ts=$input3_ts bcftools_tv=$input3_tv strict_pass=$input3_strict not_failed=$input3_notfailed"

printf '\n=== INPUT 4 (regression, Edge): empty VCF + zero-transversion denominator ===\n'
"$PY" "$RUN/vcf_stats.source-copy.py" "$OUT/empty.vcf.gz" > "$OUT/input4_empty.txt"
"$PY" "$RUN/vcf_stats.source-copy.py" "$OUT/transitions_only.vcf.gz" > "$OUT/input4_transitions_only.txt"
check 'empty VCF completes with zero records' grep -Eq 'Total variants:[[:space:]]+0$' "$OUT/input4_empty.txt"
check 'empty VCF emits no fabricated mean quality' bash -c "! grep -q 'Mean QUAL' '$OUT/input4_empty.txt'"
check 'transition-only VCF retains QUAL=0 in mean 5.0' grep -Eq 'Mean QUAL:[[:space:]]+5\.0$' "$OUT/input4_transitions_only.txt"
check 'transition-only output still suppresses both Ts/Tv counts (known open P2)' bash -c "! grep -q 'Transitions:' '$OUT/input4_transitions_only.txt'"

printf '\n=== INPUT 5 (regression, Stress): missingness + exact-HWE cohort workflow ===\n'
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --missing-indv --out "$OUT/input5_sample_miss" > "$OUT/input5_missing_indv.log" 2>&1
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --missing-site --out "$OUT/input5_site_miss" > "$OUT/input5_missing_site.log" 2>&1
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --hardy --out "$OUT/input5_hwe" > "$OUT/input5_hwe.log" 2>&1
"$PY" "$RUN/validate_missingness.py" "$DATA/cohort.vcf" "$OUT/input5_sample_miss.imiss" "$OUT/input5_site_miss.lmiss" > "$OUT/input5_missingness_validation.txt"
check 'VCFtools per-sample missingness has eight data rows' test "$(($(wc -l < "$OUT/input5_sample_miss.imiss") - 1))" -eq 8
check 'VCFtools per-site missingness has 361 data rows' test "$(($(wc -l < "$OUT/input5_site_miss.lmiss") - 1))" -eq 361
check 'independent parser matches every sample and site missingness value' grep -Fq 'PASS missingness: 8 samples and 361 sites' "$OUT/input5_missingness_validation.txt"
check 'exact-HWE workflow emits one row per cohort site' test "$(($(wc -l < "$OUT/input5_hwe.hwe") - 1))" -eq 361

printf '\n=== INPUT 6 (regression, Scope Boundary): caller comparison + regional stratification ===\n'
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
value "input6 callerA=$caller_a_count callerB=$caller_b_count comparison_ids=$comparison_ids easy=$easy_count difficult=$difficult_count"

printf '\n=== INPUT 7 (regression, Adversarial): identity + relatedness completeness ===\n'
bcftools gtcheck "$OUT/cohort.vcf.gz" > "$OUT/input7_gtcheck.txt" 2> "$OUT/input7_gtcheck.stderr.txt"
"$VCFTOOLS" --gzvcf "$OUT/cohort.vcf.gz" --relatedness2 --out "$OUT/input7_kin" > "$OUT/input7_relatedness.log" 2>&1
gt_pairs=$(grep -c '^DC' "$OUT/input7_gtcheck.txt")
kin_pairs=$(($(wc -l < "$OUT/input7_kin.relatedness2") - 1))
check 'gtcheck emits all 28 unordered sample pairs' test "$gt_pairs" -eq 28
check 'KING-robust relatedness emits the full 8-by-8 matrix' test "$kin_pairs" -eq 64
check 'gtcheck reports 361 sites compared' grep -Fq $'INFO\tsites-compared\t361' "$OUT/input7_gtcheck.txt"
value "input7 gtcheck_pairs=$gt_pairs king_pairs=$kin_pairs"

printf '\n=== INPUT 8 (NEW, usage-guide.md-only Python snippets): per-sample genotype distribution + AF spectrum ===\n'
"$PY" "$RUN/snippet_genotype_dist.py" "$OUT/cohort.vcf.gz" > "$OUT/input8_genotype_dist.txt"
"$PY" "$RUN/snippet_af_spectrum.py" "$OUT/core_regression.vcf.gz" > "$OUT/input8_af_spectrum_core.txt"
"$PY" "$RUN/snippet_af_spectrum.py" "$OUT/cohort.vcf.gz" > "$OUT/input8_af_spectrum_cohort.txt"
cat "$OUT/input8_genotype_dist.txt"
cat "$OUT/input8_af_spectrum_core.txt"
cat "$OUT/input8_af_spectrum_cohort.txt"
n_snippet_rows=$(wc -l < "$OUT/input8_genotype_dist.txt")
check 'genotype-distribution snippet emits one row per of eight cohort samples' test "$n_snippet_rows" -eq 8
# independent cross-check: sum HET across snippet output vs bcftools PSC nHets column (col 6, 0-based per bcftools docs: field 3 hom-ref? use header)
bcftools stats -s - "$OUT/cohort.vcf.gz" | awk -F'\t' '$1=="PSC"{print $3, $6}' | sort > "$OUT/input8_psc_het_by_sample.txt"
awk -F': ' '{split($2,a," "); sample=$1; for(i=1;i<=NF;i++) ; }' "$OUT/input8_genotype_dist.txt" > /dev/null
# parse snippet output "SAMPLE: het/hom=R HET=n HOM_ALT=n MISS=n"
awk '{sample=$1; sub(":","",sample); for(i=2;i<=NF;i++){split($i,kv,"="); v[kv[1]]=kv[2]} print sample, v["HET"]}' "$OUT/input8_genotype_dist.txt" | sort > "$OUT/input8_snippet_het_by_sample.txt"
check 'snippet HET counts match bcftools PSC nHets per sample exactly' diff -q <(cut -d' ' -f2 "$OUT/input8_psc_het_by_sample.txt") <(cut -d' ' -f2 "$OUT/input8_snippet_het_by_sample.txt")
value "input8 core_af=$(cat "$OUT/input8_af_spectrum_core.txt") cohort_af=$(cat "$OUT/input8_af_spectrum_cohort.txt")"

printf '\n=== INPUT 9 (NEW, adversarial/organism-scope): novel/known dbSNP stratification on a non-human-labelled fixture, no INFO/AF present ===\n'
# cohort.vcf carries no INFO/AF (real GATK-style INFO fields only: DP,QD,FS,MQ,SOR), so this probes
# whether the Skill's documented novel/known workflow still works without AF, and whether the
# usage-guide trim silently dropped the only copy of this command (it did not -- SKILL.md has it).
grep -q 'novel fraction = records with ID' "$SOURCE/SKILL.md" && novel_cmd_in_skill=1 || novel_cmd_in_skill=0
grep -q 'novel fraction = records with ID' "$SOURCE/usage-guide.md" && novel_cmd_in_guide=1 || novel_cmd_in_guide=0
bcftools annotate -a "$DATA/dbsnp_syn.vcf" -c ID "$OUT/cohort.vcf.gz" -Oz -o "$OUT/input9_annotated.vcf.gz" 2>"$OUT/input9_annotate.stderr.txt"
bcftools index -f -t "$OUT/input9_annotated.vcf.gz"
bcftools view -H "$OUT/input9_annotated.vcf.gz" | awk '{n++; if($3==".") novel++} END{print "novel:", novel/n, "novel_n="novel, "total="n}' > "$OUT/input9_novel_fraction.txt"
cat "$OUT/input9_novel_fraction.txt"
check 'the novel/known dbSNP annotate-and-count command still lives in SKILL.md after the trim' test "$novel_cmd_in_skill" -eq 1
check 'the novel/known command is correctly NOT duplicated in the trimmed usage-guide.md' test "$novel_cmd_in_guide" -eq 0
check 'the annotate+novel-fraction command runs end to end on a real cohort VCF' test -s "$OUT/input9_novel_fraction.txt"
n_annotated=$(bcftools view -H "$OUT/input9_annotated.vcf.gz" | wc -l)
check 'annotation preserves all 361 cohort records' test "$n_annotated" -eq 361

printf '\nSUMMARY | %s/%s shell-level checks passed\n' "$passes" "$checks"
printf 'NOTE | Some deliberate edge assertions are known open P2 findings from the 2026-09-25 audit, not harness errors.\n'
