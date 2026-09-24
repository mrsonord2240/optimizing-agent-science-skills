# Input 3: strandedness. B11 (infer_experiment.py) literal on planted PE libraries + NEW SE / MAPQ-1 / wrong-contig / GTF-as-BED cases.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice
mkdir -p $R/work/in3; cd $R/work/in3
asenv as-core python $R/30_in3_make_se.py $D .
for lib in pe_dutp pe_fwd pe_unstr pe_dutp_leak20 pe_dutp_leak40 se_dutp se_fwd; do
  [ -f $lib.bam ] || { cp $D/$lib.bam $lib.bam; cp $D/$lib.bam.bai $lib.bam.bai; }
  echo "=========== $lib"; cp $lib.bam sample.bam; cp $lib.bam.bai sample.bam.bai; cp $D/synth.bed12 genes.bed12
  bash $R/blocks/B11.sh 2>&1 | grep -v '^$'
done
echo "=========== real chrX (unstranded per nf-core test set)"; cp $P/bam/ERR188383.Aligned.out.bam sample.bam; cp $P/bam/ERR188383.Aligned.out.bam.bai .; cp $R/work/in1/real/genes.bed12 genes.bed12
bash $R/blocks/B11.sh 2>&1 | grep -v '^$'
echo "=========== BED6 gene model (SKILL: infer_experiment accepts BED6)"; cp pe_dutp.bam sample.bam; cp pe_dutp.bam.bai sample.bam.bai; cp $D/synth.bed6 genes.bed12
bash $R/blocks/B11.sh 2>&1 | grep -v '^$'
echo "=========== contig mismatch (BED without chr)"; cp $D/synth_nochr.bed12 genes.bed12
bash $R/blocks/B11.sh 2>&1 | grep -v '^$'; echo rc=${PIPESTATUS[0]}
echo "=========== GTF passed as BED"; cp $P/reference/genes_chrX.gtf genes.bed12; cp pe_dutp.bam sample.bam
bash $R/blocks/B11.sh 2>&1 | grep -v '^$' | head -6
echo "=========== MAPQ-1 BAM: default -q 30 then -q 0 (SKILL: pass -q 0)"; cp $D/synth.bed12 genes.bed12; cp pe_dutp_mapq1.bam sample.bam; cp pe_dutp_mapq1.bam.bai sample.bam.bai
bash $R/blocks/B11.sh 2>&1 | grep -v '^$'
infer_experiment.py -i sample.bam -r genes.bed12 -s 200000 -q 0 2>&1 | grep -v '^$'
