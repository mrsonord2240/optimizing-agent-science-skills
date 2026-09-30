# negative controls for the Skill's AMULET table on ARC: (a) BAM route with documented ATAC defaults (no idx flags); (b) fragment route fed the raw ARC per_barcode_metrics.csv
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
A=$SCA/public-cache/amulet; P=$ATACDATA/10x-multiome/arc-pbmc3k; M=$P/pbmc_granulocyte_sorted_3k_per_barcode_metrics.csv
REP=$A/RestrictionRepeatLists/restrictionlist_repeats_segdups_rmsk_hg38.bed
E="micromamba run -n bio-atac-seq-single-cell-atac-amulet"
W=$SCA/work/reaudit10x_amulet_neg_a; rm -rf $W; mkdir -p $W; cd $W; echo chr1 > chr1.txt
echo "=== (a) BAM, --forcesorted only (ATAC default idx)"; $E bash $A/AMULET.sh --forcesorted $P/chr1_1-30Mb.possorted.bam $M chr1.txt $REP $W $A 2>&1 | tail -6; echo "exit ${PIPESTATUS[0]}"; ls $W; cat $W/MultipletSummary.txt 2>/dev/null
W=$SCA/work/reaudit10x_amulet_neg_b; rm -rf $W; mkdir -p $W; cd $W; echo chr1 > chr1.txt
echo "=== (b) fragments, raw ARC per_barcode_metrics.csv"; $E bash $A/AMULET.sh $P/pbmc_granulocyte_sorted_3k_atac_fragments.tsv.gz $M chr1.txt $REP $W $A 2>&1 | tail -8; echo "exit ${PIPESTATUS[0]}"; ls $W; cat $W/MultipletSummary.txt 2>/dev/null
