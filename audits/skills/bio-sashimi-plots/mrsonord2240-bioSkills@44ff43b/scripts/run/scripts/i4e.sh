source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
E=$RUN/data/rmats_planted/SE.MATS.JC.txt
B1=G1_rep1.bam,G1_rep2.bam,G1_rep3.bam; B2=G2_rep1.bam,G2_rep2.bam,G2_rep3.bam
echo "### 4e per-replicate, NO --color"
rm -rf $RUN/out/r2s_e; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_e --exon_s 1 --intron_s 5 > $RUN/out/r2s_e.log 2>&1; echo "rc=$?"; ls $RUN/out/r2s_e/Sashimi_plot
echo "### 4c full log (per-replicate WITH --color 2 colours)"
rm -rf $RUN/out/r2s_c; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_c --exon_s 1 --intron_s 5 --color '#1f77b4,#ff7f0e' > $RUN/out/r2s_c.log 2>&1; echo "rc=$?"; ls $RUN/out/r2s_c/Sashimi_plot; grep -ai -n "error\|Traceback\|exception\|color" $RUN/out/r2s_c.log | head
echo "### 4f group-info: missing file"
rm -rf $RUN/out/r2s_b; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_b --group-info group_def.txt > $RUN/out/r2s_b.log 2>&1; echo "rc=$?"; ls $RUN/out/r2s_b/Sashimi_plot; grep -ai -n "error\|Traceback\|No such" $RUN/out/r2s_b.log | head -5
echo "### 4g per-replicate, 6 colours"
rm -rf $RUN/out/r2s_g; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_g --exon_s 1 --intron_s 5 --color '#1f77b4,#1f77b4,#1f77b4,#ff7f0e,#ff7f0e,#ff7f0e' > $RUN/out/r2s_g.log 2>&1; echo "rc=$?"; ls $RUN/out/r2s_g/Sashimi_plot
