#!/bin/bash
# A9: does the documented conda install of rgt give a runnable rgt-hint without extra data setup? (no RGTDATA set)
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
unset RGTDATA; cd $W/a5
mkdir -p hint_nodata
micromamba run -n $P-rgt rgt-hint footprinting --atac-seq --paired-end --organism=hg38 --output-location=hint_nodata --output-prefix=t w.bam pk60.bed > hint_nodata.log 2>&1; echo "rgt-hint without RGTDATA rc=$?"
tail -n 6 hint_nodata.log | cut -c1-200; ls hint_nodata | wc -l
micromamba run -n $P-rgt python -c "import os,rgt;print('rgt pkg dir:',os.path.dirname(rgt.__file__));print(os.listdir(os.path.expanduser('~/rgtdata')) if os.path.isdir(os.path.expanduser('~/rgtdata')) else 'no ~/rgtdata')" 2>&1 | tail -n 3
