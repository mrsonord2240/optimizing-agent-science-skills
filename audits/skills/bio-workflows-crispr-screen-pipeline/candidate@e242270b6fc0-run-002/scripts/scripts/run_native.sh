#!/bin/bash
# Audit run: native-Windows routes, commands as in route files. Run from run root.
set -u
export PATH=/f/OpenScience/audit-envs/crispr-screen-analyst/Scripts:$PATH
SK=/f/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
D=/f/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline
T=/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl
R=$(pwd)/work; mkdir -p $R
# count (route text literal library columns: sgRNA,Gene,Sequence -> trap), then mageck order
mkdir -p $R/count_literal $R/count; cd $R/count_literal
awk -F, 'BEGIN{OFS=","}{print $1,$3,$2}' $D/count/library.csv > library.csv
mageck count --list-seq library.csv --sample-label Plasmid,Day18_r1,Day18_r2,Day18_r3 --fastq $D/count/Plasmid.fastq.gz $D/count/Day18_r1.fastq.gz $D/count/Day18_r2.fastq.gz $D/count/Day18_r3.fastq.gz --norm-method median --output-prefix experiment --trim-5 5 > log 2>&1; echo "count_literal exit $?"
cd $R/count
mageck count --list-seq $D/count/library.csv --sample-label Plasmid,Day18_r1,Day18_r2,Day18_r3 --fastq $D/count/Plasmid.fastq.gz $D/count/Day18_r1.fastq.gz $D/count/Day18_r2.fastq.gz $D/count/Day18_r3.fastq.gz --norm-method median --output-prefix experiment --trim-5 5 > log 2>&1; echo "count exit $?"
# qc
mkdir -p $R/qc; cd $R/qc
python $SK/scripts/qc.py $D/qc/hap1.count.txt qc.tsv plasmid=HAP1_T0 > log 2>&1; echo "qc exit $?"
# rra
mkdir -p $R/rra; cd $R/rra
python $SK/scripts/rra.py $D/rra/hap1.count.txt essentiality_rra treatment=HAP1_T18A,HAP1_T18B,HAP1_T18C control=HAP1_T0 > log 2>&1; echo "rra exit $?"
# bagel2
mkdir -p $R/bagel2; cd $R/bagel2
B=$T/bagel/BAGEL.py
python $B fc -i $D/bagel2/hap1.count.txt -o experiment -c HAP1_T0 --min-reads 30 > log 2>&1; echo "fc exit $?"
python $B bf -i experiment.foldchange -o bayes_factor.txt -e $D/bagel2/CEGv2.txt -n $D/bagel2/NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C --seed 42 >> log 2>&1; echo "bf exit $?"
python $B pr -i bayes_factor.txt -o pr_curve.txt -e $D/bagel2/CEGv2.txt -n $D/bagel2/NEGv1.txt >> log 2>&1; echo "pr exit $?"
# drugz
mkdir -p $R/drugz; cd $R/drugz
python $T/drugz/drugz.py -i $D/drugz/screen.count.txt -o drugz_output.txt -c Veh_r1,Veh_r2 -x Drug_r1 -p 5 -unpaired > log 2>&1; echo "drugz exit $?"
# mle
mkdir -p $R/mle; cd $R/mle
mageck mle --count-table $D/mle/leukemia.count.txt --design-matrix $D/mle/designmat.txt --output-prefix timecourse_mle --norm-method median --permutation-round 10 > log 2>&1; echo "mle exit $?"
