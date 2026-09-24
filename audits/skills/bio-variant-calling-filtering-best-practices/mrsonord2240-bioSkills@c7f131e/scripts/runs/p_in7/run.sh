#!/bin/bash
# Input 7 (Adversarial / ambiguous): "Tumor-normal Mutect2 calls. Skip FilterMutectCalls, just run the germline
# hard filter we used before, then keep TLOD>6.3, tumor VAF>5%, tumor DP>20 like your example."
# Checks: (1) the Skill refuses the germline filter for somatic data; (2) the FilterMutectCalls flags exist
# in GATK 4.6.1.0; (3) the SKILL.md bcftools post-filter 'FMT/AF[0]' selects the FIRST sample column,
# which is the NORMAL when the VCF lists the normal first. SYNTHETIC Mutect2-shaped VCF.
set -uo pipefail
source ../env.sh
S=../../data
echo "== FilterMutectCalls flags in GATK 4.6.1.0 =="
$GATK FilterMutectCalls --help 2>&1 | grep -E -- "--contamination-table|--tumor-segmentation|--variant|--reference|--output" | sed 's/^ *//' | cut -c1-90
cat > mutect_syn.vcf <<'EOF'
##fileformat=VCFv4.2
##source=SYNTHETIC_Mutect2_shaped
##contig=<ID=chr1,length=20000>
##INFO=<ID=TLOD,Number=A,Type=Float,Description="Log 10 likelihood ratio score of variant existing versus not existing">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=AF,Number=A,Type=Float,Description="Allele fractions of alternate alleles in the tumor">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">
##normal_sample=SYN_NORMAL
##tumor_sample=SYN_TUMOR
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SYN_NORMAL	SYN_TUMOR
chr1	5100	.	C	T	.	PASS	TLOD=25.3	GT:AD:AF:DP	0/0:40,0:0.012:40	0/1:30,12:0.29:42
chr1	5200	.	G	A	.	PASS	TLOD=18.1	GT:AD:AF:DP	0/0:35,0:0.014:35	0/1:40,8:0.17:48
chr1	5300	.	A	G	.	PASS	TLOD=7.9	GT:AD:AF:DP	0/0:38,1:0.03:39	0/1:50,4:0.07:54
chr1	5400	.	T	C	.	PASS	TLOD=4.1	GT:AD:AF:DP	0/0:30,0:0.016:30	0/1:45,2:0.04:47
chr1	5500	.	G	T	.	PASS	TLOD=60.2	GT:AD:AF:DP	0/1:20,19:0.49:39	0/1:21,20:0.49:41
EOF
bgzip -c mutect_syn.vcf > mutect_syn.vcf.gz; bcftools index -f mutect_syn.vcf.gz
echo "samples (column order): $(bcftools query -l mutect_syn.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "== SKILL.md post-fix somatic block, verbatim (file name substituted) =="
TUMOR=$(bcftools view -h mutect_syn.vcf.gz | grep '^##tumor_sample=' | cut -d= -f2)
T=$(( $(bcftools query -l mutect_syn.vcf.gz | grep -nxF "$TUMOR" | cut -d: -f1) - 1 ))
echo "TUMOR=$TUMOR T=$T"
bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" mutect_syn.vcf.gz -o somatic_final.vcf 2> v.err; echo "filter exit=$?"; head -2 v.err
bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' somatic_final.vcf | tr -d '\r'
echo "(expected somatic keepers 5100,5200,5300; 5500 is a germline het also passing on tumor AF - the Skill states the normal is not tested)"
