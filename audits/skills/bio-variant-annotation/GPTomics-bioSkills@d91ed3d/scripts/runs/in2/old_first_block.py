# The user's legacy approach (first CSQ block) for contrast.
import sys
from cyvcf2 import VCF
for path in sys.argv[1:]:
    for v in VCF(path):
        b = v.INFO.get('CSQ').split(',')[0].split('|')
        print(v.CHROM, v.POS, b[3], b[1], b[2])
