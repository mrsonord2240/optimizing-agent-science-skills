while read -r chrom start end _; do
    samtools coverage -H -r "$chrom:$((start+1))-$end" input.bam
done < regions.bed
