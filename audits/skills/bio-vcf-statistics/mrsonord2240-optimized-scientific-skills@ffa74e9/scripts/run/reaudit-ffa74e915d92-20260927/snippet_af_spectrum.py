#!/usr/bin/env python3
# Byte-copy of the "Allele-frequency spectrum" snippet from
# skills/bio-vcf-statistics/usage-guide.md (post-trim, commit ffa74e9).
# Only the VCF path at the bottom (sys.argv) and a final print(bins) were added;
# the snippet body is otherwise character-for-character identical to the
# usage-guide.md fenced code block.
import sys
from cyvcf2 import VCF

bins = {'rare(<1%)': 0, 'low(1-5%)': 0, 'common(5-50%)': 0, 'frequent(>50%)': 0}
for variant in VCF(sys.argv[1]):
    af = variant.INFO.get('AF')
    if af is None:
        continue
    af = af[0] if isinstance(af, tuple) else af
    if af < 0.01:
        bins['rare(<1%)'] += 1
    elif af < 0.05:
        bins['low(1-5%)'] += 1
    elif af < 0.5:
        bins['common(5-50%)'] += 1
    else:
        bins['frequent(>50%)'] += 1
print(bins)
