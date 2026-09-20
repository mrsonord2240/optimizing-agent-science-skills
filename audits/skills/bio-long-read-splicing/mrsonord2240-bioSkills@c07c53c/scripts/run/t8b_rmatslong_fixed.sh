#!/bin/bash
# rMATS-long block verbatim + ONE added line (mkdir -p alignment_info, which the block omits): does it then recover the planted DTU genes?
R=/mnt/openscience/audits/bio-long-read-splicing/run; B=$R/out/blocks; cd $R/out/hifi6/rl
rm -rf gene_info_by_chr alignment_info organized events asm_counts rmats_long_output group1.txt group2.txt
mkdir -p alignment_info
bash $B/rmats-long-for-differential-isoform-anal_1.sh > rmatslong_block_mkdir.log 2>&1; echo "rc=$?"
grep -a -i -E "Traceback|Error" rmatslong_block_mkdir.log | head -5
wc -l rmats_long_output/*.tsv
head -3 rmats_long_output/differential_asms.tsv | cut -c1-300
