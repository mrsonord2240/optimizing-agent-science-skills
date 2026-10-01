#!/bin/bash
f=/home/sci/micromamba/envs/bio-atac-seq-footprinting/lib/python3.10/site-packages/tobias/tools/plot_aggregate.py
[ -f "$f" ] || exit 1; grep -n "flank\|mid\|strand\|outlier\|nanmean\|mean(\|values\|signalmat\|agg" $f | head -80
