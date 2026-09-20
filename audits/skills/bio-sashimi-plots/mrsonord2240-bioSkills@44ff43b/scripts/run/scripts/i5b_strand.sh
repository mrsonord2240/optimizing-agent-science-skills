source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
O=$RUN/out
lab() { asenv as-core python $RUN/scripts/svg_labels.py $1 | grep -E '^[0-9]+$' | tr '\n' ' '; }
cd $RUN/data/planted
echo "== planted single-end + strand reads; -s SENSE / ANTISENSE (junction labels, files produced)"
for s in NONE SENSE ANTISENSE; do
  rm -f $O/i5s_$s*; ggsashimi.py -b G1_rep1.bam -c chrP:1-1200 -s $s -F svg -o $O/i5s_$s > $O/i5s_$s.log 2>&1; echo "-s $s rc=$? files: $(ls $O | grep "^i5s_$s" | grep svg | tr '\n' ' ')"
  for f in $O/i5s_$s*.svg; do echo "   $(basename $f): $(lab $f)"; done
done
echo "== MATE1_SENSE on single-end (unpaired) reads"
ggsashimi.py -b G1_rep1.bam -c chrP:1-1200 -s MATE1_SENSE -F svg -o $O/i5s_M1 > $O/i5s_M1.log 2>&1; echo "rc=$?"; grep -a "Error" $O/i5s_M1.log | head -2
cd $RUN/data
echo "== real PE chrX BAM ERR188428, PDZD11 region, -s MATE2_SENSE vs independent strand count"
BAM=$ASDATA/rnasplice/bam/ERR188428.Aligned.out.bam
for m in MATE2_SENSE MATE1_SENSE; do
  rm -f $O/i5r_$m*; ggsashimi.py -b $BAM -c X:69508604-69510295 -s $m -F svg -o $O/i5r_$m > $O/i5r_$m.log 2>&1; echo "-s $m rc=$?"
  for f in $O/i5r_$m*.svg; do echo "   $(basename $f): $(lab $f)"; done
  echo "   pysam: $(asenv as-core python $RUN/scripts/strand_truth.py $BAM X 69508604 69510295 $m 2>/dev/null | grep -av W::)"
done
