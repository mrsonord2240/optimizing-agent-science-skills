# SKILL.md "Local VCF Query" cyvcf2 block verbatim (file path substituted), exercised on picked records.
from cyvcf2 import VCF

clinvar = VCF('clinvar_brca1.vcf.gz')

def lookup(chrom, pos, ref, alt):
    '''Look up by GRCh38 coords. Returns variant-level (VCV) aggregate; not RCV.'''
    for v in clinvar(f'{chrom}:{pos}-{pos}'):
        if v.REF == ref and alt in v.ALT:
            info = v.INFO
            return {
                'vcv_id': info.get('ALLELEID'),
                'clnsig': info.get('CLNSIG'),
                'clnsig_conf': info.get('CLNSIGCONF'),
                'clnrevstat': info.get('CLNREVSTAT'),
                'clndn': info.get('CLNDN'),
                'clnvc': info.get('CLNVC'),
                'clnhgvs': info.get('CLNHGVS'),
                'clndisdb': info.get('CLNDISDB'),
                'oncdn': info.get('ONCDN'),
                'scidn': info.get('SCIDN')
            }
    return None

for line in open('picked.tsv'):
    c, p, vid, r, a = line.rstrip('\n').split('\t')
    res = lookup(c, int(p), r, a)
    print(f'{c}:{p} {r}>{a} ID(VariationID)={vid} -> vcv_id(ALLELEID)={res["vcv_id"] if res else None} clnsig={res["clnsig"] if res else None}')
print('chr17-style query:', lookup('chr17', 43045704, 'A', 'G'))
