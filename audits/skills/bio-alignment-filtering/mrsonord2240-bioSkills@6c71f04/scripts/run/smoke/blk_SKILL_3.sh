if [ "$(samtools view -c -f 1024 input.bam)" -eq 0 ]; then
    echo "no duplicate-flagged reads; marking first" >&2
    samtools collate -O -u input.bam tmp_collate | samtools fixmate -m -u - - | \
        samtools sort -u - | samtools markdup - marked.bam
    samtools view -F 1024 -o nodup.bam marked.bam
else
    samtools view -F 1024 -o nodup.bam input.bam
fi
