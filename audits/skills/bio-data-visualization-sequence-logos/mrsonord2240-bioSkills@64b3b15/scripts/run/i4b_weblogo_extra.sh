#!/bin/bash
export PATH=/home/sci/micromamba/envs/dv-cli/bin:$PATH
cd /mnt/openscience/audits/bio-data-visualization-sequence-logos/run/out/wl   # n20.fa / n2000.fa are written by i4c_weblogo_check.py (plain FASTA from data/dna_n*.txt)
W=weblogo
$W --format logodata --sequence-type dna --units bits --composition "H. sapiens" --weight 0 < n200.fa > n200.human.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition "{'A':0.18,'C':0.32,'G':0.32,'T':0.18}" --weight 0 < gc500.fa > gc500.dict.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 < gc500.fa > gc500.equi.w0.logodata 2>/dev/null
$W --format logodata --sequence-type protein --units bits --composition equiprobable --weight 0 < prot200.fa > prot200.equi.w0.logodata 2>/dev/null
$W --format logodata --sequence-type protein --units bits --composition auto --weight 0 < prot200.fa > prot200.auto.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 < n5.fa > n5.equi.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 < n20.fa > n20.equi.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable < n20.fa > n20.equi.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable --weight 0 < n2000.fa > n2000.equi.w0.logodata 2>/dev/null
$W --format logodata --sequence-type dna --units bits --composition equiprobable < n2000.fa > n2000.equi.logodata 2>/dev/null
