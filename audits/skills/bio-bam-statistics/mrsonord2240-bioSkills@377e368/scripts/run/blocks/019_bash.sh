# Default depth caps (checked on a 9500x stack; samtools 1.24, bcftools 1.24, pysam 0.24.1):
#   samtools depth         uncapped (-d/--max-depth is deprecated in 1.13+ and silently ignored)
#   samtools coverage      -d 1000000
#   mosdepth               uncapped
#   samtools mpileup       8000  -> samtools mpileup -d 1000000 -f ref.fa input.bam
#   bcftools mpileup       250   -> bcftools mpileup -d 1000000 -f ref.fa input.bam
#   pysam pileup()         max_depth=8000  -> pass max_depth=1_000_000
