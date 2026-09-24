# Input 6b: SpliceAI (B09 command, only edits: files, -A grch37 because the real chrX FASTA/GTF are GRCh37, as the Skill says assembly must match the FASTA)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; P=$ASDATA/rnasplice
mkdir -p $R/work/in6b; cd $R/work/in6b
asenv as-maxent python $R/62_in6b_make_vcf.py $P/reference/genes_chrX.gtf $ASDATA/derived/X.fa variants.vcf
sed -e 's#-R genome.fa -A grch38#-R '$ASDATA'/derived/X.fa -A grch37#' $R/blocks/B09.sh > b09_edit.sh; cat b09_edit.sh | head -1
asenv as-spliceai bash b09_edit.sh > spliceai.log 2>&1; echo rc=$?; tail -2 spliceai.log | cut -c1-200
grep -v '^##' variants.spliceai.vcf | awk -F'\t' 'NR>1{split($8,a,"SpliceAI="); n=split(a[2],al,","); best=0; for(i=1;i<=n;i++){split(al[i],f,"|"); for(k=3;k<=6;k++) if(f[k]+0>best) best=f[k]+0}; printf "%s\t%s\t%s>%s\tmaxDS=%.2f\t%s\n",$3,$2,$4,$5,best,a[2]}'
