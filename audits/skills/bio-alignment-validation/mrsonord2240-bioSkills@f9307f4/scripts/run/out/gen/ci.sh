MIN_READS=${MIN_READS:-1}
test -s /mnt/openscience/audits/bio-alignment-validation/run/out/work/sp dir/my sample.bam \
  && samtools quickcheck -v /mnt/openscience/audits/bio-alignment-validation/run/out/work/sp dir/my sample.bam \
  && [ "$(samtools view -c -F 2304 /mnt/openscience/audits/bio-alignment-validation/run/out/work/sp dir/my sample.bam)" -ge "$MIN_READS" ] \
  || { echo "BAM failed integrity"; exit 1; }
