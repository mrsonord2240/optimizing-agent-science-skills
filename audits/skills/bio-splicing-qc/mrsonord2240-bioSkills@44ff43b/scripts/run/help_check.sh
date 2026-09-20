#!/bin/bash
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
for t in junction_annotation.py junction_saturation.py infer_experiment.py geneBody_coverage.py; do echo "=== $t"; $t --help 2>&1 | head -40; done
echo "=== STAR params"
STAR --parametersDefault 2>&1 | grep -E "^(alignIntronMax|alignSJoverhangMin|alignSJDBoverhangMin|sjdbOverhang|limitSjdbInsertNsj|outSJtype|winBinNbits|winAnchorDistNbins|outSJfilter|twopass)" 
STAR --help 2>&1 | grep -E -A3 "^alignIntronMax|^alignSJoverhangMin|^limitSjdbInsertNsj|^outSJtype|^sjdbFileChrStartEnd"
