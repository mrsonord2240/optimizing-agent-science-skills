#!/bin/bash
# Input 4 (Variant B): "Case:control is ~1:10 and we suspect cryptic relatedness. Set up SAIGE-GENE+ across MAF
# cutoffs 0.0001, 0.001 and 0.01 with lof / lof+missense / lof+missense+synonymous groups."
# WSL: r-saige 1.3.1 (bioconda, tbb<2021 pinned so SAIGE.so loads) in /tmp/vaca/saige. SYNTHETIC data
# (unrelated by construction, so no sparse GRM is fitted; step 1 uses all array + WES markers).
set -uo pipefail
export PATH=/tmp/vaca/saige/bin:/tmp/vaca/env/bin:$PATH
D=../../data
plink2 --vcf $D/wes.vcf --double-id --make-bed --out geno_wes --silent
bgzip -c $D/array.vcf > a.vcf.gz; bgzip -c $D/wes.vcf > w.vcf.gz; bcftools index -f a.vcf.gz; bcftools index -f w.vcf.gz
bcftools concat -a a.vcf.gz w.vcf.gz -Oz -o all.vcf.gz 2>/dev/null
plink2 --vcf all.vcf.gz --double-id --make-bed --out geno_all --silent
echo "geno_all markers: $(wc -l < geno_all.bim); geno_wes markers: $(wc -l < geno_wes.bim)"
printf 'IID\tY\tage\tsex\tPC1\tPC2\n' > pheno_saige.txt
paste <(awk 'NR>1{print $2"\t"$3}' $D/pheno.txt) <(awk 'NR>1{print $3"\t"$4"\t"$5"\t"$6}' $D/covar.txt) >> pheno_saige.txt
head -2 pheno_saige.txt
# group file (SAIGE >=1.0 format): '<gene> var <ids...>' then '<gene> anno <labels...>', lowercase labels as in SKILL.md
awk '{lab=($3=="LoF")?"lof":$3; v[$2]=v[$2]" "$1; a[$2]=a[$2]" "lab; if(!($2 in seen)){order[++n]=$2; seen[$2]=1}} END{for(i=1;i<=n;i++){g=order[i]; print g" var"v[g]; print g" anno"a[g]}}' $D/annot.txt > groups.txt
head -2 groups.txt | cut -c1-110
Rscript -e 'suppressMessages(library(SAIGE)); cat("SAIGE", as.character(packageVersion("SAIGE")), "\n")'
echo "== step 1: null GLMM with categorical variance ratios (SAIGE docs; the Skill gives only the step-2 command) =="
step1_fitNULLGLMM.R --plinkFile=geno_all --phenoFile=pheno_saige.txt --phenoCol=Y --covarColList=age,sex,PC1,PC2 \
    --sampleIDColinphenoFile=IID --traitType=binary --isCateVarianceRatio=TRUE --outputPrefix=null \
    --nThreads=2 --IsOverwriteVarianceRatioFile=TRUE > step1.log 2>&1
echo "step1 exit=$?"; grep -iE "error|warning" step1.log | head -3; ls -la null.rda null.varianceRatio.txt 2>/dev/null | awk '{print $5, $9}'
echo "== step 2, post-fix SKILL.md bgen command verbatim (no .bgen/.bgi built here: checks argument parsing only) =="
step2_SPAtests.R --bgenFile geno_wes.bgen --bgenFileIndex geno_wes.bgen.bgi --sampleFile samples.txt \
    --groupFile groups.txt \
    --GMMATmodelFile null.rda --varianceRatioFile null.varianceRatio.txt \
    --annotation_in_groupTest "lof,missense;lof,missense;lof;synonymous" \
    --maxMAF_in_groupTest 0.0001,0.001,0.01 --is_output_moreDetails TRUE \
    --SAIGEOutputFile gene_tests_bgen.txt > step2_bgen.log 2>&1
echo "step2 as printed exit=$?"; grep -iE "error|bgenFileIndex|sampleFile" step2_bgen.log | head -3
echo "== step 2 with the Skill's flags, PLINK input =="
step2_SPAtests.R --bedFile=geno_wes.bed --bimFile=geno_wes.bim --famFile=geno_wes.fam --AlleleOrder=alt-first \
    --groupFile=groups.txt --GMMATmodelFile=null.rda --varianceRatioFile=null.varianceRatio.txt \
    --annotation_in_groupTest="lof,missense;lof,missense;lof;synonymous" \
    --maxMAF_in_groupTest=0.0001,0.001,0.01 --is_output_moreDetails=TRUE --LOCO=FALSE \
    --SAIGEOutputFile=gene_tests.txt > step2.log 2>&1
echo "step2 exit=$?"; grep -iE "error" step2.log | head -3
if [ -s gene_tests.txt ]; then
  echo "columns: $(head -1 gene_tests.txt | tr '\t' ' ')"
  echo "== Cauchy-combined rows, smallest p =="
  awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Group"]=="Cauchy" {print $h["Region"], $h["max_MAF"], $h["Pvalue"]}' gene_tests.txt | sort -k3,3g | head -8
  echo "== planted genes, best rows =="
  for g in G01 G11 G21; do awk -F'\t' -v g=$g 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Region"]==g {print $h["Region"], $h["Group"], $h["max_MAF"], $h["Pvalue"], $h["Pvalue_Burden"], $h["Pvalue_SKAT"]}' gene_tests.txt | sort -k4,4g | head -2; done
  echo "null genes Cauchy p<0.05: $(awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Group"]=="Cauchy" && $h["Region"]!~/^G(01|11|21)$/ && $h["Pvalue"]<0.05' gene_tests.txt | wc -l) of $(awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Group"]=="Cauchy" && $h["Region"]!~/^G(01|11|21)$/' gene_tests.txt | wc -l)"
fi
