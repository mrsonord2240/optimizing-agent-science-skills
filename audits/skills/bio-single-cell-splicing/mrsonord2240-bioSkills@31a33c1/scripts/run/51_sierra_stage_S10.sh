#!/bin/bash
# INPUT 6b: Sierra. Stage the package's own bundled real 10x example (mouse heart TIP cells, MI) under the names SKILL.md uses, then run block S10 (regtools) LITERALLY.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; E=/mnt/openscience/audit-envs/alternative-splicing/R-lib/Sierra/extdata
W=$R/out/in6_sierra; rm -rf $W; mkdir -p $W; cd $W
cp $E/Vignette_example_TIP_mi.bam possorted_genome_bam.bam; cp $E/Vignette_example_TIP_mi.bai possorted_genome_bam.bam.bai
cp $E/Vignette_cellranger_genes_subset.gtf annotation.gtf; cp $E/example_TIP_MI_whitelist_barcodes.tsv barcodes.tsv
bash $R/blocks/S10_bash.sh 2>&1 | tail -3
wc -l junctions.bed; head -3 junctions.bed
awk 'NR>1 && $6=="+"' junctions.bed | wc -l; awk 'NR>1 && $6=="-"' junctions.bed | wc -l; awk 'NR>1 && $6=="?"' junctions.bed | wc -l
echo "shipped junction BED for the same BAM:"; wc -l $E/Vignette_example_TIP_MI_junctions.bed; head -3 $E/Vignette_example_TIP_MI_junctions.bed
