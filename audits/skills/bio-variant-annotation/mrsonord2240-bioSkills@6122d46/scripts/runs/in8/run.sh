#!/bin/bash
# Input 8 (NEW, re-audit 2026-09-15, Variant C): "Our VCF uses Ensembl contig names (1, 2) but the gnomAD file uses chr1.
# Add the gnomAD grpmax FAF into its own tag and list the variants absent from gnomAD."
# Tests the SKILL.md annotate line, its Common Errors row (build/chr naming -> --rename-chrs) and the "absent" caveat.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH; export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
DATA=../../data
bgzip -c $DATA/gnomad_syn.vcf > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
sed -e 's/^chr//' -e 's/##contig=<ID=chr/##contig=<ID=/' $DATA/callerA.vcf | bcftools norm -f $DATA/ref.fa -m-any 2>norm.err - -Oz -o nochr.vcf.gz; echo "norm on renamed VCF against chr-named FASTA exit=$?"; head -2 norm.err
sed -e 's/^chr//' -e 's/##contig=<ID=chr/##contig=<ID=/' $DATA/callerA.vcf | bgzip -c > nochr.vcf.gz; bcftools index -f nochr.vcf.gz
echo "contigs: VCF $(bcftools index -s nochr.vcf.gz | cut -f1 | tr -d '\r' | tr '\n' ' ') | gnomAD $(bcftools index -s gnomad_syn.vcf.gz | cut -f1 | tr -d '\r' | tr '\n' ' ')"
echo "== SKILL.md annotate line as written =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max nochr.vcf.gz -Oz -o naive.vcf.gz 2> naive.err; echo "exit=$?"; head -2 naive.err
echo "records with gnomAD_FAF set: $(bcftools view -H -i 'INFO/gnomAD_FAF!="."' naive.vcf.gz 2>/dev/null | wc -l) of $(bcftools view -H nochr.vcf.gz | wc -l)"
echo "== Common Errors fix: bcftools annotate --rename-chrs (on the source) =="
bcftools index -s gnomad_syn.vcf.gz | cut -f1 | tr -d '\r' | awk '{n=$1; sub(/^chr/,"",n); print $1"\t"n}' > chr_map.txt
bcftools annotate --rename-chrs chr_map.txt gnomad_syn.vcf.gz -Oz -o gnomad_nochr.vcf.gz; bcftools index -f gnomad_nochr.vcf.gz
bcftools annotate -a gnomad_nochr.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max nochr.vcf.gz -Oz -o fixed.vcf.gz; echo "exit=$?"
echo "records with gnomAD_FAF set: $(bcftools view -H -i 'INFO/gnomAD_FAF!="."' fixed.vcf.gz | wc -l)"
echo "-- absent from the gnomAD file (FAF='.') --"
bcftools query -i 'INFO/gnomAD_FAF="."' -f '%CHROM:%POS %REF>%ALT\n' fixed.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
echo "-- of those, is any position present in gnomAD with a different allele or a non-PASS filter? --"
bcftools query -i 'INFO/gnomAD_FAF="."' -f '%CHROM\t%POS\n' fixed.vcf.gz | tr -d '\r' > absent_pos.tsv
bcftools view -H -T absent_pos.tsv gnomad_nochr.vcf.gz | cut -f1-2,4-5,7 | tr -d '\r'
