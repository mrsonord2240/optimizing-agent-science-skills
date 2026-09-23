#!/bin/bash
# Build the two synthetic fixtures (labelled synthetic in the report) and record tool versions.
set -u
R=/mnt/openscience/audits/bio-alignment-filtering/run
cd $R
mkdir -p data out
samtools --version | head -2; python -c "import pysam;print('pysam',pysam.__version__)"; python --version
python make_synthetic_flags.py data/synthetic_allflags.bam
python make_repeat_genome.py data/repeat
