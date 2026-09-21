junction_saturation.py -i sample.bam -r genes.bed12 -o sample_junc_sat --skip-plot   # add -l/-u/-s for a finer 80-100% range
python examples/splicing_qc.py saturation sample.bam genes.bed12 sample_junc_sat
