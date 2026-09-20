#!/bin/bash
# Probe installed CLI help for every flag the Skill documents (auditor script)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
O=/mnt/openscience/audits/bio-long-read-splicing/run/logs
LR="micromamba run -n as-lr"
SQ="micromamba run -n as-sqanti"
$LR flair --version > $O/flair_version.txt 2>&1
for m in align correct collapse quantify diffsplice diffSplice transcriptome; do $LR flair $m --help > $O/flair_${m}_help.txt 2>&1; done
$LR isoquant --help > $O/isoquant_help.txt 2>&1
$LR isoquant --version > $O/isoquant_version.txt 2>&1
$LR which isoquant.py > $O/isoquant_py_which.txt 2>&1; 
$SQ sqanti3_qc.py --help > $O/sqanti_qc_help.txt 2>&1
$SQ sqanti3_filter.py rules --help > $O/sqanti_filter_rules_help.txt 2>&1
$SQ sqanti3_filter.py --help > $O/sqanti_filter_help.txt 2>&1
micromamba run -n as-rmatslong rmats-long rmats_long.py --help > $O/rmatslong_help.txt 2>&1
minimap2 --version > $O/minimap2_version.txt 2>&1
$LR minimap2 --version >> $O/minimap2_version.txt 2>&1
for t in skera lima isoseq isoseq3 match_cell_barcode FLAMES uLTRA desalt gffread; do echo "$t: $(micromamba run -n as-lr which $t 2>&1 | tail -1) | $(micromamba run -n as-sqanti which $t 2>&1|tail -1) | $(micromamba run -n as-core which $t 2>&1|tail -1)"; done > $O/tool_presence.txt
