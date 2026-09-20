samtools idxstats /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam | awk '$2>0 {printf "%s\t%.4f\n", $1, $3/$2}' | head -25
