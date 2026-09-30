# Audit run: Skill workflow steps 4-5 (bedtools slop -l 200 -r 1000 on TSS -> nucleoatac run) + documented install recipe re-test.
export PATH=$NPENV/bin:$PATH
D=$ATACDATA; W=$NP/work/a3; rm -rf $W; mkdir -p $W; cd $W
samtools merge -f -@4 merged.bam $D/encode/GM12878_rep1_filtered.chr1_1-30000000.bam $D/encode/GM12878_rep2_filtered.chr1_1-30000000.bam && samtools index merged.bam
awk '$2>10000000 && $2<20000000' $D/annotation/gencode_v29_protein_coding_tss.chr1.bed | cut -f1-3 > tss.bed
bedtools slop -i tss.bed -g $D/reference/hg38.chr1.chrom.sizes -l 200 -r 1000 | sort -k1,1 -k2,2n | bedtools merge -i - > regions.bed
echo "TSS $(wc -l < tss.bed) regions $(wc -l < regions.bed)"
export PATH=$SHARED/tools/bin:$PATH
nucleoatac run --bed regions.bed --bam merged.bam --fasta $D/reference/hg38.chr1.fa --out out --cores 8 > run.log 2>&1; echo "nucleoatac rc=$?"
for f in out.*.gz; do echo "$f $(zcat $f | wc -l)"; done
export PATH=$NPENV/bin:$PATH
python $NP/../../audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930/scripts/a3_check.py
echo "---- documented install recipe (py3.7 env, pip install nucleoatac) ----"
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
$NPNA37/bin/python --version
$NPNA37/bin/pip install nucleoatac 2>&1 | tail -4
