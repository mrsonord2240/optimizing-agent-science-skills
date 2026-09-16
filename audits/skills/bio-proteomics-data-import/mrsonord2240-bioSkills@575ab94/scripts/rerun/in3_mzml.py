'''Data-import Input 3 (regression, edge): mixed mzML (DDA, DIA windows, offsets-not-written scan, AIF scan without precursor).
SKILL.md block b01 executed verbatim (cwd has sample.mzML = data/synthetic_mixed.mzML, SYNTHETIC), then the agent's table.'''
import os, io, contextlib, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work')
ns, buf = {}, io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        with open('../blocks/b01_Loading_mzML_mzXML_with_pyOpenMS.py', encoding='utf-8') as fh:
            exec(fh.read(), ns)
    print('Skill loop: completed over', ns['exp'].getNrSpectra(), 'spectra')
except Exception as e:
    print('Skill loop CRASHED:', type(e).__name__, e)
print('printed by the block:', buf.getvalue().strip())
rows = []
for i, s in enumerate(ns['exp']):
    precs = s.getPrecursors()
    if s.getMSLevel() == 1:
        rows.append({'i': i, 'ms': 1, 'n_peaks': len(s.get_peaks()[0])}); continue
    if not precs:
        rows.append({'i': i, 'ms': 2, 'n_peaks': len(s.get_peaks()[0]), 'flag': 'no precursor (all-ion)'}); continue
    p = precs[0]; lo, hi = p.getIsolationWindowLowerOffset(), p.getIsolationWindowUpperOffset()
    rows.append({'i': i, 'ms': 2, 'n_peaks': len(s.get_peaks()[0]), 'prec_mz': round(p.getMZ(), 4), 'z': p.getCharge(), 'lo': lo, 'hi': hi,
                 'flag': 'offsets not written' if lo + hi == 0 else ''})
t = pd.DataFrame(rows)
print(t.tail(6).to_string(index=False))
truth = pd.read_csv('../../data/synthetic_mixed_truth.csv')
print('truth columns:', list(truth.columns))
print(truth.tail(4).to_string(index=False))
