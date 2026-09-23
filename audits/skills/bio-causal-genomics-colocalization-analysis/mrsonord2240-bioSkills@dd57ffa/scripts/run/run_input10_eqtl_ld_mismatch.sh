#!/usr/bin/env bash
set -euo pipefail
set +e
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
rsh="F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh"
"$rsh" "$root/input10_make_eqtl_ld_mismatch.R" "$root/input9_susie" "$root/input10_eqtl_mismatch" > "$root/input10_prep_output.txt" 2>&1
cd "$root/skill_snapshot"
"$rsh" scripts/coloc_susie.R "$root/input10_eqtl_mismatch/gwas.tsv" "$root/input10_eqtl_mismatch/eqtl.tsv" "$root/input10_eqtl_mismatch/ld.tsv" --gwas-type cc --gwas-s 0.3 --gwas-n 1800 --eqtl-type quant --eqtl-sdy 1 --eqtl-n 1800 --L 10 --out "$root/input10_eqtl_mismatch/coloc" > "$root/input10_output.txt" 2>&1
printf 'source_script_exit=%s\n' "$?" >> "$root/input10_output.txt"
