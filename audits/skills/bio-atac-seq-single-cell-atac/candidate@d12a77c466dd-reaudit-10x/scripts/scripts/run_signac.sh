# independent re-audit: run the shipped scripts/signac_workflow.R. usage: run_signac.sh arc|atac2x|atac1x TAG [min_tss min_frags]
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
T=$1; TAG=$2; shift 2
P=$ATACDATA/10x-multiome
W=$SCA/work/reaudit10x_$TAG; rm -rf $W; mkdir -p $W; cd $W
case $T in
arc) H5=/mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/public-cache/pbmc_granulocyte_sorted_3k_filtered_feature_bc_matrix.h5
  FR=$P/arc-pbmc3k/pbmc_granulocyte_sorted_3k_atac_fragments.tsv.gz; MD=$P/arc-pbmc3k/pbmc_granulocyte_sorted_3k_per_barcode_metrics.csv;;
atac2x) H5=$P/atac2x-pbmc10k/10k_pbmc_ATACv2_nextgem_Chromium_Controller_filtered_peak_bc_matrix.h5
  FR=$P/atac2x-pbmc10k/chr1_1-30Mb.fragments.tsv.gz; MD=$P/atac2x-pbmc10k/10k_pbmc_ATACv2_nextgem_Chromium_Controller_singlecell.csv;;
atac1x) H5=$ATACDATA/scatac/outs/filtered_peak_bc_matrix.h5; FR=$ATACDATA/scatac/outs/fragments.tsv.gz; MD=$ATACDATA/scatac/outs/singlecell.csv;;
esac
echo "CMD Rscript signac_workflow.R $H5 $FR $MD $@"
time micromamba run -n bio-atac-seq-single-cell-atac-r Rscript $SKILL/scripts/signac_workflow.R $H5 $FR $MD "$@"
echo EXIT $?
ls -la $W
