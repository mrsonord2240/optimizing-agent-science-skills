"""SYNTHETIC mzML for the bio-proteomics-data-import audit (2026-09-11). NOT REAL DATA.

Writes data/synthetic_mixed.mzML with pyOpenMS 3.5:
  - 3 DDA cycles: 1 MS1 (500 peaks) + 3 MS2 each (precursor m/z, charge, symmetric 0.8/0.8 Th isolation offsets)
  - 1 DIA cycle: 1 MS1 + 4 MS2 with 12.5/12.5 Th windows (precursor m/z = window centre, charge 0)
  - 1 MS2 whose isolation-window offsets were never written (offsets 0 -> width 0)
  - 1 all-ion-fragmentation (AIF/MSE-style) MS2 scan with NO precursor element
  - 1 asymmetric-window MS2 (lower 0.5 / upper 1.5 Th, offset isolation)
Ground truth is written to data/synthetic_mixed_truth.csv.
"""
import numpy as np
import pandas as pd
import pyopenms as oms

OUT = 'F:/OpenScience/audits/bio-proteomics-data-import/data/'
rng = np.random.default_rng(11)
exp = oms.MSExperiment()
truth = []
rt = 0.0
idx = 0


def add(ms_level, n_peaks, prec=None):
    global rt, idx
    s = oms.MSSpectrum()
    s.setMSLevel(ms_level)
    rt += 0.35
    s.setRT(rt)
    s.setNativeID(f'controllerType=0 controllerNumber=1 scan={idx + 1}')
    mz = np.sort(rng.uniform(150 if ms_level == 2 else 350, 1500, n_peaks))
    inten = rng.lognormal(10, 1.5, n_peaks)
    s.set_peaks((mz, inten))
    if prec is not None:
        p = oms.Precursor()
        p.setMZ(prec['mz'])
        p.setCharge(prec['z'])
        p.setIsolationWindowLowerOffset(prec['lo'])
        p.setIsolationWindowUpperOffset(prec['hi'])
        p.setActivationEnergy(28.0)
        s.setPrecursors([p])
    exp.addSpectrum(s)
    truth.append({'index': idx, 'ms_level': ms_level, 'n_peaks': n_peaks,
                  'prec_mz': None if prec is None else prec['mz'], 'charge': None if prec is None else prec['z'],
                  'lo': None if prec is None else prec['lo'], 'hi': None if prec is None else prec['hi']})
    idx += 1


for cyc in range(3):  # DDA
    add(1, 500)
    for k in range(3):
        add(2, int(rng.integers(40, 120)), {'mz': float(round(rng.uniform(400, 1200), 4)), 'z': int(rng.choice([2, 3])), 'lo': 0.8, 'hi': 0.8})
add(1, 500)  # DIA cycle
for centre in (412.5, 437.5, 462.5, 487.5):
    add(2, 300, {'mz': centre, 'z': 0, 'lo': 12.5, 'hi': 12.5})
add(2, 60, {'mz': 733.3812, 'z': 2, 'lo': 0.0, 'hi': 0.0})   # isolation window not written
add(2, 400, None)                                             # AIF scan: MS2 without precursor
add(2, 80, {'mz': 650.1234, 'z': 3, 'lo': 0.5, 'hi': 1.5})    # asymmetric window

oms.MzMLFile().store(OUT + 'synthetic_mixed.mzML', exp)
pd.DataFrame(truth).to_csv(OUT + 'synthetic_mixed_truth.csv', index=False)
print('wrote', exp.getNrSpectra(), 'spectra')
