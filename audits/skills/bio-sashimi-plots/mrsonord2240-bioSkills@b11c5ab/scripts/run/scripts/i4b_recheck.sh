source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/out/i4; R=chr10:27040584-27048100
echo "== counting every alignment record (incl. 132 secondary in one BAM):"
micromamba run -n as-core python $RUN/scripts/jtruth.py $R groups.tsv --M 1 --agg mean_j --svg ex.svg | tail -11
echo "== per-sample, endothelial:"; micromamba run -n as-core python $RUN/scripts/jtruth.py $R endo.tsv --M 1 --agg none --svg endo.svg | tail -3
echo "== --no-secondary (for the record):"; micromamba run -n as-core python $RUN/scripts/jtruth.py $R groups.tsv --M 1 --agg mean_j --svg ex.svg --no-secondary | tail -1
echo "== secondary/paired counts per BAM"
for b in $AS/public-data/sashimi/bams/*.bam; do micromamba run -n as-core samtools view -c -f 256 $b | tr '\n' ' '; done; echo
micromamba run -n as-core samtools view -c -f 1 $AS/public-data/sashimi/bams/ENCFF088HTJ.chr10_27035000_27050000.bam
