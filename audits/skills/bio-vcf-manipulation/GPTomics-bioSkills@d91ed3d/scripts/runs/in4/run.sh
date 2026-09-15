#!/bin/bash
# Input 4: subset cases (S1-S4) from a cohort that carries INFO AC/AN/AF; stale tags; -R vs -T with overlapping BED.
set -uo pipefail
bcftools +fill-tags ../../data/cohort.vcf -Oz -o cohort.vcf.gz -- -t AC,AN,AF 2>/dev/null; bcftools index -f cohort.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Oz -o sub_default.vcf.gz
bcftools view -I -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Oz -o sub_noupdate.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Ou | bcftools +fill-tags -Oz -o sub_filltags.vcf.gz -- -t AC,AN,AF
for f in sub_default sub_noupdate sub_filltags; do
  bcftools query -f '%AC\t%AN\t%AF[\t%GT]\n' $f.vcf.gz | tr -d '\r' | awk -v f=$f '{ac=0;an=0; for(i=4;i<=NF;i++){split($i,g,"/"); for(j in g){if(g[j]!="."){an++; if(g[j]=="1") ac++}}} af=(an?ac/an:0); if($1!=ac) bad_ac++; if($2!=an) bad_an++; if(sprintf("%.4f",$3)!=sprintf("%.4f",af)) bad_af++; n++} END{print f": records "n", AC wrong "bad_ac+0", AN wrong "bad_an+0", AF wrong "bad_af+0}'
done
echo "== -R with overlapping BED regions vs -T =="
printf 'chr1\t5000\t9000\nchr1\t8000\t12000\n' > overlap.bed
echo "unique records in chr1:5001-12000: $(bcftools view -H -r chr1:5001-12000 cohort.vcf.gz | wc -l)"
echo "-R overlap.bed: $(bcftools view -H -R overlap.bed cohort.vcf.gz | wc -l) (distinct: $(bcftools view -H -R overlap.bed cohort.vcf.gz | cut -f1-5 | sort -u | wc -l))"
echo "-T overlap.bed: $(bcftools view -H -T overlap.bed cohort.vcf.gz | wc -l)"
