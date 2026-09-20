source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
E=$RUN/data/rmats_planted/SE.MATS.JC.txt
B1=G1_rep1.bam,G1_rep2.bam,G1_rep3.bam; B2=G2_rep1.bam,G2_rep2.bam,G2_rep3.bam
echo "### 4a Skill command VERBATIM (-t SE, --group-info group_def.txt which the Skill never defines)"
rm -rf $RUN/out/r2s_a; rmats2sashimiplot --b1 $B1 --b2 $B2 -t SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_a --exon_s 1 --intron_s 5 --color '#1f77b4,#ff7f0e' --group-info group_def.txt 2>&1 | tr '\r' '\n' | tail -5; echo "rc=${PIPESTATUS[0]}"; ls $RUN/out/r2s_a 2>&1 | head
echo "### 4b --event-type SE, group-info missing file"
rm -rf $RUN/out/r2s_b; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_b --exon_s 1 --intron_s 5 --color '#1f77b4,#ff7f0e' --group-info group_def.txt 2>&1 | tr '\r' '\n' | tail -5; echo "rc=${PIPESTATUS[0]}"; ls $RUN/out/r2s_b 2>&1 | head
echo "### 4c --event-type SE, no group-info (per-replicate plots)"
rm -rf $RUN/out/r2s_c; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_c --exon_s 1 --intron_s 5 --color '#1f77b4,#ff7f0e' 2>&1 | tr '\r' '\n' | tail -4; echo "rc=${PIPESTATUS[0]}"; find $RUN/out/r2s_c -type f | head
echo "### 4d --event-type SE + valid .gf group file"
printf 'Control: 1-3\nTreatment: 4-6\n' > grouping.gf
rm -rf $RUN/out/r2s_d; rmats2sashimiplot --b1 $B1 --b2 $B2 --event-type SE -e $E --l1 Control --l2 Treatment -o $RUN/out/r2s_d --exon_s 1 --intron_s 5 --group-info grouping.gf --color '#1f77b4,#ff7f0e' 2>&1 | tr '\r' '\n' | tail -4; echo "rc=${PIPESTATUS[0]}"; find $RUN/out/r2s_d -type f | head
echo "### converters available?"; which gs mutool convert pdftotext pdftoppm 2>&1; micromamba run -n as-viz python -c "import fitz" 2>&1 | tail -1; micromamba run -n as-viz python -c "import pypdf; print('pypdf')" 2>&1 | tail -1; micromamba run -n as-viz python -c "import matplotlib; print('mpl', matplotlib.__version__)" 2>&1 | tail -1
