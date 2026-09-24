samtools idxstats /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.name.sorted.bam | awk '$1!="*" && $3>0 {print $1}' | head -25 | while read -r chr; do
    fwd=$(samtools view -c -F 2324 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.name.sorted.bam "$chr")
    rev=$(samtools view -c -f 16 -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.name.sorted.bam "$chr")
    awk -v c="$chr" -v f="$fwd" -v r="$rev" 'BEGIN{if (f+r) printf "%s: F=%d R=%d forward fraction=%.3f\n", c, f, r, f/(f+r)}'
done
