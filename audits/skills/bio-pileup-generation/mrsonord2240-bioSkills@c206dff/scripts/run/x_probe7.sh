P=/mnt/openscience/audit-envs/alignment-files/public-data
samtools view $P/human/test.rna.paired_end.sorted.bam | awk '$6 ~ /N/' | wc -l
samtools view -H $P/human/test.rna.paired_end.sorted.bam | head -5
samtools view $P/human/test.rna.paired_end.sorted.bam | head -3 | cut -f1-9
samtools view -H $P/sarscov2/sars-cov-2_v5.3.2.nanopore.bam | head -4
samtools flagstat $P/sarscov2/sars-cov-2_v5.3.2.nanopore.bam | head -6
samtools view $P/sarscov2/sars-cov-2_v5.3.2.nanopore.bam | cut -f5 | sort -n | uniq -c | head
