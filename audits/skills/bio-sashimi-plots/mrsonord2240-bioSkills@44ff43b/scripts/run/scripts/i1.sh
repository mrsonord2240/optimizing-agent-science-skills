source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
asenv as-core python $RUN/scripts/i1_canonical.py; echo "rc=$?"
ls -la $RUN/out/
asenv as-core python $RUN/scripts/svg_labels.py $RUN/out/i1_G1_sashimi.svg | tr '\n' '|'; echo
