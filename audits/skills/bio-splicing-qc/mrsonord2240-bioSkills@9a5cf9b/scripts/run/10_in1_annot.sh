# Input 1: known/novel junction ratio. Runs SKILL.md blocks B05 (RSeQC), B06 (pandas snippet), B01 (helper report) UNEDITED.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run
D=$R/data/synthetic
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice
mkdir -p $R/work/in1; cd $R/work/in1
for lib in se_clean se_novelrich; do
  mkdir -p $lib; cd $lib
  cp $D/$lib.bam sample.bam; cp $D/$lib.bam.bai sample.bam.bai; cp $D/synth.bed12 genes.bed12; cp -r $R/skill/examples .
  echo "=================== $lib"
  echo "--- B05 (RSeQC) literal"; bash $R/blocks/B05.sh 2>&1 | tail -8; echo rc=$?
  echo "--- B06 (pandas snippet) literal"; asenv as-core python $R/blocks/B06.py
  echo "--- B01 (helper report) literal"; asenv as-core python examples/splicing_qc.py report sample.bam genes.bed12 sample_qc; echo rc=$?
  cd ..
done
# real chrX data: BED12 by the SKILL's gffread recipe
mkdir -p real; cd real
cp $P/bam/ERR188383.Aligned.out.bam sample.bam; cp $P/bam/ERR188383.Aligned.out.bam.bai sample.bam.bai; cp -r $R/skill/examples .
echo "=================== real chrX ERR188383 (BED12 from GTF via the Before-You-Run recipe)"
gffread $P/reference/genes_chrX.gtf --bed | cut -f1-12 > genes.bed12; awk -F'\t' '{print NF}' genes.bed12 | sort | uniq -c
bash $R/blocks/B05.sh 2>&1 | tail -8
asenv as-core python $R/blocks/B06.py
asenv as-core python examples/splicing_qc.py report sample.bam genes.bed12 sample_qc; echo rc=$?
cd ..
