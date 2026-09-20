# When fragment length < 2 * read_length, R1 and R2 overlap (tool defaults: see the table above).
# samtools depth counts the overlap twice; -s counts each template once:
samtools depth -s input.bam
