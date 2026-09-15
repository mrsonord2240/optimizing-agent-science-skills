# SKILL.md "cyvcf2 Normalization Check" block, verbatim except the input path.
from cyvcf2 import VCF

def needs_normalization(variant):
    if len(variant.ALT) > 1:
        return True
    ref, alt = variant.REF, variant.ALT[0]
    if len(ref) > 1 and len(alt) > 1 and len(ref) == len(alt):
        return True
    return False

total, needs_norm, multiallelic, mnps = 0, 0, 0, 0
for variant in VCF('callerB.vcf.gz'):
    total += 1
    if len(variant.ALT) > 1:
        multiallelic += 1
    ref, alt = variant.REF, variant.ALT[0]
    if len(ref) > 1 and len(alt) > 1 and len(ref) == len(alt):
        mnps += 1
    if needs_normalization(variant):
        needs_norm += 1

print(f'Total variants: {total}')
print(f'Needing normalization: {needs_norm} ({needs_norm/total*100:.1f}%)')
print(f'  Multiallelic sites: {multiallelic}')
print(f'  MNPs: {mnps}')
