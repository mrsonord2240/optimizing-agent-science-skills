source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
ggsashimi.py --help | tr '\r' '\n' | grep -a -B1 -A3 "MIN_COVERAGE, --min-coverage" | head; ggsashimi.py --help | grep -a -i -A4 "\-\-min-coverage"| head -8
echo "== median_j labels (expected medians Control 40/10/40, Treatment 10/40/10)"
micromamba run -n as-core python $RUN/scripts/svg_labels.py $RUN/out/i1c/l_median_j.svg | grep -aE '^[0-9]+$' | tr '\n' ' '
