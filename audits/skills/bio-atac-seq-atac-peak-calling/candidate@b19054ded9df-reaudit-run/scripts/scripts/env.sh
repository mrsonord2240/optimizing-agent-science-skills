source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/wsl_env.sh
export S=/mnt/openscience/wt/atac-atac-peak-calling/skills/bio-atac-seq-atac-peak-calling/scripts/call_atac_peaks.sh
export D=$ATACDATA/encode
export E1=$D/GM12878_rep1_filtered.chr1_1-30000000.bam E2=$D/GM12878_rep2_filtered.chr1_1-30000000.bam
export BL=$APC/public-cache/hg38-blacklist.v2.bed CS=$ATACDATA/reference/hg38.chr1.chrom.sizes
export R=$APC/run/reaudit; mkdir -p $R
