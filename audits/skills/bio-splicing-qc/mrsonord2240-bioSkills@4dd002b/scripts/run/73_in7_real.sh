# Input 7b (NEW): B10's awk refFlat + Picard + geneBody on the REAL chrX library (unstranded per nf-core; STAR). No rRNA locus exists on chrX, so RIBOSOMAL_INTERVALS is dropped.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; P=$ASDATA/rnasplice
mkdir -p $R/work/in7/real; cd $R/work/in7/real
cp $P/bam/ERR188383.Aligned.out.bam sample.bam; cp $P/bam/ERR188383.Aligned.out.bam.bai sample.bam.bai; cp $R/work/in1/real/genes.bed12 .
cp $R/work/b10_real_picard.sh b10_picard.sh; micromamba run -n af-picard3 bash b10_picard.sh > picard.log 2>&1; echo picard rc=$?; tail -3 picard.log
asenv as-core geneBody_coverage.py -i sample.bam -r genes.bed12 -o sample_geneBody --skip-plot > gb.log 2>&1; echo geneBody rc=$?
asenv as-core python $R/72_in7_real_picard.py sample.bam genes.bed12 refFlat.txt sample.rna_metrics.txt
asenv as-core python - <<'PY'
rows = [l.split('\t') for l in open('sample_geneBody.geneBodyCoverage.txt').read().strip().splitlines()]
v = [float(x) for x in rows[1][1:]]; print('geneBody 100 bins: 5p(first10)/3p(last10) = %.3f' % (sum(v[:10]) / sum(v[-10:])))
PY
