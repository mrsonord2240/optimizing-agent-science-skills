"""Misc checks: SKILL.md Ascore-illustration block, pyOpenMS AScore presence, example-script class boundary at 0.75,
chemistry masses quoted in SKILL.md (monoisotopic, computed from element masses)."""
import numpy as np, pandas as pd
from scipy.stats import binom
import pyopenms

def illustrative_localization_score(matched_site_ions, total_ions, depth_p=0.04):
    '''Binomial intuition only; NOT Ascore (no best-vs-second competition or depth sweep).'''
    if total_ions == 0 or matched_site_ions == 0:
        return 0.0
    p_random = 1 - binom.cdf(matched_site_ions - 1, total_ions, depth_p)
    return -10 * np.log10(p_random) if p_random > 0 else 100.0

print('illustrative score (3 of 10 ions, p=0.04):', round(illustrative_localization_score(3, 10), 2))
print('pyopenms', pyopenms.__version__, '| has AScore:', hasattr(pyopenms, 'AScore'),
      '| AScore.compute exists:', hasattr(pyopenms.AScore, 'compute') if hasattr(pyopenms, 'AScore') else None)
# example script's class labels: pd.cut(bins=[0,.25,.5,.75,1], include_lowest=True) vs filter >= 0.75
lab = pd.cut(pd.Series([0.75]), bins=[0, 0.25, 0.5, 0.75, 1.0], labels=['IV', 'III', 'II', 'I'], include_lowest=True)
print('example script: Localization prob 0.75 labelled', lab.iloc[0], 'but kept by the >= 0.75 class-I filter')
m = {'C': 12.0, 'H': 1.00782503207, 'N': 14.0030740048, 'O': 15.99491461956}
f = lambda **k: sum(m[e] * n for e, n in k.items())
gg = f(C=4, H=6, N=2, O=2); cam2 = 2 * f(C=2, H=3, N=1, O=1)
ac = f(C=2, H=2, O=1); me3 = f(C=3, H=6)
print('GlyGly C4H6N2O2 = %.4f | 2x carbamidomethyl 2*C2H3NO = %.4f' % (gg, cam2))
print('acetyl C2H2O = %.4f | trimethyl C3H6 = %.4f | delta = %.4f' % (ac, me3, me3 - ac))
print('deamidation N->D = %.4f | with one 18O: %.4f' % (f(O=1) - f(N=1, H=1), f(O=1) - f(N=1, H=1) + (17.9991610 - 15.99491461956)))
