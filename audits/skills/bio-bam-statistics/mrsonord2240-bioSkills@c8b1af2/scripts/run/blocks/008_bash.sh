# Total mapped alignments (includes secondary/supplementary)
samtools idxstats input.bam | awk '{sum += $3} END {print sum}'

# Mitochondrial percentage of mapped alignments (chrM or MT)
samtools idxstats input.bam | awk '
    $1 ~ /^(chr)?(M|MT)$/ {mt += $3; found = 1}
    {total += $3}
    END {if (!found) {print "no chrM/MT contig in idxstats" > "/dev/stderr"; exit 1}
         if (!total) {print "no mapped reads" > "/dev/stderr"; exit 1}
         printf "%.2f%% mitochondrial\n", mt/total*100}'

# Sex check (X/Y ratio; +1 avoids division by zero)
samtools idxstats input.bam | awk '
    $1 ~ /^(chr)?X$/ {x = $3; fx = 1}
    $1 ~ /^(chr)?Y$/ {y = $3; fy = 1}
    END {if (!fx || !fy) {print "no chrX/chrY contig in idxstats" > "/dev/stderr"; exit 1}
         printf "X:Y = %.2f\n", x/(y+1)}'
