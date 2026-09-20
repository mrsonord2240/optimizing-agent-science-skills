#!/bin/bash
# Input 5 (stress): cohort-style STAR 2-pass exactly as in SKILL.md, on the 4 real chrX GEUVADIS samples (2x75, ~50k pairs each).
# Adaptations (noted in the report): paths, --runThreadN 8, --sjdbOverhang 74 (=readlen-1; SKILL.md's 149 is for 2x150).
# Run: wsl_run.sh 'bash /mnt/openscience/audits/bio-splicing-qc/run/input5_star_2pass.sh'
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
set -u
W=/mnt/openscience/audits/bio-splicing-qc/run/work/in5
mkdir -p $W && cd $W
FQ=$ASDATA/rnasplice/fastq
GTF=$ASDATA/rnasplice/reference/genes_chrX.gtf
FA=$ASDATA/derived/X.fa
SAMPLES="ERR188383 ERR188428 ERR188454 ERR204916"

if [ ! -f genome_index/SA ]; then
  echo "== genomeGenerate (no GTF; SKILL.md inserts the GTF at mapping time)"
  STAR --runMode genomeGenerate --runThreadN 8 --genomeDir genome_index --genomeFastaFiles $FA \
       --genomeSAindexNbases 12 --outFileNamePrefix idx_ > idx.stdout 2>&1
  tail -2 idx.stdout
fi

echo "== PASS 1 (verbatim flags from SKILL.md)"
for sample in $SAMPLES; do
  STAR --runMode alignReads \
      --runThreadN 8 \
      --genomeDir genome_index \
      --sjdbGTFfile $GTF \
      --sjdbOverhang 74 \
      --readFilesIn $FQ/${sample}_chrX_1.fastq.gz $FQ/${sample}_chrX_2.fastq.gz \
      --readFilesCommand zcat \
      --outSAMtype BAM SortedByCoordinate \
      --outFileNamePrefix pass1_${sample}_ \
      --outSJtype Standard \
      --outFilterMultimapNmax 20 \
      --alignSJoverhangMin 8 \
      --alignSJDBoverhangMin 1 > pass1_${sample}.stdout 2>&1
  echo "$sample pass1 rc=$? SJ lines: $(wc -l < pass1_${sample}_SJ.out.tab)"
  grep -E "Uniquely mapped reads (number|%)" pass1_${sample}_Log.final.out
done

echo "== cohort merge (verbatim awk from SKILL.md)"
cat pass1_*_SJ.out.tab | awk '$5 > 0 && $7 >= 3' | sort -u > cohort_novel_SJ.tab
echo "cohort_novel_SJ.tab lines: $(wc -l < cohort_novel_SJ.tab)"
echo "distinct (chr,start,end) keys: $(cut -f1-3 cohort_novel_SJ.tab | sort -u | wc -l)"
echo "col4 (strand) values in merged file:"; cut -f4 cohort_novel_SJ.tab | sort | uniq -c
echo "col5 (motif) values in merged file:"; cut -f5 cohort_novel_SJ.tab | sort | uniq -c
echo "col6 (annotated) values in merged file:"; cut -f6 cohort_novel_SJ.tab | sort | uniq -c
echo "columns in pass1 SJ.out.tab: $(head -1 pass1_ERR188383_SJ.out.tab | awk '{print NF}')"
echo "rows in pass1 ERR188383 with col5==0 (non-canonical): $(awk '$5==0' pass1_ERR188383_SJ.out.tab | wc -l); with col4==0 (undefined strand): $(awk '$4==0' pass1_ERR188383_SJ.out.tab | wc -l); col5==0 AND col4==0: $(awk '$5==0 && $4==0' pass1_ERR188383_SJ.out.tab | wc -l)"

echo "== PASS 2 (verbatim flags from SKILL.md)"
for sample in $SAMPLES; do
  STAR --runMode alignReads \
      --runThreadN 8 \
      --genomeDir genome_index \
      --sjdbGTFfile $GTF \
      --sjdbFileChrStartEnd cohort_novel_SJ.tab \
      --sjdbOverhang 74 \
      --readFilesIn $FQ/${sample}_chrX_1.fastq.gz $FQ/${sample}_chrX_2.fastq.gz \
      --readFilesCommand zcat \
      --outSAMtype BAM SortedByCoordinate \
      --outFileNamePrefix pass2_${sample}_ \
      --outSJtype Standard \
      --twopassMode None \
      --quantMode GeneCounts \
      --alignSJoverhangMin 8 \
      --alignSJDBoverhangMin 3 > pass2_${sample}.stdout 2>&1
  echo "$sample pass2 rc=$? SJ lines: $(wc -l < pass2_${sample}_SJ.out.tab) ReadsPerGene: $(ls pass2_${sample}_ReadsPerGene.out.tab 2>/dev/null | wc -l)"
  grep -E "Uniquely mapped reads (number|%)" pass2_${sample}_Log.final.out
