samtools view -c -F 2308 -q 30 in.bam   # primary, mapped, MAPQ>=30
samtools view -c -F 2308 in.bam          # primary, mapped (denominator)
# For STAR/STARsolo, use -q 255 instead of -q 30 (255 is the unique-mapping sentinel)
