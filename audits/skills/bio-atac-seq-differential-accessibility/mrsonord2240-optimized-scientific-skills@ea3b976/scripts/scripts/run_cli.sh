#!/bin/bash
# reaudit CLI cases. usage: bash run_cli.sh <case>
S=/mnt/openscience/wt/atac-differential-accessibility/skills/bio-atac-seq-differential-accessibility/scripts/diff_accessibility.R
D=/mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run
export PATH=/home/sci/.local/bin:$PATH MAMBA_ROOT_PREFIX=/home/sci/micromamba
W=$D/work/$1; rm -rf $W; mkdir -p $W; cd $W
R="micromamba run -n bio-atac-seq-differential-accessibility Rscript $S"
case $1 in
 default) $R ../samples.csv d --cores=4 ;;
 native)  $R ../samples.csv n native --cores=4 ;;
 args)    $R ../samples.csv mypfx lib 0.01 3 --cores=4 ;;
 edger)   $R ../samples.csv e lib 0.05 1 --method=edger --cores=4 ;;
 design)  $R ../samples_tissue.csv des lib 0.05 1 '--design=~Tissue + Condition' --cores=4 ;;
 sva)     $R ../samples.csv s lib 0.05 1 --sva=2 --cores=4 ;;
 sva1)    $R ../samples.csv s1 lib 0.05 1 --sva=1 --cores=4 ;;
 svanull) $R ../samples.csv sn lib 0.05 10 --sva=1 --cores=4 ;;
 sva4)    $R ../samples.csv s4 lib 0.05 1 --sva=4 --cores=4 ;;
 null)    $R ../samples.csv nl lib 0.05 10 --cores=4 ;;
 labels)  $R ../samples_labels.csv lb lib 0.05 1 --cores=4 ;;
 labels_ok) $R ../samples_labels.csv lo lib 0.05 1 --case=K562 --control=GM12878 --cores=4 ;;
 notxdb)  $R ../samples.csv nt lib 0.05 1 --txdb=none --cores=4 ;;
 designbad) $R ../samples_batch.csv db lib 0.05 1 '--design=~Batch + Condition' --cores=4 ;;
 badarg)  $R ../samples.csv x lib 0.05 1 --bogus=1 ;;
 badnum)  $R ../samples.csv x lib abc 1 ;;
esac
echo "RC=$?"
