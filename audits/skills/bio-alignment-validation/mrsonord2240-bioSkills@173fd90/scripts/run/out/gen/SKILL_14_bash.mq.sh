samtools view -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam | cut -f5 | sort -n | uniq -c | sort -k2 -n
