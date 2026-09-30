#!/bin/bash
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
python $A/scripts/a7b_qc_profiles.py $W/a1 $W/a7 $A/out/a7_ctcf_profiles.png
