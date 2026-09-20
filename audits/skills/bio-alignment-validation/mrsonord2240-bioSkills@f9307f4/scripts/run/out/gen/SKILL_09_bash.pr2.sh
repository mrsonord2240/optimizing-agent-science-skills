proper=$(samtools view -c -f 2 -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam)
paired=$(samtools view -c -f 1 -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam)
awk -v p="$proper" -v n="$paired" 'BEGIN{if (n) printf "Proper pairing rate: %.2f%%\n", 100*p/n; else print "no paired reads"}'
