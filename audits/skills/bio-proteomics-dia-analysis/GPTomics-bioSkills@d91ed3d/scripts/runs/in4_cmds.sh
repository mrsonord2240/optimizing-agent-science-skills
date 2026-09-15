#!/bin/bash
# Input 4 - agent output following SKILL.md "Generating a Predicted Library Outside DIA-NN" + "Library-Based Route".
# The easypqp line WAS executed (sandbox, see in4_easypqp_stdout.txt) and exits 1. DIA-NN NOT executed.
easypqp library \
    --psmtsv psm.tsv \
    --rt_reference irt.tsv \
    --peptide_fdr_threshold 0.01 \
    --protein_fdr_threshold 0.01 \
    --out library.tsv
diann \
    --f C1_DIA.mzML --f C2_DIA.mzML --f C3_DIA.mzML --f C4_DIA.mzML \
    --f T1_DIA.mzML --f T2_DIA.mzML --f T3_DIA.mzML --f T4_DIA.mzML \
    --lib library.tsv \
    --out diann_out/report.parquet \
    --qvalue 0.01 --matrices \
    --mass-acc 0 \
    --reanalyse --smart-profiling \
    --threads 8
