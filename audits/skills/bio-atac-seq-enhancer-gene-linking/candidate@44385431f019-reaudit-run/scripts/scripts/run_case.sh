#!/bin/bash
# Re-audit: run candidate scripts/run_abc.sh in the main env on ABC chr22 K562 example. usage: run_case.sh <case> [ABC_DIR]
source /mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/env.sh
export LD_PRELOAD=$EG/libfinite_shim.so
A=${2:-abc-head}; export ABC_REPO=$EG/src/$A
SK=/mnt/openscience/wt/atac-enhancer-gene-linking/skills/bio-atac-seq-enhancer-gene-linking/scripts/run_abc.sh
E=$ABC_REPO/example_chr/chr22
W=/mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/reaudit-run/work/$1
rm -rf $W; mkdir -p $W; cd $W
export ACCESS_BAM=$E/ENCFF860XAE.chr22.sorted.se.bam H3K27AC_BAM=$E/ENCFF790GFL.chr22.sorted.se.bam
export ACCESS_TYPE=DHS CELL_TYPE=K562 OUTDIR=$W/out
export GENES_BED=$E/RefSeqCurated.170308.bed.CollapsedGeneBounds.chr22.hg38.bed TSS_BED=$E/RefSeqCurated.170308.bed.CollapsedGeneBounds.chr22.hg38.TSS500bp.bed
case $1 in
 usage) export HIC_TYPE=hic HIC_FILE=https://www.encodeproject.org/files/ENCFF621AIY/@@download/ENCFF621AIY.hic;;
 powerlaw|powerlaw_v112) ;;
 avgsub) export HIC_TYPE=avg HIC_FILE=$EG/work/avg;;
 atac_only) export ACCESS_TYPE=ATAC H3K27AC_BAM=;;
 macs3) export PEAKS=$W/macs3_peaks.narrowPeak; macs3 callpeak -f AUTO -g hs -p 0.1 -n macs3 --shift -75 --extsize 150 --nomodel --keep-dup all --call-summits --outdir $W -t $ACCESS_BAM >$W/macs3.log 2>&1; mv $W/macs3_peaks.narrowPeak $PEAKS 2>/dev/null; ls $W;;
esac
date -Is
bash $SK; echo "run_abc.sh rc=$?"; date -Is
