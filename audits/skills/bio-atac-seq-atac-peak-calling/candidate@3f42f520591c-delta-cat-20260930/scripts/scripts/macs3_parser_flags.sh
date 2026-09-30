#!/usr/bin/env bash
# Static check of how the Skill env's MACS3 3.0.4 BAMPE parser filters reads by SAM flag,
# and which parser `macs3 hmmratac -f BAMPE` uses.
SP=/home/sci/micromamba/envs/bio-atac-seq-atac-peak-calling/lib/python3.10/site-packages/MACS3
echo "== Parser.py flag filter used by bampe_pe_binary_parse"
awk '/def bampe_pe_binary_parse/{f=1} f{print NR": "$0; n++} n>40{exit}' $SP/IO/Parser.py
echo "== hmmratac parser selection"
grep -n -E "Parser|BAMPE|format" $SP/Commands/hmmratac_cmd.py | head -20
