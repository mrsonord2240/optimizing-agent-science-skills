#!/bin/bash
# Re-audit stress: shipped CLI on the 1726 peaks x 3277 cells real PBMC 5k chr1:1-30Mb slice (pattern-format .mtx), chr1 TSS BED
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
W=$CO/work/reaudit/stress; rm -rf $W; mkdir -p $W; cd $W; I=$CO/work/input
head -2 $I/peak_matrix.mtx
date -Is; time micromamba run -n bio-atac-seq-co-accessibility Rscript $SKILL/scripts/cicero_workflow.R $I/peak_matrix.mtx $I/peak_metadata.tsv $I/cell_metadata.tsv $ATACDATA/annotation/gencode_v29_protein_coding_tss.chr1.bed
echo CLI_EXIT $?; date -Is; ls -l
