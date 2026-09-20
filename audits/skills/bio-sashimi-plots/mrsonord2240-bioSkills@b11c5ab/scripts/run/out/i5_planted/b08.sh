# one merged BAM per group; -split is essential: without it introns are filled with coverage
samtools merge -f ctrl_merged.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G1_rep1.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G1_rep2.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G1_rep3.bam && samtools index ctrl_merged.bam
samtools merge -f trt_merged.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G2_rep1.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G2_rep2.bam /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/G2_rep3.bam && samtools index trt_merged.bam
bedtools genomecov -ibam ctrl_merged.bam -split -bga > ctrl.bedgraph
bedtools genomecov -ibam trt_merged.bam -split -bga > trt.bedgraph
