# Exit codes of the helper CLI on the failure modes (direct $?, no pipe)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic; cd $R/work/in1g
H="asenv as-core python examples/splicing_qc.py"
$H annotation $D/se_clean.bam $D/synth.bed6 x1 >x1.out 2>x1.err; echo "BED6 rc=$? stderr: $(cut -c1-90 x1.err)"
$H saturation $D/se_sat_mid.bam $D/synth_nochr.bed12 x2 >x2.out 2>x2.err; echo "contig mismatch rc=$? stderr: $(cut -c1-90 x2.err)"
$H report unspliced.bam $D/synth.bed12 x3 >x3.out 2>x3.err; echo "no spliced reads rc=$? stderr: $(cut -c1-90 x3.err)"
$H annotation $D/se_clean.bam $D/synth.bed12 x4 >x4.out 2>x4.err; echo "good input rc=$? ; keys: $(cut -c1-60 x4.out)"
$H sites --donor CAGGTAAGT --donor NNNNNNNNN --acceptor TTTTTTTTTTTTTTCCTTAGGAG >x5.out 2>x5.err; echo "sites rc=$? $(cat x5.out)"
