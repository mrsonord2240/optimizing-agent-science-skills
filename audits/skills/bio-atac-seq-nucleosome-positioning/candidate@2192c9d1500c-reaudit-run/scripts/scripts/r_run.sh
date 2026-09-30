#!/bin/bash
# usage: r_run.sh <tag> [bed]  -- runs skill R script with lane -r env
export PYTHONDONTWRITEBYTECODE=1 PATH=/home/sci/micromamba/envs/bio-atac-seq-nucleosome-positioning-r/bin:$PATH
TAG=$1; BED=$2
SKILL=/mnt/openscience/wt/atac-nucleosome-positioning/skills/bio-atac-seq-nucleosome-positioning
DATA=/mnt/openscience/audit-envs/atac-seq/public-data
W=/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/reaudit-run/out/r_$TAG; rm -rf $W; mkdir -p $W; cd $W
Rscript -e 'cat(R.version.string,"ATACseqQC",as.character(packageVersion("ATACseqQC")),"ChIPpeakAnno",as.character(packageVersion("ChIPpeakAnno")),"\n")'
( time Rscript $SKILL/scripts/nucleosome_analysis.R $DATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam $TAG $BED ) > run.log 2>&1; echo "rc=$?"
grep -v '^ ' run.log | tail -20 | cut -c1-200; cat ${TAG}_summary.csv
S=/home/sci/micromamba/envs/bio-atac-seq-nucleosome-positioning/bin/samtools
for b in ${TAG}_nfr.bam ${TAG}_mono.bam; do echo $b total $($S view -c $b) mapq_lt30 $($S view -c -e 'mapq<30' $b); done
$S view ${TAG}_mono.bam | awk '{l=$9<0?-$9:$9; if(l>=180&&l<=247)a++; else b++} END{print "mono tlen in 180-247:",a,"outside:",b}'
ls -l
