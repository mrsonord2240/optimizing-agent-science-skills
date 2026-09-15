"""SYNTHETIC TMT10 mzML for the bio-proteomics-quantification audit (2026-09-11). NOT REAL DATA.

24 centroided HCD MS2 spectra (3 proteins x 8 PSMs) interleaved with MS1 scans. Each MS2 carries the ten TMT10
reporter peaks (m/z from MSnbase::TMT10, written to tmt10_reporters.csv) plus 12 random fragment peaks.
True per-channel reporter intensities are known (tmt_truth.csv); the observed peaks include isotopic bleed
applied with the MSnbase built-in TMT10 impurity template (physical model: observed = t(M) %*% true, rows of
M = source reagent), plus 1% multiplicative noise and +/-0.0005 Da m/z jitter.
Channel 131 is a pooled reference (geometric mean of the other nine). Controls = 126..128C (5 channels),
Treatment = 129N..130C (4 channels). Truth: PROT_UP is 2x in Treatment, PROT_NULL flat, PROT_DOWN 0.5x.
"""
import os
import numpy as np
import pandas as pd
import pyopenms as oms

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
rep = pd.read_csv(os.path.join(OUT, 'tmt10_reporters.csv'))
names, mzs = rep['name'].tolist(), rep['mz'].to_numpy()

# MSnbase built-in makeImpuritiesMatrix(10) template (rows = source reagent, cols = observed channel)
M = np.zeros((10, 10))
colmajor = [0.95, 0, 0.003, 0, 0, 0, 0, 0, 0, 0, 0, 0.94, 0, 0.004, 0, 0, 0, 0, 0, 0, 0.05, 0, 0.949, 0, 0.006, 0, 0, 0,
            0, 0, 0, 0.058, 0, 0.955, 0, 0.008, 0, 0.001, 0, 0, 0, 0, 0.048, 0, 0.964, 0, 0.014, 0, 0, 0, 0, 0, 0, 0.041,
            0, 0.957, 0, 0.015, 0, 0.002, 0, 0, 0, 0, 0.03, 0, 0.962, 0, 0.017, 0, 0, 0, 0, 0, 0, 0.035, 0, 0.928, 0,
            0.02, 0, 0, 0, 0, 0, 0, 0.024, 0, 0.965, 0, 0, 0, 0, 0, 0, 0, 0, 0.024, 0, 0.956]
M = np.array(colmajor).reshape(10, 10, order='F')

cond = np.array(['C'] * 5 + ['T'] * 4 + ['R'])  # 126..128C Control, 129N..130C Treatment, 131 reference
fold = {'PROT_UP': 2.0, 'PROT_NULL': 1.0, 'PROT_DOWN': 0.5}
exp = oms.MSExperiment()
psms, truth = [], []
scan = 0
rt = 600.0
for prot, fc in fold.items():
    for k in range(8):
        base = 10 ** rng.uniform(4.5, 6.0)
        true = np.array([base * (fc if c == 'T' else 1.0) for c in cond[:9]]) * rng.lognormal(0, 0.05, 9)
        true = np.append(true, np.exp(np.log(true).mean()))  # pooled reference channel
        obs = M.T @ true * rng.lognormal(0, 0.01, 10)
        # MS1 survey scan
        scan += 1
        s1 = oms.MSSpectrum(); s1.setMSLevel(1); s1.setRT(rt); s1.setNativeID(f'controllerType=0 controllerNumber=1 scan={scan}')
        mz1 = np.sort(rng.uniform(350, 1500, 40)); s1.set_peaks((mz1, rng.uniform(1e5, 1e7, 40)))
        s1.setType(oms.SpectrumSettings.SpectrumType.CENTROID)
        exp.addSpectrum(s1)
        rt += 1.5
        # MS2 with reporters
        scan += 1
        s2 = oms.MSSpectrum(); s2.setMSLevel(2); s2.setRT(rt); s2.setNativeID(f'controllerType=0 controllerNumber=1 scan={scan}')
        p = oms.Precursor(); p.setMZ(float(rng.uniform(400, 1100))); p.setCharge(2); s2.setPrecursors([p])
        frag = np.sort(rng.uniform(150, 1400, 12))
        mz2 = np.concatenate([mzs + rng.uniform(-0.0005, 0.0005, 10), frag])
        it2 = np.concatenate([obs, rng.uniform(1e4, 5e5, 12)])
        order = np.argsort(mz2)
        s2.set_peaks((mz2[order], it2[order]))
        s2.setType(oms.SpectrumSettings.SpectrumType.CENTROID)
        exp.addSpectrum(s2)
        rt += 1.5
        psms.append({'scan': scan, 'ms2_index': len(psms) + 1, 'protein': prot})
        truth.append(dict(scan=scan, protein=prot, **{n: t for n, t in zip(names, true)}))
oms.MzMLFile().store(os.path.join(OUT, 'tmt10_synthetic.mzML'), exp)
pd.DataFrame(psms).to_csv(os.path.join(OUT, 'tmt_psms.csv'), index=False)
pd.DataFrame(truth).to_csv(os.path.join(OUT, 'tmt_truth.csv'), index=False)
print('wrote tmt10_synthetic.mzML with', exp.getNrSpectra(), 'spectra (', len(psms), 'MS2 )')
