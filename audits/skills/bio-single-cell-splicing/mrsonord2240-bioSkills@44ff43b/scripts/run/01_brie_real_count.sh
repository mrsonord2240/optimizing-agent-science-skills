#!/bin/bash
# Input 1 step A: follow the Skill's BRIE2 CLI literally on the REAL cached Smart-seq2 data (mouse E6.5, 130 cells).
# Skill line: brie-count -a splicing_events.gff3 -S sample_list.tsv -o brie_counts/ -p 16
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
cd $R/data/real
rm -rf $R/out/real_counts
time brie-count -a mouse_SE.lenient_50events.gff3 -S cell_table.tsv -o $R/out/real_counts -p 16
ls -la $R/out/real_counts
