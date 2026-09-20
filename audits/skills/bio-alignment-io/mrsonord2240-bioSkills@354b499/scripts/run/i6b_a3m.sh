#!/bin/bash
# REAL data: Pfam seed (aligned fasta) -> A3M (HH-suite reformat.pl, first sequence as match reference) -> A2M. Then parsed by i6b_a3m.py
D=/mnt/openscience/audits/bio-alignment-io/run/data
which reformat.pl hhfilter
sed 's/\./-/g' $D/pf.fasta > $D/pf_dash.fas
reformat.pl fas a3m $D/pf_dash.fas $D/pf.a3m -M first >/dev/null 2>&1 </dev/null
reformat.pl a3m a2m $D/pf.a3m $D/pf.a2m >/dev/null 2>&1 </dev/null
ls -l $D/pf.a3m $D/pf.a2m
head -4 $D/pf.a3m | cut -c1-100
