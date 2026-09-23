  samtools view -F 3332 -q 30 -o filt.bam input.bam
  samtools view filt.bam | cut -f1 | sort | uniq -d > both.txt   # valid while at most two records per name remain (no supplementary)
  samtools view -N both.txt -o paired.bam filt.bam
  