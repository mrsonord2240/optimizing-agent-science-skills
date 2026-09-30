#!/bin/bash
# usage: run_py.sh <script.py>  (runs inside audit env with RUN/EG set)
source /mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/initial-audit-20260930/scripts/common.sh
python "$RUN/scripts/$1"
