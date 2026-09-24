#!/bin/bash
# Input 6 (Scope boundary): "These calls came from DeepVariant. Apply the GATK hard filters to them before
# annotation." The Skill says DL-native caller output must NOT get GATK hard filters. We build a SYNTHETIC
# DeepVariant-shaped VCF (no QD/FS/MQ/SOR/RankSum annotations; FILTER=RefCall on low-QUAL records) and show
# what the GATK expressions actually do to it.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools annotate -x INFO/QD,INFO/FS,INFO/MQ,INFO/SOR,INFO/MQRankSum,INFO/ReadPosRankSum,INFO/ExcessHet cohort.vcf.gz \
  | sed 's/^##source=SYNTHETIC_cohort_GATKlike_raw_joint_callset/##source=SYNTHETIC_DeepVariant_shaped\n##FILTER=<ID=RefCall,Description="Genotyping model thinks this site is reference.">/' \
  | awk 'BEGIN{OFS="\t"} /^#/{print;next} {if($6<40) $7="RefCall"; else $7="PASS"; print}' \
  | bgzip -c > dv.vcf.gz; bcftools index -t -f dv.vcf.gz
echo "DV-shaped records: $(bcftools view -H dv.vcf.gz | wc -l); FILTER: $(bcftools query -f '%FILTER\n' dv.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== (a) guarded bcftools GATK SNP+indel expressions on DV output =="
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=3.0||INFO/SOR=".")) || (TYPE="indel" && QUAL>=30)' dv.vcf.gz 2> a.err | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > a_kept.tsv
head -2 a.err; $PY ../../data/score_truth.py a_kept.tsv "guarded GATK expr on DV (effectively QUAL>=30 only):"
echo "== (b) GATK VariantFiltration SNP command on DV output =="
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V dv.vcf.gz -O dv_gatk.vcf.gz \
    --filter-expression "QD < 2.0" --filter-name "QD2" --filter-expression "FS > 60.0" --filter-name "FS60" \
    --filter-expression "MQ < 40.0" --filter-name "MQ40" --filter-expression "SOR > 3.0" --filter-name "SOR3" 2> b.log; echo "exit=$?"
grep -m3 -iE "warn.*(QD|attribute|JEXL)|undefined" b.log
echo "FILTER after VariantFiltration: $(bcftools query -f '%FILTER\n' dv_gatk.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== (c) what the Skill routes to instead: caller's own FILTER + QUAL/GQ (deepvariant skill idiom) =="
bcftools view -f PASS dv.vcf.gz | bcftools view -i 'QUAL>20 && FMT/GQ>20' | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > c_kept.tsv
$PY ../../data/score_truth.py c_kept.tsv "FILTER=PASS + QUAL>20 & any-sample GQ>20:"
