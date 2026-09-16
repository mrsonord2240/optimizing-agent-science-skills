"""Input 2: per-sample het allele balance from AD (SKILL.md: AB = alt_AD/(ref_AD+alt_AD), GATK does not emit AB),
and sites where QUAL (site) and GQ (genotype) disagree. SYNTHETIC cohort."""
import numpy as np
from cyvcf2 import VCF

vcf = VCF('../../data/cohort.vcf')
samples = vcf.samples
ab = {s: [] for s in samples}
disagree = []
for v in vcf:
    gts = v.gt_types                       # 0=HOM_REF, 1=HET, 2=UNKNOWN, 3=HOM_ALT
    ad = v.format('AD')                    # Number=R: [ref, alt]
    gq = v.format('GQ')
    for i, s in enumerate(samples):
        if gts[i] == 1 and ad[i, 0] >= 0 and ad[i, 1] >= 0 and ad[i].sum() > 0:
            ab[s].append(ad[i, 1] / (ad[i, 0] + ad[i, 1]))
    if v.QUAL is not None and v.QUAL >= 300:
        low = [samples[i] for i in range(len(samples)) if gts[i] in (1, 3) and 0 <= gq[i, 0] < 20]
        if low:
            disagree.append((v.CHROM, v.POS, v.QUAL, low))
print('sample  n_het  mean_AB  frac_AB<0.2_or>0.8')
for s in samples:
    a = np.array(ab[s])
    print(f'{s}  {len(a):5d}  {a.mean():.3f}   {np.mean((a < 0.2) | (a > 0.8)):.3f}')
print(f'\nhigh-QUAL (>=300) sites with a low-GQ (<20) carrier genotype: {len(disagree)}')
for d in disagree[:5]:
    print('  ', d)
