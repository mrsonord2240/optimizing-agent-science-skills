#!/bin/bash
# Input 5 (Stress): "Compare the raw and hard-filtered callsets: counts removed, Ti/Tv overall and in the novel
# (not-in-dbSNP) fraction, novel% stratified by allele frequency, and a stratified Ti/Tv for a 'difficult'
# region BED." SYNTHETIC cohort; SYNTHETIC dbSNP-like sites file built from the simulation's known IDs.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=3.0||INFO/SOR=".")) || (TYPE="indel" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=200.0||INFO/FS=".") && (INFO/ReadPosRankSum>=-20.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=10.0||INFO/SOR="."))' cohort.vcf.gz -Oz -o filtered.vcf.gz; bcftools index -t -f filtered.vcf.gz
echo "== SKILL.md compare: bcftools stats file1 file2 > cmp.txt =="
bcftools stats cohort.vcf.gz filtered.vcf.gz > cmp.txt; echo "exit=$?"
grep -E "^SN" cmp.txt | grep -E "number of (records|SNPs|indels)"; grep "^TSTV" cmp.txt
echo "(stats with 2 files reports id 0 = private to file1, 1 = private to file2, 2 = shared)"
echo "== novel/known via dbSNP annotate (SKILL.md idiom) =="
bcftools view -G -i 'ID!="."' cohort.vcf.gz -Oz -o dbsnp_syn.vcf.gz; bcftools index -t -f dbsnp_syn.vcf.gz
for f in cohort filtered; do
  bcftools annotate -x ID $f.vcf.gz -Oz -o $f.noid.vcf.gz; bcftools index -t -f $f.noid.vcf.gz
  bcftools annotate -a dbsnp_syn.vcf.gz -c ID $f.noid.vcf.gz -Oz -o $f.annotated.vcf.gz; bcftools index -t -f $f.annotated.vcf.gz
  echo "$f: $(bcftools view -H $f.annotated.vcf.gz | awk '{n++; if($3==".") novel++} END{print "novel:", novel/n}')"
  echo "$f Ti/Tv all=$(bcftools stats $f.annotated.vcf.gz | grep '^TSTV' | cut -f5 | tr -d '\r') known=$(bcftools view -i 'ID!="."' $f.annotated.vcf.gz | bcftools stats | grep '^TSTV' | cut -f5 | tr -d '\r') novel=$(bcftools view -i 'ID="."' $f.annotated.vcf.gz | bcftools stats | grep '^TSTV' | cut -f5 | tr -d '\r')"
done
echo "== novel% stratified by cohort AF (fill-tags AF) =="
bcftools +fill-tags filtered.annotated.vcf.gz -- -t AF 2>/dev/null | bcftools query -f '%ID\t%AF\n' | tr -d '\r' | \
  awk -F'\t' '{b=($2<0.1?"AF<0.1":($2<0.3?"0.1-0.3":">=0.3")); n[b]++; if($1==".") v[b]++} END{for(k in n) printf "%s n=%d novel%%=%.1f\n",k,n[k],100*v[k]/n[k]}'
echo "novel common (AF>=0.3) sites by truth class:"
bcftools +fill-tags filtered.annotated.vcf.gz -- -t AF 2>/dev/null | bcftools query -i 'ID="." && INFO/AF>=0.3' -f '%CHROM\t%POS\n' | tr -d '\r' > novel_common.tsv
awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv novel_common.tsv | sort | uniq -c
echo "== stratified: bcftools stats -R difficult.bed vs -R easy.bed (SKILL.md) =="
printf 'chr1\t5000\t12000\n' > difficult_regions.bed; printf 'chr1\t12000\t20000\nchr2\t0\t15000\n' > easy_regions.bed
for r in easy difficult; do echo "$r: $(bcftools stats -R ${r}_regions.bed cohort.vcf.gz 2>&1 | grep -E '^TSTV|^SN.*number of records' | cut -f3-5 | tr '\n' ' ')"; done
