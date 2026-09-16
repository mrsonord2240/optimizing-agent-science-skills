"""Input 3: missing vs hom-ref, AF computed both ways, and the PL/GQ relationship. SYNTHETIC cohort."""
import numpy as np
from cyvcf2 import VCF

vcf = VCF('../../data/cohort.vcf')
S = vcf.samples
miss = np.zeros(len(S), int); n = 0
af_right, af_wrong = [], []
gq_mismatch = 0; checked = 0
for v in vcf:
    n += 1
    g = v.gt_types
    miss += (g == 2)
    called = g != 2
    alt = (g == 1).sum() + 2 * (g == 3).sum()
    af_right.append(alt / (2 * called.sum()) if called.sum() else np.nan)      # ./. excluded
    af_wrong.append(alt / (2 * len(g)))                                         # ./. counted as 0/0 (the trap)
    pl = v.format('PL'); gq = v.format('GQ')
    for i in range(len(S)):
        if called[i] and pl[i, 0] >= 0:
            p = sorted(pl[i, :3]); checked += 1
            if min(99, p[1] - p[0]) != gq[i, 0]:
                gq_mismatch += 1
print('per-sample missingness (./. count / sites):')
for s, m in zip(S, miss):
    print(f'  {s}: {m}/{n} = {m/n:.3f}')
d = np.array(af_right) - np.array(af_wrong)
print(f'AF bias from treating ./. as 0/0: mean {np.nanmean(d):.4f}, max {np.nanmax(d):.4f}')
print(f'GQ == min(99, 2nd-smallest PL - smallest PL): {checked - gq_mismatch}/{checked} genotypes')
