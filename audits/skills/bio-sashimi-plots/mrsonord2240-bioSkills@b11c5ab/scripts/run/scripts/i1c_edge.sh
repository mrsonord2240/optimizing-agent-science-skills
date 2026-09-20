# Input 1c (edge): the corrected ggsashimi defaults / claims / silent-failure section, each checked by output
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
cd $RUN/data/planted
O=$RUN/out/i1c; mkdir -p $O
JT="micromamba run -n as-core python $RUN/scripts/jtruth.py"
run() { n=$1; shift; ggsashimi.py "$@" -F svg -o $O/$n > $O/$n.log 2>&1; rc=$?; echo "[$n] rc=$rc svg=$([ -f $O/$n.svg ] && stat -c %s $O/$n.svg || echo NONE)"; grep -aE "ERROR|Error|StopIteration|invalid contig|Cannot apply|Unknown" $O/$n.log | head -2; }
echo "== default -M per --help"; ggsashimi.py --help | grep -a -A2 -- "-M MIN_COVERAGE" | head -4
echo "== a. -M 10 with mean_j: SKILL claims Treatment skip 10.33 shows 11 (rep3=9 drops out), 10 at -M 1"
run a_M10 -b sashimi_groups.tsv -c chrP:1-1200 -M 10 -O 3 -A mean_j
$JT chrP:1-1200 sashimi_groups.tsv --M 10 --svg $O/a_M10.svg | grep -E "Treatment|LABELS"
echo "== b. one wrong BAM path in TSV (SKILL: dropped silently, rc 0)"
printf 'ok\tG1_rep1.bam\tA\ntypo\tG1_rep_TYPO.bam\tA\n' > $O/bad1.tsv; cp $O/bad1.tsv ./bad1.tsv
run b_onemissing -b bad1.tsv -c chrP:1-1200 -O 3
echo "== c. all BAM paths wrong"
printf 'typo\tnope.bam\tA\n' > bad2.tsv; run c_allmissing -b bad2.tsv -c chrP:1-1200
echo "== d. contig 1 vs chrP"; run d_badcontig -b sashimi_groups.tsv -c 1:1-1200 -O 3
echo "== e. -A mean without -O"; run e_aggnoO -b sashimi_groups.tsv -c chrP:1-1200 -A mean
echo "== f. region without reads"; run f_empty -b sashimi_groups.tsv -c chrP:2000-2500 -O 3
echo "== g. --shrink with -M above every junction (SKILL: RuntimeError generator raised StopIteration)"
run g_shrink_hiM -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -A mean_j -M 100 --shrink
echo "== g2. same without --shrink (should draw coverage without arcs)"
run g2_noshrink_hiM -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -A mean_j -M 100
echo "== h. bad palette colour (SKILL: rc 0 and no figure)"
printf 'notacolour\nalsobad\n' > $O/badpal.txt
run h_badpal -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -C 3 -P $O/badpal.txt -A mean_j
echo "== i. colours: no -C (grey) vs -C without -P (R defaults) -> pngs"
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -A mean_j -M 1 -F png --width 6 --height 3 -R 60 -o $O/i_noC > $O/i_noC.log 2>&1; echo "[i_noC] rc=$? $(stat -c %s $O/i_noC.png)"
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -C 3 -A mean_j -M 1 -F png --width 6 --height 3 -R 60 -o $O/i_Cnop > $O/i_Cnop.log 2>&1; echo "[i_Cnop] rc=$? $(stat -c %s $O/i_Cnop.png)"
echo "== j. -s SENSE output files (single-end)"
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -A mean_j -M 1 -s SENSE -F png -R 60 --width 6 --height 3 -o $O/j_strand > $O/j_strand.log 2>&1; echo "rc=$?"; ls $O | grep j_strand
echo "== k. -s MATE1_SENSE on single-end (SKILL: TypeError)"
ggsashimi.py -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -M 1 -s MATE1_SENSE -F png -o $O/k_mate > $O/k_mate.log 2>&1; echo "rc=$?"; grep -aE "TypeError" $O/k_mate.log | head -1
echo "== l. median_j / mean (coverage) also work"
run l_median_j -b sashimi_groups.tsv -c chrP:1-1200 -O 3 -A median_j -M 1; $JT chrP:1-1200 sashimi_groups.tsv --M 1 --svg $O/l_median_j.svg | tail -1
