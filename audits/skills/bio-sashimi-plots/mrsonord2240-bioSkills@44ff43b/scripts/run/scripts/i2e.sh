source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
asenv as-core python $RUN/scripts/i2e_plot_fn.py 2>&1 | grep -a "saved\|size\|Error"
asenv as-core python $RUN/scripts/svg_labels.py $RUN/out/ex_plot_fn.svg | grep -aE '^[0-9]+$|^G[12]' | tr '\n' ' '; echo
