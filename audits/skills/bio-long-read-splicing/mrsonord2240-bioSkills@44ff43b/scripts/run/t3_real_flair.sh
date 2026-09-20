#!/bin/bash
# Input 1 real-data leg: SKILL recipes on REAL long reads (FLAIR test set: LRGASP WTC-11 cDNA, hg38 chr12/17/20). Copy data; never write into public-data.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test
O=$R/out/real_flair; rm -rf $O; mkdir -p $O; cd $O
cp $P/input/basic.reads.fa $P/input/basic.annotation.gtf $P/input/basic.shortread_junctions.tab $P/input/basic.promoter_regions.bed .
cp $P/genome.fa $P/genome.fa.fai . # copied (286 MB) so no tool can write beside the cached original; deleted at the end
G=$O/genome.fa
LR="micromamba run -n as-lr"
echo "### minimap2 -ax splice:hq -uf --secondary=no (SKILL HiFi recipe) on real cDNA reads"
$LR minimap2 -ax splice:hq -uf --secondary=no -t 8 $G basic.reads.fa 2>mm2.log | $LR samtools sort -o real.bam - 2>/dev/null; $LR samtools index real.bam
$LR samtools flagstat real.bam | head -5
$LR python $R/real_junction_concordance.py real.bam basic.annotation.gtf basic.shortread_junctions.tab
echo "### same reads, ONT recipe minimap2 -ax splice -k14 (no -uf) and with -uf"
$LR minimap2 -ax splice -k14 -t 8 $G basic.reads.fa 2>/dev/null | $LR samtools sort -o real_k14.bam - 2>/dev/null; $LR samtools index real_k14.bam
$LR python $R/real_junction_concordance.py real_k14.bam basic.annotation.gtf basic.shortread_junctions.tab
$LR minimap2 -ax splice -uf -k14 -t 8 $G basic.reads.fa 2>/dev/null | $LR samtools sort -o real_uf_k14.bam - 2>/dev/null; $LR samtools index real_uf_k14.bam
$LR python $R/real_junction_concordance.py real_uf_k14.bam basic.annotation.gtf basic.shortread_junctions.tab
echo "### bedtools bamtobed -bed12 (example script) -> flair correct (flags that exist) with annotation + short-read junction_tab"
$LR bedtools bamtobed -bed12 -i real.bam > real.bed
wc -l real.bed
$LR flair correct -q real.bed -f basic.annotation.gtf --junction_tab basic.shortread_junctions.tab -o rc -t 8 > rc.log 2>&1; echo "correct rc=$? corrected=$(wc -l < rc_all_corrected.bed) inconsistent=$(wc -l < rc_all_inconsistent.bed)"
$LR flair correct -q real.bed -f basic.annotation.gtf -o rc_annonly -t 8 > rc2.log 2>&1; echo "annotation-only correct rc=$? corrected=$(wc -l < rc_annonly_all_corrected.bed) inconsistent=$(wc -l < rc_annonly_all_inconsistent.bed)"
echo "### flair collapse (SKILL flags)"
$LR flair collapse --query rc_all_corrected.bed --reads basic.reads.fa --genome $G --gtf basic.annotation.gtf --output rcoll --threads 8 --generate_map > rcoll.log 2>&1; echo "collapse rc=$?"
tail -2 rcoll.log; grep -c '>' rcoll.isoforms.fa; grep '>' rcoll.isoforms.fa | head -12
$LR flair collapse --query rc_all_corrected.bed --reads basic.reads.fa --genome $G --gtf basic.annotation.gtf --output rcoll_hq --threads 8 --generate_map -p basic.promoter_regions.bed --gene_tss > rcoll_hq.log 2>&1; echo "collapse+promoters rc=$? isoforms=$(grep -c '>' rcoll_hq.isoforms.fa)"
echo "### compare with FLAIR's own expected outputs for the same input"
wc -l $P/expected/test-align.bed $P/expected/test-correct_all_corrected.bed
grep -c '>' $P/expected/test-collapse-annot.isoforms.fa $P/expected/test-collapse.isoforms.fa
echo "### FLAIR-native align on the same reads (not in SKILL.md) for a comparison of alignment counts"
$LR flair align -r basic.reads.fa --genome $G -t 8 -o falign > falign.log 2>&1; echo "flair align rc=$? lines=$(wc -l < falign.bed)"
cut -f1-6 real.bed | sort > a.s; cut -f1-6 falign.bed | sort > b.s; echo "bamtobed vs flair align identical rows (chr,start,end,name,score,strand): $(comm -12 a.s b.s | wc -l) of $(wc -l < a.s)"
rm -f genome.fa genome.fa.fai
