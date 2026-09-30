#!/bin/bash
# Audit-run driver (WSL science). Usage: run_audit.sh <step>
export PATH=/home/sci/.local/bin:$PATH MAMBA_ROOT_PREFIX=/home/sci/micromamba
export SCA=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/audit-initial-20260930
export ATACDATA=/mnt/openscience/audit-envs/atac-seq/public-data
export CACHE=/mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/public-cache
export SKILL=/mnt/openscience/wt/atac-single-cell-atac/skills/bio-atac-seq-single-cell-atac
export MACS3=/home/sci/micromamba/envs/bio-atac-seq-single-cell-atac-py/bin/macs3
RUN=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/initial-audit-20260930
export AUDOUT=$RUN/out
SC=$RUN/scripts; mkdir -p $SCA/work $AUDOUT; cd $SCA/work
RR="micromamba run -n bio-atac-seq-single-cell-atac-r"; PY="micromamba run -n bio-atac-seq-single-cell-atac-py"; AM="micromamba run -n bio-atac-seq-single-cell-atac-amulet"
case $1 in
 signac_asis) mkdir -p asis && cd asis && $RR Rscript $SKILL/scripts/signac_workflow.R $ATACDATA/scatac/outs/filtered_peak_bc_matrix.h5 $ATACDATA/scatac/outs/fragments.tsv.gz $ATACDATA/scatac/outs/singlecell.csv ;;
 signac_patched) mkdir -p patched && cd patched && python3 $SC/patch_signac.py $SKILL/scripts/signac_workflow.R signac_patched.R 1 && diff $SKILL/scripts/signac_workflow.R signac_patched.R; $RR Rscript signac_patched.R $ATACDATA/scatac/outs/filtered_peak_bc_matrix.h5 $ATACDATA/scatac/outs/fragments.tsv.gz $ATACDATA/scatac/outs/singlecell.csv && $RR Rscript $SC/check_signac.R ;;
 snap) $PY python $SC/snap_pipeline.py ;;
 archr) $RR Rscript $SC/archr_pipeline.R ;;
 callpeaks) $RR Rscript $SC/callpeaks_doublets.R ;;
 wnn) $RR Rscript $SC/multiome_wnn.R ;;
 peakvi) $PY python $SC/peakvi_query.py ;;
 amulet)
   A=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/public-cache/amulet; O=$SCA/work/amulet; rm -rf $O; mkdir -p $O; cd $O; echo chr1 > chr1.txt
   $AM bash $A/AMULET.sh --forcesorted $ATACDATA/scatac/outs/fragments.tsv.gz $ATACDATA/scatac/outs/singlecell.csv $O/chr1.txt $A/RestrictionRepeatLists/restrictionlist_repeats_segdups_rmsk_hg38.bed $O $A
   cp $O/MultipletSummary.txt $AUDOUT/amulet_MultipletSummary.txt ;;
 amulet_numpy_probe)
   # does AMULET fail under modern numpy? (py env has numpy>=1.24)
   A=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/public-cache/amulet
   $PY python -c "import numpy;print('numpy',numpy.__version__)"; $PY python -c "import numpy as np; np.ones((2,2),dtype=np.object)" ;;
 peakvi_mm) $PY python $SC/peakvi_feature_mismatch.py ;;
 snap_macs3) HDF5_USE_FILE_LOCKING=${HDF5_LOCK:-TRUE} $PY python $SC/snap_macs3_default.py ;;
 probe) $RR Rscript $SC/probe_static_claims.R ;;
 qccsv) python3 $SC/singlecell_csv_qc.py $ATACDATA/scatac/outs/singlecell.csv ;;
 tabix) mkdir -p tabix && cd tabix && zcat $ATACDATA/scatac/outs/fragments.tsv.gz | head -200000 > sub.tsv && $AM bgzip -f sub.tsv && $AM tabix -f -p bed sub.tsv.gz
   n1=$($AM tabix sub.tsv.gz chr1:1-1500000 | wc -l); n2=$(zcat sub.tsv.gz | awk '$1=="chr1" && $2<=1500000 && $3>=1' | wc -l); echo "tabix=$n1 awk=$n2" ;;
esac
echo "STEP $1 EXIT $?"
