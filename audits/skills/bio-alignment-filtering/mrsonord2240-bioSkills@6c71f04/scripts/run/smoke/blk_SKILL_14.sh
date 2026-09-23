# Short-variant germline
samtools view -f 2 -F 3328 -q 20 -o clean.bam input.bam

# SV calling: KEEP supplementary
samtools view -F 1024 -o sv_input.bam input.bam   # NOT -F 2304, 2308, 3328 or 3332

# ChIP-seq / ATAC-seq common filter
samtools view -F 1804 -q 30 -o filtered.bam input.bam
