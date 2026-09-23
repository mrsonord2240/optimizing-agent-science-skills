samtools view -F 20 -o forward.bam input.bam      # 20 = 4 + 16
samtools view -f 16 -F 4 -o reverse.bam input.bam
