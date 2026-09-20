test -s /nonexistent.bam \
  && samtools quickcheck -v /nonexistent.bam \
  && [ $(samtools view -c -F 2304 /nonexistent.bam) -gt 1000 ] \
  || { echo "BAM failed integrity"; exit 1; }
