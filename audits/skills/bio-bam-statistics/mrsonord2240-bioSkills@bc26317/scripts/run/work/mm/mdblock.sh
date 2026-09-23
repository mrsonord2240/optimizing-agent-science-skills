mosdepth -t 2 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base sample input.bam   # exome QC
mosdepth -t 2 --quantize 0:1:10:100: sample input.bam                                # CNV-style bands
mosdepth -t 2 -f ref.fa sample c.cram                                            # CRAM: needs the reference and a .crai (samtools index input.cram)
