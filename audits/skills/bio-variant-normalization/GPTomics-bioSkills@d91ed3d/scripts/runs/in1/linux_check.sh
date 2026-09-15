# Cross-check on Linux bcftools 1.21 (bioconda): does the Skill's atomize->split order emit '*' records?
set -u
bcftools --version | head -1
bgzip -c ../../data/callerA.vcf > A.vcf.gz; bcftools index -f A.vcf.gz
echo "skill order (atomize | -m- | -f):"; bcftools norm --atomize A.vcf.gz 2>/dev/null | bcftools norm -m- 2>/dev/null | bcftools norm -f ../../data/ref.fa 2>/dev/null | grep -v '^#' | awk '$2==2000' | cut -f1-5,10
echo "split first:"; bcftools norm -m- A.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | bcftools norm -f ../../data/ref.fa 2>/dev/null | grep -v '^#' | awk '$2==2000' | cut -f1-5,10
echo "annotate from stdin with -a VCF (Linux):"; bgzip -c ../../data/dbsnp_syn.vcf > db.vcf.gz; bcftools index -f db.vcf.gz; bcftools view A.vcf.gz | bcftools annotate -a db.vcf.gz -c ID - 2>&1 | grep -v '^#' | head -2 | cut -f1-5
