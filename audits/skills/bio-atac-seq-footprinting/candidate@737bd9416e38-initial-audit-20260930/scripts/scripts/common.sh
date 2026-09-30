# source inside WSL `science` (user sci). Audit-run environment, initial audit 2026-09-30.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
export P=bio-atac-seq-footprinting
export A=/mnt/openscience/audits/$P/initial-audit-20260930
export W=/mnt/openscience/audit-envs/$P/audit-20260930   # disposable run root
export D=/mnt/openscience/audit-envs/atac-seq/public-data
export SKILL=/mnt/openscience/wt/atac-footprinting/skills/bio-atac-seq-footprinting
export PATH=/home/sci/micromamba/envs/$P/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
export PATH=$PATH:/home/sci/.local/bin
mkdir -p $W
prep_inputs() {  # $1 = run dir; creates peaks.bed hg38-blacklist.v2.bed cond1.bam cond2.bam
  cd $1
  ( zcat $D/encode/ENCFF346CZA.bed.gz; zcat $D/encode/ENCFF855PCP.bed.gz ) | awk '$1=="chr1" && $3<30000000' | cut -f1-3 | sort -k1,1 -k2,2n | bedtools merge -i - > peaks0.bed
  zcat $D/annotation/hg38-blacklist.v2.bed.gz > hg38-blacklist.v2.bed
  bedtools intersect -v -a peaks0.bed -b hg38-blacklist.v2.bed > peaks.bed
  cp $D/encode/GM12878_rep1_filtered.chr1_1-30000000.bam cond1.bam; cp $D/encode/K562_rep1_filtered.chr1_1-30000000.bam cond2.bam
  samtools index cond1.bam; samtools index cond2.bam
}
