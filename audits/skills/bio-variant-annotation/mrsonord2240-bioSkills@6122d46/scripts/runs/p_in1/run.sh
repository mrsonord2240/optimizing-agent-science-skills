#!/bin/bash
# Input 1 (canonical, post-fix regression 2026-09-15): normalize -> rsID -> gnomAD FAF -> ClinVar -> bcftools csq -> triage;
# then the post-fix usage-guide Basic and Clinical recipes and the shipped example, all verbatim (file names substituted).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH; export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
DATA=../../data
echo "### $(bcftools --version | head -1)"
for db in dbsnp_syn gnomad_syn clinvar_syn; do bgzip -c $DATA/$db.vcf > $db.vcf.gz; bcftools index -f $db.vcf.gz; done
bgzip -c $DATA/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>norm.log; bcftools index -f norm.vcf.gz; cat norm.log
echo "== SKILL.md csq/annotate block (post-fix, verbatim) =="
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 norm.vcf.gz -Oz -o csq.vcf.gz; echo "csq exit=$?"
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o rsid.vcf.gz; echo "rsID annotate exit=$?"
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max rsid.vcf.gz -Oz -o af.vcf.gz; echo "gnomAD annotate on UNINDEXED rsid.vcf.gz exit=$?"
echo "== continue to ClinVar and triage =="
bcftools index -f af.vcf.gz
bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT af.vcf.gz -Oz -o a3.vcf.gz; bcftools index -f a3.vcf.gz
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 a3.vcf.gz -Oz -o csq3.vcf.gz; bcftools index -f csq3.vcf.gz
bcftools query -f '%CHROM:%POS\t%REF>%ALT\t%ID\t%INFO/BCSQ\t%INFO/gnomAD_FAF\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' csq3.vcf.gz | tr -d '\r'
echo "== usage-guide Basic Pipeline (post-fix, verbatim) =="
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o with_ids.vcf.gz; echo "exit=$?"
bcftools index -f with_ids.vcf.gz
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_AF:=INFO/AF with_ids.vcf.gz -Oz -o annotated.vcf.gz; echo "exit=$?"
bcftools index -f annotated.vcf.gz
bcftools query -f '%POS\t%ID\tgnomAD_AF=%INFO/gnomAD_AF\n' annotated.vcf.gz | tr -d '\r'
echo "== usage-guide Clinical Variant Analysis (post-fix, verbatim) =="
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz -Oz -o cnorm.vcf.gz; bcftools index -f cnorm.vcf.gz
bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNDN cnorm.vcf.gz -Oz -o with_clinvar.vcf.gz; echo "clinvar exit=$?"
bcftools index -f with_clinvar.vcf.gz
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 with_clinvar.vcf.gz -Ou | \
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' -Oz -o pathogenic.vcf.gz; echo "exit=${PIPESTATUS[*]}"
bcftools query -f '%POS\t%INFO/CLNSIG\t%INFO/BCSQ\n' pathogenic.vcf.gz | tr -d '\r' | cut -c1-120
echo "== shipped examples/annotate_vcf.sh (fork commit, verbatim) =="
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/variant-annotation/examples/annotate_vcf.sh > annotate_vcf.fork_copy.sh
bash annotate_vcf.fork_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz ex_out.vcf.gz; echo "exit=$?"
GNOMAD_VCF=gnomad_syn.vcf.gz bash annotate_vcf.fork_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz ex_out2.vcf.gz; echo "exit(gnomAD branch)=$?"
bcftools query -f '%POS\t%ID\tgnomAD_AF=%INFO/gnomAD_AF\tAF=%INFO/AF\n' ex_out2.vcf.gz | tr -d '\r'
