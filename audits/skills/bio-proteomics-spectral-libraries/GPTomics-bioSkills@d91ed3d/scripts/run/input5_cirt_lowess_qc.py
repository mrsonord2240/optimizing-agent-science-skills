"""Input 5 (Stress/complex, multi-part): "I have no iRT spike-in -- calibrate
retention time using CiRT endogenous peptides" + "My gradient is nonlinear;
use a LOWESS fit instead of a linear iRT alignment" + final QC report on the
resulting library (precursors/proteins/transitions), all in one request --
exercising three separate Skill capabilities together.
"""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess

# CiRT (common internal retention time) endogenous peptide set (subset; real CiRT
# has 143 peptides with published iRT values - Parker et al. 2015).
CIRT_PEPTIDES = {
    'GAGSSEPVTGLDAK': 0.00, 'VEATFGVDESNAK': 12.39, 'YILAGVENSK': 19.79,
    'TPVISGGPYEYR': 28.71, 'DGLDAASYYAPVR': 42.26, 'ADVTPADFSEWSK': 54.62,
    'GTFIIDPGGVIR': 70.52, 'GTFIIDPAAVIR': 87.23,
}

rng = np.random.default_rng(7)
anchors = pd.DataFrame({'peptide': list(CIRT_PEPTIDES), 'cirt': list(CIRT_PEPTIDES.values())})
# simulate a NONLINEAR gradient (a mild curvature a linear fit will not capture well)
true_rt = 5.0 + 0.22 * anchors['cirt'] + 0.0015 * anchors['cirt'] ** 2
anchors['observed_rt'] = true_rt + rng.normal(0, 0.2, len(anchors))

# 1) naive linear fit (what the Skill warns against for nonlinear gradients)
slope, intercept, r, _, _ = stats.linregress(anchors['cirt'], anchors['observed_rt'])
print(f'Linear CiRT fit: RT = {slope:.4f}*CiRT + {intercept:.4f}, R^2 = {r**2:.4f}')

# 2) LOWESS fit as the Skill recommends for nonlinear gradients
smoothed = lowess(anchors['observed_rt'], anchors['cirt'], frac=0.6, return_sorted=True)
lowess_x, lowess_y = smoothed[:, 0], smoothed[:, 1]
lowess_pred = np.interp(anchors['cirt'], lowess_x, lowess_y)
resid_linear = anchors['observed_rt'] - (slope * anchors['cirt'] + intercept)
resid_lowess = anchors['observed_rt'] - lowess_pred
print(f'Residual SS linear = {np.sum(resid_linear**2):.4f}, LOWESS = {np.sum(resid_lowess**2):.4f}')
print('LOWESS reduces residual SS:', np.sum(resid_lowess**2) < np.sum(resid_linear**2))

# 3) Apply the LOWESS calibration to a predicted library's iRT column and QC the result
lib = pd.DataFrame({
    'ModifiedSequence': ['LGGNEQVTR', 'LGGNEQVTR', 'VEATFGVDESNAK', 'YILAGVENSK'],
    'PrecursorCharge': [2, 3, 2, 2],
    'ProteinId': ['P1', 'P1', 'P2', 'P3'],
    'iRT_predicted': [-24.92, -24.92, 12.39, 19.79],
})
lib['RT_calibrated'] = np.interp(lib['iRT_predicted'], lowess_x, lowess_y)
n_prec = lib.groupby(['ModifiedSequence', 'PrecursorCharge']).ngroups
print('QC report -> precursors:', n_prec, '| proteins:', lib['ProteinId'].nunique(),
      '| rows:', len(lib))
print(lib[['ModifiedSequence', 'PrecursorCharge', 'iRT_predicted', 'RT_calibrated']])
