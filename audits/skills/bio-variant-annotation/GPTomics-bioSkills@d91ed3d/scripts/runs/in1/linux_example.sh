# shipped examples/annotate_vcf.sh run as written on Linux bcftools 1.21
bcftools --version | head -1; which bc || echo "bc not installed in this distro"
bash annotate_vcf.upstream_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz lx_out.vcf.gz; echo "exit=$?"
GNOMAD_VCF=gnomad_syn.vcf.gz bash annotate_vcf.upstream_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz lx_out2.vcf.gz; echo "exit(gnomAD branch)=$?"
echo "-- same two-step annotate with an explicit -Ou pipe --"
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Ou | bcftools annotate -a gnomad_syn.vcf.gz -c INFO/AF -Oz -o lx_pipe.vcf.gz; echo "exit=$?"
