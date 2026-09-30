# Re-audit: run the SHIPPED signac_workflow.R as documented (3 args), relaxed (args 4,5), and with a column-stripped singlecell.csv (guard).
# usage (WSL science): bash ra_signac.sh doc|relaxed|guard
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
T=$1; D=$ATACDATA/scatac/outs
W=$SCA/work/ra_signac_$T; rm -rf $W; mkdir -p $W; cd $W
R="micromamba run -n bio-atac-seq-single-cell-atac-r Rscript $SKILL/scripts/signac_workflow.R"
case $T in
  doc)     $R $D/filtered_peak_bc_matrix.h5 $D/fragments.tsv.gz $D/singlecell.csv ;;
  relaxed) $R $D/filtered_peak_bc_matrix.h5 $D/fragments.tsv.gz $D/singlecell.csv 1 1000 ;;
  guard)   # rename peak_region_fragments column -> simulates cellranger-arc style metadata
           sed '1s/peak_region_fragments/peak_region_frags_renamed/' $D/singlecell.csv > $W/sc_missing.csv
           $R $D/filtered_peak_bc_matrix.h5 $D/fragments.tsv.gz $W/sc_missing.csv ;;
esac
echo EXIT $?
ls -la $W