done
grep -i -E "sjdb|inserted|junctions" pass2_ERR188383_Log.out | head -12

echo "== 1-pass vs cohort 2-pass junction counts (ERR188383, unique reads >=1)"
echo "pass1 SJ rows: $(wc -l < pass1_ERR188383_SJ.out.tab)   pass2 SJ rows: $(wc -l < pass2_ERR188383_SJ.out.tab)"

echo "== per-sample --twopassMode Basic (ERR188383) for comparison"
STAR --runMode alignReads --runThreadN 8 --genomeDir genome_index --sjdbGTFfile $GTF --sjdbOverhang 74 \
  --readFilesIn $FQ/ERR188383_chrX_1.fastq.gz $FQ/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate --outFileNamePrefix basic_ERR188383_ --twopassMode Basic \
  --alignSJoverhangMin 8 --alignSJDBoverhangMin 3 > basic.stdout 2>&1
echo "basic rc=$? SJ rows: $(wc -l < basic_ERR188383_SJ.out.tab)"

echo "== XS tags in pass2 BAM (SKILL.md STAR commands do not pass --outSAMstrandField intronMotif)"
samtools view pass2_ERR188383_Aligned.sortedByCoord.out.bam | awk '$6 ~ /N/' | head -20000 | awk '{x=0; for(i=12;i<=NF;i++) if($i ~ /^XS:/) x=1; s++; t+=x} END{print "spliced reads sampled:", s, "with XS:", t}'

echo "== error strings: limitSjdbInsertNsj and sjdbOverhang mismatch"
STAR --runMode alignReads --runThreadN 4 --genomeDir genome_index --sjdbGTFfile $GTF --sjdbFileChrStartEnd cohort_novel_SJ.tab --sjdbOverhang 74 --limitSjdbInsertNsj 10 \
  --readFilesIn $FQ/ERR188383_chrX_1.fastq.gz $FQ/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat --outSAMtype None --outFileNamePrefix lim_ > lim.stdout 2>&1
echo "limitSjdbInsertNsj=10 rc=$?"; grep -i -E "EXITING|fatal|limitSjdb" lim.stdout lim_Log.out | head -4
if [ ! -f genome_index_sjdb100/SA ]; then
  STAR --runMode genomeGenerate --runThreadN 8 --genomeDir genome_index_sjdb100 --genomeFastaFiles $FA --sjdbGTFfile $GTF --sjdbOverhang 100 \
       --genomeSAindexNbases 12 --outFileNamePrefix idx2_ > idx2.stdout 2>&1
fi
STAR --runMode alignReads --runThreadN 4 --genomeDir genome_index_sjdb100 --sjdbOverhang 74 \
  --readFilesIn $FQ/ERR188383_chrX_1.fastq.gz $FQ/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat --outSAMtype None --outFileNamePrefix ovh_ > ovh.stdout 2>&1
echo "sjdbOverhang mismatch rc=$?"; grep -i -E "EXITING|fatal|sjdbOverhang" ovh.stdout ovh_Log.out | head -4
echo "== literal --sjdbOverhang 149 with 75-nt reads (pass 1 command as printed)"
STAR --runMode alignReads --runThreadN 8 --genomeDir genome_index --sjdbGTFfile $GTF --sjdbOverhang 149 \
  --readFilesIn $FQ/ERR188383_chrX_1.fastq.gz $FQ/ERR188383_chrX_2.fastq.gz --readFilesCommand zcat --outSAMtype None --outFileNamePrefix lit149_ --outSJtype Standard > lit149.stdout 2>&1
echo "sjdbOverhang 149 rc=$?  SJ rows: $(wc -l < lit149_SJ.out.tab)"
echo "== samtools -F 0x100 -F 0x800 semantics (SKILL.md Common Errors row)"
BAM=pass1_ERR188383_Aligned.sortedByCoord.out.bam
echo "records: $(samtools view -c $BAM)  secondary(0x100): $(samtools view -c -f 0x100 $BAM)  supplementary(0x800): $(samtools view -c -f 0x800 $BAM)"
echo "-F 0x100 -F 0x800  -> $(samtools view -c -F 0x100 -F 0x800 $BAM)   ;  -F 0x900 -> $(samtools view -c -F 0x900 $BAM)  ;  -F 0x100 -> $(samtools view -c -F 0x100 $BAM)  ; -F 0x800 -> $(samtools view -c -F 0x800 $BAM)"
echo DONE
