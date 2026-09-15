#!/bin/bash
# Input 5 - Skill decision-tree row "Large cohort: DIA-NN --reanalyse, filter on Global.PG.Q.Value" (NOT executed).
diann --dir plasma_600_d/ \
    --lib plasma.predicted.speclib --fasta uniprot_human_reviewed.fasta \
    --out diann_out/report.parquet --qvalue 0.01 --matrices \
    --mass-acc 0 --reanalyse --smart-profiling --threads 32
# DIA-NN docs (master README, lines 93-112, 678, 684, 848) instead recommend for this design: fixed --mass-acc 15
# --mass-acc-ms1 15 on timsTOF, and an empirical library from 20-100 good runs, then all 600 runs searched with it (MBR off).
