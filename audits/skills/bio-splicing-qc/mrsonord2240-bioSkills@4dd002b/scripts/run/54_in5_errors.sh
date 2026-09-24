# Common Errors table claims: real STAR messages, pysam unindexed fetch
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; P=$ASDATA/rnasplice; S=/mnt/openscience/as-qc-reaudit-scratch/star
mkdir -p $R/work/in5e; cd $R/work/in5e
echo "--- A. sjdbOverhang mismatch (index built with 149, run with 74)"
asenv as-core STAR --runMode alignReads --runThreadN 4 --genomeDir $S/genome_index --sjdbGTFfile $P/reference/genes_chrX.gtf --sjdbOverhang 74 --readFilesIn $P/fastq/ERR188383_chrX_1.fastq.gz $P/fastq/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat --outSAMtype None --outFileNamePrefix ovh_ 2>&1 | grep -iE 'EXITING|overhang|SOLUTION' | head -4
echo "--- B. limitSjdbInsertNsj too small (set 100)"
asenv as-core STAR --runMode alignReads --runThreadN 4 --genomeDir $S/genome_index --sjdbGTFfile $P/reference/genes_chrX.gtf --sjdbFileChrStartEnd $S/run2/cohort_novel_SJ.tab --sjdbOverhang 149 --limitSjdbInsertNsj 100 --readFilesIn $P/fastq/ERR188383_chrX_1.fastq.gz $P/fastq/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat --outSAMtype None --outFileNamePrefix lim_ 2>&1 | grep -iE 'EXITING|LIMIT|SOLUTION' | head -4
echo "--- C. pysam fetch on an unindexed BAM"
asenv as-core python - <<'PY'
import pysam, shutil
shutil.copy('/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188383.Aligned.out.bam', 'noidx.bam')
try: next(pysam.AlignmentFile('noidx.bam').fetch('X', 100000, 200000))
except Exception as e: print(type(e).__name__, e)
PY
echo "--- D. GTF passed as BED to infer_experiment (tail)"
cp $P/reference/genes_chrX.gtf g.bed; cp $P/bam/ERR188383.Aligned.out.bam* .; infer_experiment.py -i ERR188383.Aligned.out.bam -r g.bed 2>&1 | tail -3 | cut -c1-120
