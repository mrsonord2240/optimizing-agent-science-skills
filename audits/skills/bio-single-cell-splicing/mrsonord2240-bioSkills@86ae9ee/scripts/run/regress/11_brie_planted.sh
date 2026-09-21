#!/bin/bash
# Input 2: Skill's BRIE2 CLI on PLANTED Smart-seq-like data (synthetic). Flags exactly as in SKILL.md.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
D=$R/data/synth_ss2; O=$R/out/planted_ss2; rm -rf $O; mkdir -p $O
cd $D
brie-count -a events.gff3 -S cell_table.tsv -o $O/counts -p 16 2>&1 | tr '\r' '\n' | grep -v "cells done" | tail -5
brie-quant -i $O/counts/brie_count.h5ad -c cellfeat.tsv -o $O/quant.h5ad --interceptMode gene --LRTindex All --testBase null --MCsize 3 -p 16 2>&1 | tr '\r' '\n' | grep -E "BRIE2|Filtered|Error|error|Traceback" | tail -12
ls -la $O
