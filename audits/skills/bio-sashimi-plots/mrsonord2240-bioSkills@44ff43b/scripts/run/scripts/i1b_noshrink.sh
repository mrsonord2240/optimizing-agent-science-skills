source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
# same as Input 1 but WITHOUT --shrink (isolates the alignment issue), png only, plus -C 3 to test colour-by-group claim
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -o ../../out/i1b_noshrink -M 10 --alpha 0.25 --height 3 --width 10 --fix-y-scale --ann-height 4 -g planted.gtf --base-size 14 -O 3 -A mean_j -F png -R 100 >/dev/null 2>&1; echo rc=$?
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -o ../../out/i1c_color -M 10 --alpha 0.25 --height 3 --width 10 --shrink --fix-y-scale --ann-height 4 -g planted.gtf --base-size 14 -O 3 -C 3 -A mean_j -F png -R 100 >/dev/null 2>&1; echo rc=$?
