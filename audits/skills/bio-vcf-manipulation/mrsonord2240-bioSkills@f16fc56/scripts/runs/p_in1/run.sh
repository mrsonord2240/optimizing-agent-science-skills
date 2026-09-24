#!/bin/bash
# Input 1 (canonical): build a cohort from single-sample project VCFs with bcftools merge; ./. vs -0.
# (tr -d '\r' strips the CR that the Windows bcftools build writes on stdout.)
set -uo pipefail
C=../../data/cohort.vcf
rm -f files.txt
bgzip -c $C > joint.vcf.gz; bcftools index -f joint.vcf.gz
# single-sample "project VCFs": each sample's non-ref sites only (what a per-sample caller emits)
for s in SYN_S1 SYN_S2 SYN_S3 SYN_S6; do
  bcftools view -s $s -c 1 joint.vcf.gz -Oz -o $s.vcf.gz; bcftools index -f $s.vcf.gz
  echo "$s.vcf.gz" >> files.txt
done
echo "sites per single-sample file: $(for s in SYN_S1 SYN_S2 SYN_S3 SYN_S6; do bcftools view -H $s.vcf.gz | wc -l; done | tr '\n' ' ')"
bcftools merge -l files.txt -Oz -o merged.vcf.gz; bcftools index -f merged.vcf.gz
bcftools merge -0 -l files.txt -Oz -o merged_m0.vcf.gz; bcftools index -f merged_m0.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S6 -c 1 joint.vcf.gz -Oz -o truth4.vcf.gz; bcftools index -f truth4.vcf.gz
for f in truth4 merged merged_m0; do
  bcftools query -f '[%GT\t]\n' $f.vcf.gz | tr -d '\r' > $f.gt
  echo "$f: sites=$(bcftools view -H $f.vcf.gz | wc -l) missing_GT=$(grep -o '\./\.' $f.gt | wc -l) hom_ref=$(grep -o '0/0' $f.gt | wc -l)"
done
echo "== genotype concordance vs the joint call (4 samples) =="
bcftools query -f '%CHROM:%POS[\t%GT]\n' truth4.vcf.gz | tr -d '\r' | sort > t.txt
for f in merged merged_m0; do
  bcftools query -f '%CHROM:%POS[\t%GT]\n' $f.vcf.gz | tr -d '\r' | sort > m.txt
  join t.txt m.txt | awk -v f=$f '{for(i=2;i<=5;i++){n++; if($i==$(i+4)) ok++; else if($(i+4)=="0/0" && $i=="./.") fab++; else if($(i+4)=="0/0") oth++; else if($(i+4)=="./.") mis++}} END{print f": concordant "ok"/"n", 0/0 fabricated where truth is ./. "fab+0", ./. placeholders "mis+0}'
done
echo "== AF of the 4 samples: joint call vs -0 merge (sites where they differ) =="
for f in truth4 merged_m0 merged; do bcftools +fill-tags $f.vcf.gz -- -t AF 2>/dev/null | bcftools query -f '%CHROM:%POS\t%INFO/AF\n' | tr -d '\r' | sort > $f.af; done
join truth4.af merged_m0.af | awk '$2!=$3{d++} END{print "sites with different AF (joint vs -0):", d+0}'
join truth4.af merged.af | awk '$2!=$3{d++; if($3>$2) up++} END{print "sites with different AF (joint vs default ./.):", d+0, " inflated:", up+0}'
