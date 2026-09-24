#!/bin/bash
# Driver: every script in this folder was executed (logs sit beside them). R goes through the env's r.sh; WSL through wsl_run.sh.
# Regression scripts (10-82) are the first re-auditor's scripts adapted to the round-2 SKILL.md (block indices remapped: r_01 workflow,
# r_02 permutation check, r_03 consequences, r_04 manual DTU, r_05 confirm, r_06 swish). 9x scripts are NEW in this audit.
# work/ (staged copies, .rds, sequences, real GTF/FASTA copies) and big generated data were deleted after the run.
export PYTHONIOENCODING=utf-8
R=F:/OpenScience/audit-envs/alternative-splicing/r.sh; W=F:/OpenScience/audit-envs/alternative-splicing/wsl_run.sh
cd F:/OpenScience/audits/bio-isoform-switching/run; mkdir -p work
python 03_extract_blocks.py
bash $R 02_gen_synth.R
bash $R 04_gen_new.R data/new1 8801 4 7 batch
bash $R 04_gen_new.R data/new2 8802 5 5
chainA() {
bash $R 10_input1_canonical.R   > 10_input1.log 2>&1
bash $R 20_input2_manual_dtu.R  > 20_input2.log 2>&1
bash $R 30_input3_real_chrX.R   > 30_input3.log 2>&1
bash 35_example_runs.sh > 35_example_runs.log 2>&1
bash $R skill/examples/isoform_switch_analysis.R > 35a_demo_rerun.log 2>&1
bash $R 40a_input4_prep.R       > 40a.log 2>&1
bash $W 'bash /mnt/openscience/audits/bio-isoform-switching/run/40b_external.sh' > 40b_external.log 2>&1
bash $R 40c_consequences.R      > 40c.log 2>&1
bash $R 40d_real_consequences.R > 40d.log 2>&1
bash $R 41_orf_overwrite_check.R > 41.log 2>&1
bash $R 50_input5_stress_adversarial.R > 50_input5.log 2>&1
}
chainB() {
bash $R 60_input6_swish.R       > 60_input6.log 2>&1
bash $R 61_tximeta_warning.R    > 61_tximeta_warning.log 2>&1
bash $R 62_isar_news.R          > 62_isar_news.log 2>&1
bash 63_converter_checks.sh     > 63_converter_checks.log 2>&1
bash $R 64_isar_source_dump.R   > 64_isar_source_dump.log 2>&1
bash $R 65_common_errors_rest.R > 65_common_errors_rest.log 2>&1
bash $R 70_input7_new_count_route.R > 70_input7.log 2>&1
bash $R 71_real_label_permutation.R > 71.log 2>&1
bash $R 72_efflen_factor.R      > 72_efflen_factor.log 2>&1
bash $R 80_input8_new_unbalanced.R > 80_input8.log 2>&1
bash 81_input8_example.sh
bash $R 82_eval_example_new.R   > 82_eval_example_new.log 2>&1
}
chainA & chainB & wait

# ---- scripts new in this re-audit (run after the regression driver above; logs beside them) ----
bash 00_download_clans.sh                       # Pfam-A.clans.tsv.gz for 40b_external.sh (run BEFORE chainA in practice)
bash 90_gen_het_data.sh                         # NEW synthetic sets (05_gen_het.R): het_null, het_3v3, het_6v6, odd_3v5
bash $R 91_input9_het_null.R      > 91_input9.log 2>&1
bash $R 92_input10_odd_ids_unbalanced.R > 92_input10.log 2>&1
bash $R 92b_perm_block_unbalanced.R > 92b_perm_block_unbalanced.log 2>&1
bash $R 94_odd_id_probe.R         > 94_odd_id_probe.log 2>&1
bash $R 95_odd_id_workaround.R    > 95_odd_id_workaround.log 2>&1
bash 93_input10_example.sh        > 93_input10_example.out 2>&1
bash $R 93b_eval_example_odd.R    > 93b_eval_example_odd.log 2>&1
bash $R 93c_id_error_message.R    > 93c_id_error_message.log 2>&1
bash $R 96_null_table_real_chrX.R > 96_null_table.log 2>&1
bash $R 97_install_isar212.R      > 97_install_isar212.log 2>&1      # fails: 2.12.0 needs Seqinfo (Bioc 3.22+)
bash 98_isar_newer_source.sh      > 98_isar_newer_source.log 2>&1
bash $R 99b_isar_part1_autoselect.R > 99b_isar_part1_autoselect.log 2>&1
bash $R 99c_sva_seed_determinism.R > 99c_sva_seed_determinism.log 2>&1
bash $R 99d_sva_seed_3v3.R        > 99d_sva_seed_3v3.log 2>&1
python 90_build_report.py; python 91_build_viewer.py
# Deleted after the run: work/ (377 MB), data/*/salmon_quant, GTF/FASTA (regenerate with the generators); truth tables kept.
