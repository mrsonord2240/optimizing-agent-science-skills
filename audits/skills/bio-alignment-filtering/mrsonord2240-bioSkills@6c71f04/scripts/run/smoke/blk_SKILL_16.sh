samtools view -b -F 4 -o output.bam input.bam                   # BAM (a .bam -o name also gives BAM)
samtools view -C -T reference.fa -F 4 -o output.cram input.bam  # CRAM (reference required)
samtools view -h -F 4 input.bam > output.sam                    # SAM with header
samtools view -c -F 3332 -q 30 input.bam                        # count only: run before writing, compare with `-c input.bam`
samtools quickcheck filtered.bam && echo OK || echo CORRUPT
samtools flagstat filtered.bam
