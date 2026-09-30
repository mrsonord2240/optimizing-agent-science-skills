# Re-audit: AMULET fragment command exactly as documented in live ecosystem-workflows.md, in an env built as documented (numpy<1.24).
# Also demonstrates the documented failure on the modern-numpy py env.
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
A=$SCA/public-cache/amulet; O=$SCA/work/ra_amulet; rm -rf $O; mkdir -p $O; cd $O
micromamba run -n bio-atac-seq-single-cell-atac-amulet python -c "import numpy,sys;print('amulet env numpy',numpy.__version__)"
micromamba run -n bio-atac-seq-single-cell-atac-amulet bash -c "cd $O; bash $A/AMULET.sh $ATACDATA/scatac/outs/fragments.tsv.gz $ATACDATA/scatac/outs/singlecell.csv $A/human_autosomes.txt $A/RestrictionRepeatLists/restrictionlist_repeats_segdups_rmsk_hg38.bed $O $A"
echo EXIT $?
cat $O/MultipletSummary.txt; wc -l $O/MultipletBarcodes_01.txt $O/MultipletProbabilities.txt; ls $O
head -3 $O/MultipletProbabilities.txt
# negative control: same command under modern numpy (py env) -> documented np.object failure
O2=$SCA/work/ra_amulet_modern; rm -rf $O2; mkdir -p $O2
micromamba run -n bio-atac-seq-single-cell-atac-py python -c "import numpy;print('py env numpy',numpy.__version__)"
micromamba run -n bio-atac-seq-single-cell-atac-py bash -c "cd $O2; bash $A/AMULET.sh $ATACDATA/scatac/outs/fragments.tsv.gz $ATACDATA/scatac/outs/singlecell.csv $A/human_autosomes.txt $A/RestrictionRepeatLists/restrictionlist_repeats_segdups_rmsk_hg38.bed $O2 $A" 2>&1 | tail -5
