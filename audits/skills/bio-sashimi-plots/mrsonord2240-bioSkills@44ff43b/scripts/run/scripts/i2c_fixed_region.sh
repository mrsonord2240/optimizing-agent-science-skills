source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data
# PDZD11 rMATS SE event (minus strand): region = upstreamES-500 .. downstreamEE+500 as in the Skill, contig renamed chrX->X (the only change)
R=X:69508604-69510295
BAMS=$(cut -f2 sashimi_groups.tsv | tr '\n' ' ')
ggsashimi.py -b sashimi_groups.tsv -c $R -o $RUN/out/i2c_PDZD11 -M 5 --shrink --fix-y-scale -O 3 -A mean_j -g annotation.gtf -F svg > $RUN/out/i2c.log 2>&1; echo rc=$?
ggsashimi.py -b sashimi_groups.tsv -c $R -o $RUN/out/i2c_PDZD11 -M 5 --shrink --fix-y-scale -O 3 -A mean_j -g annotation.gtf -F png -R 100 >> $RUN/out/i2c.log 2>&1
asenv as-core python $RUN/scripts/svg_labels.py $RUN/out/i2c_PDZD11.svg | tr '\n' '|'; echo
echo "--- pysam per-read junction counts in region"
asenv as-core python $RUN/scripts/junction_truth.py X 69508604 69510295 $BAMS 2>&1 | grep -av W::hts | tr -d ' \n'; echo
grep -aP '^\d+\t"ENSG\d+"\t"PDZD11"' rmats_real/SE.MATS.JC.txt | cut -f4-11,13-16,20-23
