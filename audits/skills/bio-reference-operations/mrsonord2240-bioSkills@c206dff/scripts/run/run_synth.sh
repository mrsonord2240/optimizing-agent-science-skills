cd /mnt/openscience/audits/bio-reference-operations/run
python make_synth.py data/synthetic
ls -la data/synthetic
samtools depth -a -r chr1:100-110 data/synthetic/synth_chr.bam | head -3
