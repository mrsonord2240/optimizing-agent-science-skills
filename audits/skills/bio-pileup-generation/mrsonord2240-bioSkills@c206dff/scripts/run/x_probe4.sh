H=/mnt/openscience/audit-envs/alignment-files/public-data/human
samtools depth -a -r chr22:3995-4005 $H/test.paired_end.sorted.bam
samtools depth -r chr22:1952-4617 $H/test.paired_end.sorted.bam | awk 'NR>1 && $2!=p+1{print p,$2} {p=$2}' | head
