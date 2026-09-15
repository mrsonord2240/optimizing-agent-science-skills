"""Input 3 (Edge) - mzML: MS1 peak counts + MS2 precursor m/z, charge and isolation-window width.
Part A: the Skill's 'Loading mzML/mzXML with pyOpenMS' loop VERBATIM (file name changed only), wrapped in try/except
        so the failure is captured instead of aborting the log.
Part B: what Claude-with-this-Skill writes for the user: the same calls, collected into a table (still no guard).
Part C: AUDITOR comparison with the generator truth + the guarded loop the Skill should give.
Data: SYNTHETIC data/synthetic_mixed.mzML (make_mzml.py).
"""
import traceback
import pandas as pd
import pyopenms
from pyopenms import MSExperiment, MzMLFile

PATH = 'F:/OpenScience/audits/bio-proteomics-data-import/data/synthetic_mixed.mzML'
print('pyopenms', pyopenms.__version__)

# ---------------- Part A: Skill block verbatim ----------------
exp = MSExperiment()
ret = MzMLFile().load(PATH, exp)  # fills exp in place; returns None
print('load() returned:', ret, '| spectra:', exp.getNrSpectra())
try:
    n = 0
    for spectrum in exp:
        if spectrum.getMSLevel() == 1:
            mz, intensity = spectrum.get_peaks()  # tuple of two numpy arrays
        elif spectrum.getMSLevel() == 2:
            precursor = spectrum.getPrecursors()[0]  # getPrecursors returns a list
            precursor_mz = precursor.getMZ()
            window = precursor.getIsolationWindowLowerOffset() + precursor.getIsolationWindowUpperOffset()
        n += 1
    print('Skill loop finished over', n, 'spectra')
except Exception:
    print(f'Skill loop CRASHED at spectrum index {n}:')
    traceback.print_exc(limit=1)
print('types from get_peaks():', type(exp[0].get_peaks()).__name__, [type(a).__name__ for a in exp[0].get_peaks()])
print('type of getPrecursors():', type(exp[1].getPrecursors()).__name__)

# ---------------- Part B: user-facing table, Skill calls only ----------------
rows = []
try:
    for i, spectrum in enumerate(exp):
        lvl = spectrum.getMSLevel()
        if lvl == 1:
            mz, intensity = spectrum.get_peaks()
            rows.append({'i': i, 'ms': 1, 'rt_s': round(spectrum.getRT(), 2), 'n_peaks': len(mz), 'tic': float(intensity.sum())})
        elif lvl == 2:
            precursor = spectrum.getPrecursors()[0]
            rows.append({'i': i, 'ms': 2, 'rt_s': round(spectrum.getRT(), 2), 'n_peaks': spectrum.size(),
                         'prec_mz': precursor.getMZ(), 'z': precursor.getCharge(),
                         'win_width': precursor.getIsolationWindowLowerOffset() + precursor.getIsolationWindowUpperOffset()})
except Exception as e:
    print(f'Part B stopped at spectrum {i}: {type(e).__name__}: {e}  ({len(rows)} rows collected)')

# ---------------- Part C: guarded version + truth check ----------------
truth = pd.read_csv('F:/OpenScience/audits/bio-proteomics-data-import/data/synthetic_mixed_truth.csv')
out = []
for i, s in enumerate(exp):
    r = {'i': i, 'ms': s.getMSLevel(), 'n_peaks': s.size()}
    precs = s.getPrecursors()
    if s.getMSLevel() >= 2:
        if not precs:
            r.update(prec_mz=None, z=None, lo=None, hi=None, flag='no precursor (AIF/MSE-style)')
        else:
            p = precs[0]
            lo, hi = p.getIsolationWindowLowerOffset(), p.getIsolationWindowUpperOffset()
            r.update(prec_mz=round(p.getMZ(), 4), z=p.getCharge(), lo=lo, hi=hi,
                     win_lo_mz=round(p.getMZ() - lo, 4), win_hi_mz=round(p.getMZ() + hi, 4),
                     flag='width 0: offsets missing' if lo + hi == 0 else ('DIA-wide' if lo + hi > 4 else ('asymmetric' if lo != hi else '')))
    out.append(r)
df = pd.DataFrame(out)
print(df[df.ms == 2].to_string(index=False))
m = df.merge(truth, left_on='i', right_on='index', suffixes=('', '_t'))
ok_peaks = (m.n_peaks == m.n_peaks_t).all()
ms2 = m[(m.ms == 2) & m.prec_mz.notna()]
print('[AUDIT] peak counts match truth:', bool(ok_peaks),
      '| precursor m/z match:', bool(((ms2.prec_mz - ms2.prec_mz_t).abs() < 1e-3).all()),
      '| offsets match:', bool(((ms2.lo == ms2.lo_t) & (ms2.hi == ms2.hi_t)).all()))
print('[AUDIT] MS1 spectra:', int((df.ms == 1).sum()), '| MS2:', int((df.ms == 2).sum()),
      '| MS2 with no precursor:', int(df.flag.eq('no precursor (AIF/MSE-style)').sum()))
