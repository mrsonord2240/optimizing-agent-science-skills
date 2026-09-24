samtools view -F 2308 aligned.bam | awk '$6 ~ /N[0-9]+S$/ || $6 ~ /^[0-9]+S[0-9]+N/' | wc -l   # reads with an intron next to a soft clip
