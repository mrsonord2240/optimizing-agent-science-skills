# Input 1b: ggplot2 pin claim. Same command, three envs: ggplot2 3.4.4 / 3.5.2 / 4.0.3. Labels checked against SVG; layout inspected visually (PNG).
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
cd $RUN/data/planted
for E in as-viz-gg34 as-viz-gg35 as-viz; do
  for F in png svg; do
    GGENV=$E ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -o $RUN/out/i1b_$E -M 1 --alpha 0.25 --height 3 --width 10 --shrink --fix-y-scale --ann-height 4 -g planted.gtf --base-size 14 -O 3 -C 3 -P $RUN/data/planted/palette.txt -A mean_j -F $F > $RUN/out/i1b_${E}_$F.log 2>&1
    echo "[$E $F] rc=$? $(ls -l $RUN/out/i1b_$E.$F | awk '{print $5}') bytes"
  done
  micromamba run -n as-core python $RUN/scripts/jtruth.py chrP:1-1200 sashimi_groups.tsv --M 1 --svg $RUN/out/i1b_$E.svg | tail -1
done
