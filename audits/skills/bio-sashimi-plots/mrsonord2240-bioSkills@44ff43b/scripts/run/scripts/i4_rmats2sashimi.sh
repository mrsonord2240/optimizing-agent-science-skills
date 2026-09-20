source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
echo "### --help"; rmats2sashimiplot --help 2>&1 | tr '\r' '\n' | head -70
