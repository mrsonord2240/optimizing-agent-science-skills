# SKILL.md "Write Filtered VCF" + "Fetch Region and Read the Header" blocks, paths adapted.
from cyvcf2 import VCF, Writer

vcf = VCF('cohort.vcf.gz')
writer = Writer('output.vcf', vcf)   # inherit the input header
kept = total = 0
for variant in vcf:
    total += 1
    if variant.QUAL is not None and variant.QUAL > 30:   # QUAL is site-level
        writer.write_record(variant); kept += 1
writer.close()
vcf.close()
print(f'kept {kept}/{total} records with QUAL > 30')

vcf = VCF('cohort.vcf.gz')
print(vcf.samples[:3], vcf.seqnames)
for info in vcf.header_iter():
    if info['HeaderType'] == 'INFO':
        print(info['ID'], info['Description'])
        break
print('records in chr2:1-3000 via index:', sum(1 for _ in vcf('chr2:1-3000')))
