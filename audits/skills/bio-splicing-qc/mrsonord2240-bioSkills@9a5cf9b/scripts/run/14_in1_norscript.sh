# Input 1c: helper with genuinely no Rscript on PATH (symlink farm of as-core/bin minus Rscript), --plot requested
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic
rm -rf /tmp/fakebin; mkdir /tmp/fakebin
for f in /home/sci/micromamba/envs/as-core/bin/*; do b=$(basename $f); case $b in Rscript*|R) ;; *) ln -s $f /tmp/fakebin/$b;; esac; done
FB=/tmp/fakebin; export PATH=$FB:/usr/bin:/bin
echo "which Rscript -> [$(which Rscript)]"
cd $R/work/in1g
echo "--- literal RSeQC without --skip-plot, Rscript genuinely absent"
$FB/junction_annotation.py -i $D/se_clean.bam -r $D/synth.bed12 -o nr_lit >/dev/null 2>nr_lit.err; echo "rc=$?"; tail -2 nr_lit.err
echo "--- helper --plot, Rscript absent"
python $R/skill/examples/splicing_qc.py annotation $D/se_clean.bam $D/synth.bed12 nr_plot --plot; echo rc=$?
python $R/skill/examples/splicing_qc.py saturation $D/se_sat_mid.bam $D/synth.bed12 nr_sat --plot | cut -c1-300; echo rc=$?
