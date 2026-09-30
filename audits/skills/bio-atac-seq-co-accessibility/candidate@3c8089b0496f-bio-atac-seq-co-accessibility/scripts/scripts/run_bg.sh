#!/bin/bash
# usage: run_bg.sh <script.R> <timeout-sec> <logname>
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
LOG=/mnt/openscience/audits/bio-atac-seq-co-accessibility/runs/$3
echo START $(date -Is) > $LOG
timeout $2 micromamba run -n bio-atac-seq-co-accessibility Rscript $1 >> $LOG 2>&1
echo EXIT $? $(date -Is) >> $LOG
