# one merged BAM per group; -split is essential: without it introns are filled with coverage
samtools merge -f ctrl_merged.bam ctrl1.bam ctrl2.bam ctrl3.bam && samtools index ctrl_merged.bam
samtools merge -f trt_merged.bam trt1.bam trt2.bam trt3.bam && samtools index trt_merged.bam
bedtools genomecov -ibam ctrl_merged.bam -split -bga > ctrl.bedgraph
bedtools genomecov -ibam trt_merged.bam -split -bga > trt.bedgraph
