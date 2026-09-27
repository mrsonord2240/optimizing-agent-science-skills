#!/usr/bin/env python3
# Byte-copy of the "Per-sample genotype distribution" snippet from
# skills/bio-vcf-statistics/usage-guide.md (post-trim, commit ffa74e9).
# Only the VCF path at the bottom (sys.argv) was added to make it runnable as a script;
# the snippet body between the markers is otherwise character-for-character identical
# to the usage-guide.md fenced code block.
import sys
from cyvcf2 import VCF

vcf = VCF(sys.argv[1])
samples = vcf.samples
hom_ref = [0] * len(samples); het = [0] * len(samples)
hom_alt = [0] * len(samples); missing = [0] * len(samples)

for variant in vcf:
    for i, gt in enumerate(variant.gt_types):   # cyvcf2 codes: 0 hom-ref, 1 het, 2 unknown, 3 hom-alt
        if gt == 0:
            hom_ref[i] += 1
        elif gt == 1:
            het[i] += 1
        elif gt == 3:
            hom_alt[i] += 1
        else:
            missing[i] += 1

for i, s in enumerate(samples):
    ratio = het[i] / hom_alt[i] if hom_alt[i] else 0
    print(f'{s}: het/hom={ratio:.2f} HET={het[i]} HOM_ALT={hom_alt[i]} MISS={missing[i]}')
