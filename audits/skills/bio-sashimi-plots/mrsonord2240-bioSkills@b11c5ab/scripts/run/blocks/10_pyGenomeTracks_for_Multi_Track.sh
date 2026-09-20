samtools merge -f all_merged.bam ctrl_merged.bam trt_merged.bam && samtools index all_merged.bam   # regtools needs an indexed BAM
regtools junctions extract -s XS -o regtools_junctions.bed all_merged.bam
# regtools BED12 column 11 is blockSizes (anchor_left, anchor_right);
# column 12 is blockStarts (0, intron_length + anchor_left).
# Intron start = chromStart + anchor_left = $2 + a[1]
# Intron end   = chromStart + blockStarts[2] = $2 + b[2]
awk 'BEGIN{OFS="\t"} {split($11,a,","); split($12,b,","); s=$2+a[1]; e=$2+b[2]; print $1, s, s+1, $1, e-1, e, $5}' \
    regtools_junctions.bed > junctions.bedpe
