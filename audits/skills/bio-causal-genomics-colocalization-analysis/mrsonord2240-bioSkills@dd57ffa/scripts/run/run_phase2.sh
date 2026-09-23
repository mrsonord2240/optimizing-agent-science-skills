#!/usr/bin/env bash
set -euo pipefail
# R 4.4.3 on this Windows/MSYS seat occasionally returns 139 after a completed
# coloc call.  Keep executing independent audit inputs and inspect/assert files,
# rather than mistaking that post-output wrapper status for scientific evidence.
set +e
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
rsh="F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh"
cd "$root"

"$rsh" input1_legacy_canonical_coloc.R > input1_output.txt 2>&1
cd "$root/skill_snapshot"
"$rsh" examples/coloc_susie.R > "$root/input2_shipped_susie_output.txt" 2>&1
"$rsh" examples/coloc_susie_multicausal.R > "$root/input3_shipped_multicausal_output.txt" 2>&1
cd "$root"
"$rsh" input4_legacy_region_gate.R > input4_output.txt 2>&1

mkdir -p input5_smr
cp input5_legacy_smr_prep.R input5_smr/input5_smr_prep.R
cd input5_smr
mkdir -p smr_test
"$rsh" input5_smr_prep.R > "$root/input5_prep_output.txt" 2>&1
cd "$root"
bash run_input5_smr.sh > input5_smr_output.txt 2>&1

"$rsh" input6_legacy_pph3_lowpower.R > input6_output.txt 2>&1
"$rsh" input7_current_harmonise.R "$root/skill_snapshot/scripts/harmonise.R" > input7_output.txt 2>&1

"$rsh" input8_make_abf_inputs.R "$root/input8_abf" > input8_prep_output.txt 2>&1
cd "$root/skill_snapshot"
"$rsh" scripts/coloc_abf.R "$root/input8_abf/gwas.tsv" "$root/input8_abf/eqtl.tsv" --gwas-type cc --gwas-s 0.3 --gwas-n 50000 --eqtl-type quant --eqtl-sdy 1 --eqtl-n 500 --p12 5e-6 --out "$root/input8_abf/coloc" > "$root/input8_output.txt" 2>&1
cd "$root"

"$rsh" input9_make_susie_inputs.R "$root/input9_susie" > input9_prep_output.txt 2>&1
cd "$root/skill_snapshot"
"$rsh" scripts/coloc_susie.R "$root/input9_susie/gwas.tsv" "$root/input9_susie/eqtl.tsv" "$root/input9_susie/ld.tsv" --gwas-type cc --gwas-s 0.3 --gwas-n 1800 --eqtl-type quant --eqtl-sdy 1 --eqtl-n 1800 --L 10 --out "$root/input9_susie/coloc" > "$root/input9_output.txt" 2>&1

"$rsh" examples/coloc_analysis.R > "$root/supplemental_coloc_analysis_output.txt" 2>&1
mkdir -p "$root/supplemental_plots"
cd "$root/supplemental_plots"
"$rsh" "$root/skill_snapshot/examples/regional_plots.R" > "$root/supplemental_regional_plots_output.txt" 2>&1
