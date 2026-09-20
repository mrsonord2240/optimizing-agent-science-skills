source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
asenv as-core python $RUN/scripts/i2d_planted_batch.py 2>&1 | grep -av "label.size\|annotate\|^Warning\|size\|linewidth" | tail -12
