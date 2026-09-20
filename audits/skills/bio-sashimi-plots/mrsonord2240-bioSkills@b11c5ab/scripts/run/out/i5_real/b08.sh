# one merged BAM per group; -split is essential: without it introns are filled with coverage
samtools merge -f ctrl_merged.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/derived/xs_bams/ERR188383.xs.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/derived/xs_bams/ERR188428.xs.bam && samtools index ctrl_merged.bam
samtools merge -f trt_merged.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/derived/xs_bams/ERR188454.xs.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/derived/xs_bams/ERR204916.xs.bam && samtools index trt_merged.bam
bedtools genomecov -ibam ctrl_merged.bam -split -bga > ctrl.bedgraph
bedtools genomecov -ibam trt_merged.bam -split -bga > trt.bedgraph
