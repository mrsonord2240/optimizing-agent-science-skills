# SKILL.md "Python: parse an annotated VCF" block, verbatim except the file names looped over.
import sys
from cyvcf2 import VCF

for path in sys.argv[1:]:
    print(f'## {path}')
    vcf = VCF(path)
    csq_fields = None
    for h in vcf.header_iter():
        if h['HeaderType'] == 'INFO' and h['ID'] == 'CSQ':
            csq_fields = h['Description'].split('Format: ')[1].rstrip('"').split('|')
            break

    for variant in vcf:
        csq = variant.INFO.get('CSQ')
        if not csq:
            continue
        for block in csq.split(','):
            ann = dict(zip(csq_fields, block.split('|')))
            # MANE_SELECT is populated only for the MANE transcript; prefer it over worst-consequence
            if ann.get('MANE_SELECT') and ann.get('IMPACT') in ('HIGH', 'MODERATE'):
                print(variant.CHROM, variant.POS, ann['SYMBOL'], ann['Consequence'])
