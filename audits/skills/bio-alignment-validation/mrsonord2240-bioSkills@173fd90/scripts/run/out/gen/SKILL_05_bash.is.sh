samtools stats /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam > stats.txt
grep "^IS" stats.txt | cut -f2,3 > insert_sizes.txt
