# Two remaining Skill claims: (1) Jutils --tsv-file-list wants a FILE, comma list -> FileNotFoundError; (2) rmats2sashimiplot without --group-info: one plot per replicate with one colour per replicate
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/out/i6_jutils_planted; J="micromamba run -n as-viz-gg34 python3 $SRC/Jutils/jutils.py"
$J venn-diagram --tsv-file-list jutils_out/rmats_JC_results.tsv,jutils_out/rmats_JCEC_results.tsv --out-dir vn_comma > vn_comma.log 2>&1; echo "comma list rc=$?"; grep -a -E "Error" vn_comma.log | head -2
cd $RUN/out/i3_planted; P=$AS/public-data/planted
rm -rf sashimi_perrep; rmats2sashimiplot --b1 G1_rep1.bam,G1_rep2.bam,G1_rep3.bam --b2 G2_rep1.bam,G2_rep2.bam,G2_rep3.bam --event-type SE -e sig.SE.MATS.JC.txt --l1 Control --l2 Treatment -o sashimi_perrep --exon_s 1 --intron_s 5 --color '#1f77b4,#1f77b4,#1f77b4,#ff7f0e,#ff7f0e,#ff7f0e' > perrep.log 2>&1; echo "6 colours no group-info rc=$? pdfs=$(find sashimi_perrep/Sashimi_plot -name '*.pdf' | wc -l)"
find sashimi_perrep/Sashimi_plot -name '*.pdf' | head -2
