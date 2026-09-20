source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/real_ggs
R=chr10:27040584-27048100
BAMS=$(cut -f2 input_bams.tsv | tr '\n' ' ')
asenv as-core python $RUN/scripts/junction_truth.py chr10 27040584 27048100 $BAMS > $RUN/out/i5_truth.json 2>/dev/null; echo truth-rc=$?
# Skill-style call: SKILL.md flags on the real data (adds -j to dump junctions, -F svg to parse)
ggsashimi.py -b input_bams.tsv -c $R -o $RUN/out/i5_skillflags -M 10 --alpha 0.25 --height 3 --width 10 --shrink --fix-y-scale --ann-height 4 -g annotation.gtf --base-size 14 -O 3 -A mean_j -F svg -j $RUN/out/i5_junc.bed > $RUN/out/i5_skillflags.log 2>&1; echo rc=$?
asenv as-core python $RUN/scripts/i5_check.py input_bams.tsv $RUN/out/i5_truth.json $RUN/out/i5_junc.bed $RUN/out/i5_skillflags.svg
