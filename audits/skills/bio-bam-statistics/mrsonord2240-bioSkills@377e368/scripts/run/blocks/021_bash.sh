mosdepth -t 4 sample input.bam                                                       # genome-wide per-base
mosdepth -t 4 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base sample input.bam   # exome QC
mosdepth -t 4 --quantize 0:1:10:100: sample input.bam                                # CNV-style bands
mosdepth -t 4 -f ref.fa sample input.cram                                            # CRAM: needs the reference and a .crai (samtools index input.cram)
