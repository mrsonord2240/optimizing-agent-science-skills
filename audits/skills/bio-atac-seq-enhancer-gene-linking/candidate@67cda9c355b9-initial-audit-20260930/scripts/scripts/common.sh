# Audit common: isolated env from tooling phase (TOOLS.md). Source inside WSL 'science'.
source /mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/env.sh
export RUN=/mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/initial-audit-20260930
export SKILL=/mnt/openscience/wt/atac-enhancer-gene-linking/skills/bio-atac-seq-enhancer-gene-linking
export A=${ABC_DIR:-abc-head}; export R=$EG/src/$A; export E=$R/example_chr/chr22
stage_inputs() {  # $1 = workdir. Stages the hard-coded inputs run_abc.sh expects (public ABC chr22 K562 example)
  W=$1; rm -rf $W; mkdir -p $W; cd $W
  cp $EG/src/abc/tests/test_output/generic/K562_chr22/Peaks/macs2_peaks.narrowPeak atac_peaks.narrowPeak   # MACS2 peaks from the ABC official run
  cp $E/RefSeqCurated.170308.bed.CollapsedGeneBounds.chr22.hg38.TSS500bp.bed promoter_regions.bed
  cp $R/reference/UbiquitouslyExpressedGenes.txt ubiquitously_expressed.txt
  grep -P "^chr22\t" $R/reference/hg38/GRCh38_EBV.no_alt.chrom.sizes.tsv > chr22.sizes
  awk '{print $1"\t0\t"$2}' chr22.sizes > chr22.sizes.bed
  cp $E/ENCFF860XAE.chr22.sorted.se.bam atac.bam; cp $E/ENCFF860XAE.chr22.sorted.se.bam.bai atac.bam.bai
  cp $E/ENCFF790GFL.chr22.sorted.se.bam h3k27ac.bam; cp $E/ENCFF790GFL.chr22.sorted.se.bam.bai h3k27ac.bam.bai
}
