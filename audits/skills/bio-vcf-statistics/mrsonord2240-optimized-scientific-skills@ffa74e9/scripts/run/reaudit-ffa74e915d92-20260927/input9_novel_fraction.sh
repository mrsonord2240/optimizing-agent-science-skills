#!/usr/bin/env bash
set -euo pipefail
BASE=/mnt/openscience/audits/bio-vcf-statistics/reaudit-ffa74e9-20260927
DATA="$BASE/data"
OUT="$BASE/outputs"
SOURCE=/mnt/openscience/audit-sources/optimized-scientific-skills-ffa74e9/skills/bio-vcf-statistics

checks=0; passes=0
check() { local label="$1"; shift; checks=$((checks+1)); if "$@"; then passes=$((passes+1)); printf 'PASS | %s\n' "$label"; else printf 'FAIL | %s\n' "$label"; fi; }

bgzip -f -c "$DATA/dbsnp_syn.vcf" > "$OUT/dbsnp_syn.vcf.gz"
bcftools index -f -t "$OUT/dbsnp_syn.vcf.gz"

grep -q 'novel fraction = records with ID' "$SOURCE/SKILL.md" && novel_cmd_in_skill=1 || novel_cmd_in_skill=0
grep -q 'novel fraction = records with ID' "$SOURCE/usage-guide.md" && novel_cmd_in_guide=1 || novel_cmd_in_guide=0

bcftools annotate -a "$OUT/dbsnp_syn.vcf.gz" -c ID "$OUT/cohort.vcf.gz" -Oz -o "$OUT/input9_annotated.vcf.gz" 2>"$OUT/input9_annotate.stderr.txt"
bcftools index -f -t "$OUT/input9_annotated.vcf.gz"
bcftools view -H "$OUT/input9_annotated.vcf.gz" | awk '{n++; if($3==".") novel++} END{print "novel:", novel/n, "novel_n="novel, "total="n}' > "$OUT/input9_novel_fraction.txt"
cat "$OUT/input9_novel_fraction.txt"

check 'the novel/known dbSNP annotate-and-count command still lives in SKILL.md after the trim' test "$novel_cmd_in_skill" -eq 1
check 'the novel/known command is correctly not duplicated in the trimmed usage-guide.md' test "$novel_cmd_in_guide" -eq 0
check 'the annotate+novel-fraction command runs end to end on a real cohort VCF' test -s "$OUT/input9_novel_fraction.txt"
n_annotated=$(bcftools view -H "$OUT/input9_annotated.vcf.gz" | wc -l)
check 'annotation preserves all 361 cohort records' test "$n_annotated" -eq 361
n_ided=$(bcftools view -H "$OUT/input9_annotated.vcf.gz" | awk -F'\t' '$3!="."' | wc -l)
check 'at least some dbSNP-overlapping sites were actually annotated (fixture is not a no-op)' test "$n_ided" -gt 0
value_novel=$(awk '{print $2}' "$OUT/input9_novel_fraction.txt")
printf 'VALUE | input9 novel_fraction=%s annotated_ids=%s total=%s\n' "$value_novel" "$n_ided" "$n_annotated"
printf 'SUMMARY9 | %s/%s\n' "$passes" "$checks"
