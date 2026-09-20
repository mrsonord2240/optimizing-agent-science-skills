source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
mkdir -p $RUN/data/jut; cd $RUN/data/jut; P=$RUN/data/planted
cp $RUN/data/rmats_planted/SE.MATS.JC.txt $RUN/data/rmats_planted/SE.MATS.JCEC.txt . 
echo "== convert-results --rmats-dir (planted rMATS-turbo dir)"
mkdir -p jutils_out; jutils.py convert-results --rmats-dir $RUN/data/rmats_planted --out-dir jutils_out 2>&1 | tail -3; ls jutils_out; head -3 jutils_out/*.tsv | cut -c1-300
printf 'G1_rep1\tctrl\nG1_rep2\tctrl\nG1_rep3\tctrl\nG2_rep1\ttrt\nG2_rep2\ttrt\nG2_rep3\ttrt\n' > meta.tsv
for i in 1 2 3; do printf 'G1_rep%s\t%s/G1_rep%s.bam\tctrl\n' $i $P $i; printf 'G2_rep%s\t%s/G2_rep%s.bam\ttrt\n' $i $P $i; done > bam_list.tsv
T=$(ls jutils_out/*.tsv | head -1)
echo "== heatmap (Skill flags: --tsv-file --meta-file --q-value 0.05)"
jutils.py heatmap --tsv-file $T --meta-file meta.tsv --q-value 0.05 --out-dir hm > hm.log 2>&1; echo rc=$?; tail -2 hm.log | cut -c1-200; ls hm 2>/dev/null
echo "== sashimi (Skill flags verbatim: --tsv-file --meta-file --gtf --coordinate --bam-list)"
jutils.py sashimi --tsv-file $T --meta-file meta.tsv --gtf $P/planted.gtf --coordinate chrP:1-1200 --bam-list bam_list.tsv --out-dir sh1 > sh1.log 2>&1; echo rc=$?; tail -3 sh1.log | cut -c1-200; ls sh1 2>/dev/null
echo "== sashimi (README bam-list mode)"
jutils.py sashimi --bam-list bam_list.tsv --coordinate chrP:1-1200 --gtf $P/planted.gtf --out-dir sh2 > sh2.log 2>&1; echo rc=$?; tail -3 sh2.log | cut -c1-200; ls sh2 2>/dev/null
echo "== venn-diagram, Skill form: comma separated --tsv-file-list a.tsv,b.tsv"
jutils.py venn-diagram --tsv-file-list $T,jutils_out/leafcutter.tsv --out-dir vn1 > vn1.log 2>&1; echo rc=$?; tail -3 vn1.log | cut -c1-200; ls vn1 2>/dev/null
echo "== venn-diagram, README form: file listing paths"
printf '%s\trMATS_a\n%s\trMATS_b\n' $PWD/$T $PWD/$T > tsv_list.txt
jutils.py venn-diagram --tsv-file-list tsv_list.txt --out-dir vn2 > vn2.log 2>&1; echo rc=$?; tail -3 vn2.log | cut -c1-200; ls vn2 2>/dev/null
