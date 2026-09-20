source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
O=$RUN/out
lab() { asenv as-core python $RUN/scripts/svg_labels.py $1 | grep -E '^[0-9]+$' | tr '\n' ' '; echo; }
run() { # name, args...
  n=$1; shift
  ggsashimi.py "$@" -F svg -o $O/$n > $O/$n.log 2>&1; rc=$?
  echo "[$n] rc=$rc  junction-labels+axis: $( [ -f $O/$n.svg ] && lab $O/$n.svg || echo NO_SVG)"
  grep -aE "ERROR|WARN|Error" $O/$n.log | head -3
}
echo "== (a) default -M (Skill troubleshooting says default is 10) : G2_rep3 has 9/38/11 reads"
run i3a_default -b G2_rep3.bam -c chrP:1-1200
echo "== (b) -M 10 on G1_rep1 (skip junction has exactly 10 reads)"
run i3b_M10 -b G1_rep1.bam -c chrP:1-1200 -M 10
echo "== (c) -M 11 on G1_rep1"
run i3c_M11 -b G1_rep1.bam -c chrP:1-1200 -M 11
echo "== (d) group aggregate, -M 11, truth G1 means: 40.67 / 10.67 / 39.33"
run i3d_aggM11 -b sashimi_groups.tsv -c chrP:1-1200 -M 11 -O 3 -A mean_j
echo "== (d0) group aggregate, -M 1 (no filter)"
run i3d0_aggM1 -b sashimi_groups.tsv -c chrP:1-1200 -M 1 -O 3 -A mean_j
echo "== (e) wrong contig name"
run i3e_badchrom -b G1_rep1.bam -c 1:1-1200
echo "== (f) TSV with one wrong BAM path (typo) and one good"
printf 'ok\tG1_rep1.bam\tA\ntypo\tG1_rep_TYPO.bam\tA\n' > bad_paths.tsv
run i3f_missing -b bad_paths.tsv -c chrP:1-1200 -O 3
echo "== (f2) TSV with only wrong BAM paths"
printf 'typo\tnope.bam\tA\n' > bad_paths2.tsv
run i3f2_allmissing -b bad_paths2.tsv -c chrP:1-1200
echo "== (g) examples/plot_sashimi.py plot_specific_event: -A mean but no -O"
run i3g_aggnoO -b sashimi_groups.tsv -c chrP:1-1200 -A mean
echo "== (h) region with no reads"
run i3h_empty -b G1_rep1.bam -c chrP:2000-2500
