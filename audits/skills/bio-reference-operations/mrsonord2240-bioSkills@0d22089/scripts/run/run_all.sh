#!/bin/bash
# Runs every WSL test in order from clean work dirs and writes logs/*.txt (the logs in this folder come from one pass of this script).
R=/mnt/openscience/audits/bio-reference-operations/run
cd $R
python extract_snippets.py skill snippets > logs/extract_snippets.txt
bash h1_help.sh > logs/h1_help.txt 2>&1
python make_planted.py data/planted > logs/make_planted.txt 2>&1
bash r1_prepare.sh > logs/r1_prepare.txt 2>&1
bash r1_consume.sh > logs/r1_consume.txt 2>&1
python r1_check.py > logs/r1_check.txt 2>&1
bash r1c_picard_dict.sh > logs/r1c_picard_dict.txt 2>&1
python r2_extract.py > logs/r2_extract.txt 2>&1
python r3_contigs.py > logs/r3_contigs.txt 2>&1
python r4_real_consensus.py > logs/r4_real_consensus.txt 2>&1
python r6_planted.py > logs/r6_planted.txt 2>&1
python r7_rename_order.py > logs/r7_rename_order.txt 2>&1
python r8_modes.py > logs/r8_modes.txt 2>&1
bash r9_misc.sh > logs/r9_misc.txt 2>&1
bash r10_blocks.sh > logs/r10_blocks.txt 2>&1
echo done
