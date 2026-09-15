#!/bin/bash
# Input 2 (Variant A): "Annotate my exome VCF with ClinVar CLNSIG/CLNREVSTAT/CLNDN using the weekly VCF and
# list P/LP hits with review status." Real public ClinVar GRCh38 VCF read remotely (region-restricted, tabix)
# in WSL bcftools 1.21; the 'user' VCF is SYNTHETIC: 5 records copied from real ClinVar coordinates in BRCA1,
# written once with 'chr17' (UCSC style) and once with '17' (ClinVar/Ensembl style), no genotypes of any person.
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
URL=https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
bcftools --version | head -1
bcftools view -h $URL > clinvar_header.txt 2> hdr.err; echo "remote header exit=$?"
grep -E "^##fileDate|^##source|^##reference" clinvar_header.txt
echo "INFO tags present: $(grep -o '^##INFO=<ID=[A-Z_]*' clinvar_header.txt | sed 's/##INFO=<ID=//' | tr '\n' ' ')"
for t in CLNSIG CLNREVSTAT CLNDN CLNVC CLNHGVS CLNSIGCONF ONCDN SCIDN CLNSIGSOMATIC ONC SCI; do printf "%s=%s " $t $(grep -c "ID=$t," clinvar_header.txt); done; echo
echo "contig naming: $(bcftools index -s $URL 2>/dev/null | head -3 | cut -f1 | tr '\n' ' ')"
bcftools view -r 17:43044295-43125483 $URL -Oz -o clinvar_brca1.vcf.gz 2>/dev/null; bcftools index -t -f clinvar_brca1.vcf.gz
echo "BRCA1 region records: $(bcftools view -H clinvar_brca1.vcf.gz | wc -l)"
# pick 5 real records: 2 P, 1 conflicting, 1 VUS, 1 benign
{ bcftools view -H -i 'INFO/CLNSIG="Pathogenic" && INFO/CLNREVSTAT~"expert"' clinvar_brca1.vcf.gz | head -2
  bcftools view -H -i 'INFO/CLNSIG~"Conflicting"' clinvar_brca1.vcf.gz | head -1
  bcftools view -H -i 'INFO/CLNSIG="Uncertain_significance"' clinvar_brca1.vcf.gz | head -1
  bcftools view -H -i 'INFO/CLNSIG="Benign"' clinvar_brca1.vcf.gz | head -1; } | cut -f1-5 | sort -k2,2n > picked.tsv
cat picked.tsv
mk() { printf '##fileformat=VCFv4.2\n##contig=<ID=%s,length=83257441>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n' $1; awk -v c=$1 'BEGIN{OFS="\t"}{print c,$2,".",$4,$5,".","PASS","."}' picked.tsv; }
mk 17 | bgzip -c > user_17.vcf.gz; mk chr17 | bgzip -c > user_chr17.vcf.gz
for f in user_17 user_chr17; do bcftools index -t -f $f.vcf.gz; done
echo "== SKILL.md bcftools annotate block (CLNSIG,CLNREVSTAT,CLNDN,CLNVC,CLNHGVS,CLNSIGCONF) =="
for f in user_17 user_chr17; do
  bcftools annotate -a clinvar_brca1.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT,INFO/CLNDN,INFO/CLNVC,INFO/CLNHGVS,INFO/CLNSIGCONF $f.vcf.gz -O z -o $f.annot.vcf.gz 2> $f.err; echo "$f annotate exit=$?"; head -2 $f.err
  bcftools query -f '%CHROM:%POS %REF>%ALT\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' $f.annot.vcf.gz
done
echo "== example annotate_vcf_with_bcftools() command adds INFO/ONCDN,INFO/SCIDN =="
bcftools annotate -a clinvar_brca1.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT,INFO/CLNDN,INFO/CLNVC,INFO/CLNHGVS,INFO/CLNSIGCONF,INFO/ONCDN,INFO/SCIDN user_17.vcf.gz -O z -o ex.annot.vcf.gz 2> ex.err; echo "exit=$?"; head -3 ex.err
echo "== SKILL.md cyvcf2 lookup() on the real BRCA1 slice =="
python lookup_test.py
