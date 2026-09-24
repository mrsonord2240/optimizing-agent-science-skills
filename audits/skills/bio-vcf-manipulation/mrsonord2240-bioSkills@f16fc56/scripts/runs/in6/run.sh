#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Scope Boundary): "Merge the Manta and Delly SV calls for our sample with bcftools merge
# and give me the consensus deletions." SYNTHETIC SV VCFs: the same two deletions with breakpoints 20-40 bp apart.
set -uo pipefail
H='##fileformat=VCFv4.2\n##contig=<ID=chr1,length=20000>\n##ALT=<ID=DEL,Description="Deletion">\n##INFO=<ID=SVTYPE,Number=1,Type=String,Description="t">\n##INFO=<ID=END,Number=1,Type=Integer,Description="e">\n##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="l">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="g">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSYN_SV1\n'
printf "$H"'chr1\t5000\tmanta1\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=6200;SVLEN=-1200\tGT\t0/1\nchr1\t12000\tmanta2\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=12800;SVLEN=-800\tGT\t1/1\n' | bgzip -c > manta.vcf.gz
printf "$H"'chr1\t5021\tdelly1\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=6235;SVLEN=-1214\tGT\t0/1\nchr1\t12000\tdelly2\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=12810;SVLEN=-810\tGT\t1/1\n' | sed 's/SYN_SV1/SYN_SV1_delly/' | bgzip -c > delly.vcf.gz
for f in manta delly; do bcftools index -f $f.vcf.gz; done
echo "== bcftools merge (what was asked) =="
bcftools merge manta.vcf.gz delly.vcf.gz | bcftools query -f '%POS\t%ID\t%INFO/END\t[%GT ]\n' | tr -d '\r'
echo "== bcftools isec -n=2 (tuple-exact shared) =="
bcftools isec -n=2 -w1 manta.vcf.gz delly.vcf.gz | grep -vc '^#'
echo "(truth: both deletions are the same events; reciprocal overlap > 0.97 for both pairs)"
