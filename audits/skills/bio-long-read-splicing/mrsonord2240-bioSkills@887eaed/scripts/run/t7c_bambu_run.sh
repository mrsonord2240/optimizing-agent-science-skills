#!/bin/bash
# Bambu block on the planted HiFi BAMs (t7a made out/bambu/sample1-3.bam): verbatim (ncore = 8, fails on Windows R) then with ncore = 1; then the truth comparison (t7b_bambu_eval.R). Windows R via r-bambu.sh.
AS=/f/OpenScience/audit-envs/alternative-splicing; cd /f/OpenScience/audits/bio-long-read-splicing/run/out/bambu
cp ../blocks/bambu-for-annotation-aware-discovery-qua_1.R bambu_block_ncore8_verbatim.R
$AS/r-bambu.sh bambu_block_ncore8_verbatim.R > bambu_block_ncore8.log 2>&1; echo "verbatim (ncore=8) exit=$?"; grep -a -m2 "Error" bambu_block_ncore8.log
sed 's/ncore = 8/ncore = 1/' bambu_block_ncore8_verbatim.R > bambu_block.R; rm -rf bambu_output
$AS/r-bambu.sh bambu_block.R > bambu_block.log 2>&1; echo "ncore=1 exit=$?"
$AS/r-bambu.sh /f/OpenScience/audits/bio-long-read-splicing/run/t7b_bambu_eval.R 2>&1 | tail -8
