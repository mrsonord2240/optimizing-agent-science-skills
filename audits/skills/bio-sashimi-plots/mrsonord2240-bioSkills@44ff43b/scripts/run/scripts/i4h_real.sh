source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data
head -1 rmats_real/SE.MATS.JC.txt > rmats_real/SE.PDZD11.txt; grep -a '"PDZD11"' rmats_real/SE.MATS.JC.txt >> rmats_real/SE.PDZD11.txt; wc -l rmats_real/SE.PDZD11.txt
D=$ASDATA/rnasplice/bam
B1=$D/ERR188383.Aligned.out.bam,$D/ERR188428.Aligned.out.bam; B2=$D/ERR188454.Aligned.out.bam,$D/ERR204916.Aligned.out.bam
printf 'GBR: 1-2\nYRI: 3-4\n' > real_group.gf
for f in "" "--remove-event-chr-prefix"; do
 n=r2s_real$(echo $f | tr -d ' -')
 rm -rf $RUN/out/$n; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e rmats_real/SE.PDZD11.txt --l1 GBR --l2 YRI -o $RUN/out/$n --exon_s 1 --intron_s 5 --group-info real_group.gf $f > $RUN/out/$n.log 2>&1
 echo "[$n] rc=$? pdfs: $(ls $RUN/out/$n/Sashimi_plot 2>/dev/null | wc -l)"; grep -ai "Error\|Traceback" $RUN/out/$n.log | head -3
done
