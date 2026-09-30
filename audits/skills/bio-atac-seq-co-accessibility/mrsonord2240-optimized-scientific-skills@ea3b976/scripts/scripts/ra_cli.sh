#!/bin/bash
# Re-audit: shipped CLI on a real 3-chromosome pattern-format .mtx + 4th-arg TSS BED
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
W=$CO/work/reaudit/cli; rm -rf $W; mkdir -p $W; cd $W
I=$CO/work/reaudit/input
TSS=$ATACDATA/annotation/gencode_v29_protein_coding_tss.chr1.bed
date -Is; time micromamba run -n bio-atac-seq-co-accessibility Rscript $SKILL/scripts/cicero_workflow.R $I/peak_matrix.mtx $I/peak_metadata.tsv $I/cell_metadata.tsv $TSS
echo CLI_EXIT $?; date -Is; ls -l
