#!/bin/bash
# A3b: assertions on the NFR-BAM run (A3): same biology checks as A1; CTCF dip on NFR-corrected signal.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
cd $W/a3
python $A/scripts/check_bindetect.py out/bindetect/bindetect_results.txt | tail -n 8
python $A/scripts/check_ctcf_profile.py out $A/out/a3_nfr_ctcf_profile.png
echo "--- full-fragment (A1) vs NFR (A3): total reads and CTCF bound-site counts"
for r in a1 a3; do echo "$r: cond1 bound CTCF_MA0139.2 sites=$(wc -l < $W/$r/out/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_cond1_bound.bed)"; done
