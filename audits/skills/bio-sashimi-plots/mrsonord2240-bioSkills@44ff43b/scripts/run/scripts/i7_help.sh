source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
for c in "" convert-results heatmap sashimi venn-diagram; do echo "######## jutils.py $c --help"; jutils.py $c --help 2>&1 | tr '\r' '\n' | head -45; done
