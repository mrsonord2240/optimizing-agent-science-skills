source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
for e in as-viz-gg34 as-viz-gg35 as-viz; do
  echo "== $e"
  micromamba run -n $e bash -c 'which R python samtools rmats2sashimiplot pyGenomeTracks bedtools regtools; R --version | head -1; Rscript -e "cat(as.character(packageVersion(\"ggplot2\")),\"\n\")"; python -c "import pysam;print(pysam.__version__)"' 2>&1 | tr '\r' '\n'
done
cd $SRC/ggsashimi && git log --oneline -1; cd $SRC/Jutils && git log --oneline -1; cd $SRC/leafcutter && git log --oneline -1
