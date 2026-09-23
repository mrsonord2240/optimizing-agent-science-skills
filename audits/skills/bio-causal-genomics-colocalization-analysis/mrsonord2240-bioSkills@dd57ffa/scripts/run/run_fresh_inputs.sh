#!/usr/bin/env bash
set -euo pipefail
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
rsh="F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh"
script="$root/skill_snapshot/scripts/coloc_susie.R"

set +e
"$rsh" "$root/input11_make_fresh_eqtl_mismatch.R" "$root/input11_fresh_eqtl_mismatch" > "$root/input11_prep_output.txt" 2>&1
prep11_status=$?
"$rsh" "$script" "$root/input11_fresh_eqtl_mismatch/gwas.tsv" "$root/input11_fresh_eqtl_mismatch/eqtl.tsv" "$root/input11_fresh_eqtl_mismatch/ld.tsv" --gwas-type cc --gwas-s 0.3 --gwas-n 1400 --eqtl-type quant --eqtl-sdy 1 --eqtl-n 1400 --L 10 --out "$root/input11_fresh_eqtl_mismatch/coloc" > "$root/input11_output.txt" 2>&1
status=$?
printf 'generator_exit=%s\n' "$prep11_status" >> "$root/input11_prep_output.txt"
printf 'source_script_exit=%s\n' "$status" >> "$root/input11_output.txt"
test "$status" -ne 0
grep -F 'LD reference mismatched to eQTL z-scores' "$root/input11_output.txt"
test ! -e "$root/input11_fresh_eqtl_mismatch/coloc_susie_summary.tsv"

"$rsh" "$root/input12_make_fresh_matched_locus.R" "$root/input12_fresh_matched_locus" > "$root/input12_prep_output.txt" 2>&1
prep12_status=$?
"$rsh" "$script" "$root/input12_fresh_matched_locus/gwas.tsv" "$root/input12_fresh_matched_locus/eqtl.tsv" "$root/input12_fresh_matched_locus/ld.tsv" --gwas-type cc --gwas-s 0.3 --gwas-n 2200 --eqtl-type quant --eqtl-sdy 1 --eqtl-n 2200 --L 10 --out "$root/input12_fresh_matched_locus/coloc" > "$root/input12_output.txt" 2>&1
source12_status=$?
printf 'generator_exit=%s\n' "$prep12_status" >> "$root/input12_prep_output.txt"
printf 'source_script_exit=%s\n' "$source12_status" >> "$root/input12_output.txt"
set -e
test -s "$root/input12_fresh_matched_locus/coloc_susie_summary.tsv"
