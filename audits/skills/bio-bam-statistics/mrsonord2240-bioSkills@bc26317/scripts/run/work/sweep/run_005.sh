printf 'Sample\tRecords\tQCfail\tPrimary\tPrimaryMapped\tProperPair\tPrimaryDup\n' > summary.tsv
for bam in *.bam; do
    sample=$(basename "$bam" .bam)
    samtools flagstat -O tsv "$bam" | awk -F'\t' -v s="$sample" '
        $3 ~ /^total/            {rec = $1 + $2; fail = $2}
        $3 == "primary"          {pri = $1 + $2}
        $3 == "primary mapped"   {pm = $1 + $2}
        $3 == "properly paired"  {pp = $1 + $2}
        $3 == "primary duplicates" {dup = $1 + $2}
        END {print s"\t"rec"\t"fail"\t"pri"\t"pm"\t"pp"\t"dup}' >> summary.tsv
done
