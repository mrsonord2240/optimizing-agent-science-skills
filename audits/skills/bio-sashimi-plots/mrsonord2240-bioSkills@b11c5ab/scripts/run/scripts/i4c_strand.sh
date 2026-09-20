source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/out/i4; R=chr10:27040584-27048100
echo "== independent per-strand counts (SENSE routing = read strand), endothelial samples, per-sample counts [s1..s4]"
micromamba run -n as-core python $RUN/scripts/jtruth.py $R endo.tsv --M 1 --agg none --strand SENSE | grep -v hts_idx
echo "== labels in ggsashimi st_SENSE_+.svg / st_SENSE_-.svg (arc labels are first numbers per sample track)"
