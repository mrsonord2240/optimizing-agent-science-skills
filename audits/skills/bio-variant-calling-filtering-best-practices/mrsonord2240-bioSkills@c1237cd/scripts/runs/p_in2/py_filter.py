# SKILL.md "Python Filtering (cyvcf2)" block, verbatim except the input path (SYNTHETIC SNP VCF).
from cyvcf2 import VCF, Writer

vcf = VCF('snps.vcf.gz')
writer = Writer('filtered.vcf', vcf)
for variant in vcf:
    qual = variant.QUAL or 0
    dp = variant.INFO.get('DP') or 1e9      # missing depth => do not fail on depth
    fs = variant.INFO.get('FS') or 0.0      # missing strand bias => pass (None -> 0)
    mq = variant.INFO.get('MQ') or 1e9      # missing MQ => pass
    if qual >= 30 and dp >= 10 and fs <= 60.0 and mq >= 40.0:
        writer.write_record(variant)
writer.close(); vcf.close()
