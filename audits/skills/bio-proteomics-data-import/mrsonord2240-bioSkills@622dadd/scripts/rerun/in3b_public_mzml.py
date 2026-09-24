'''Data-import Input 3 (public-data run): SKILL.md block b01 executed verbatim on a REAL mzML -- PXD070049 (CC0) Orbitrap Astral
DIA Condition A REP1, converted with msconvert 3.0.26253 (peakPicking vendor msLevel=1-). The file stays outside the audits folder;
a temporary 'sample.mzML' path is created as a Windows hard link would not be portable, so the block text is run with the path swapped.'''
import io, contextlib, time, collections
import pandas as pd
P = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/mzml/dia/LFQ_Astral_DIA_5min_250pg_Condition_A_REP1.mzML'
src = open('F:/OpenScience/audits/bio-proteomics-data-import/rerun/blocks/b01_Loading_mzML_mzXML_with_pyOpenMS.py', encoding='utf-8').read()
assert src.count("'sample.mzML'") == 1
ns, buf = {}, io.StringIO(); t0 = time.time()
try:
    with contextlib.redirect_stdout(buf):
        exec(src.replace("'sample.mzML'", repr(P)), ns)
    print(f'Skill block completed in {time.time() - t0:.0f} s over {ns["exp"].getNrSpectra()} spectra')
except Exception as e:
    print('Skill block CRASHED:', type(e).__name__, e)
lines = buf.getvalue().strip().splitlines()
print('lines printed by the block (offsets not written):', len(lines), lines[:2])
exp = ns['exp']; lv = collections.Counter(); widths = collections.Counter(); noprec = 0; centers = []
for s in exp:
    lv[s.getMSLevel()] += 1
    if s.getMSLevel() == 2:
        pr = s.getPrecursors()
        if not pr: noprec += 1; continue
        w = pr[0].getIsolationWindowLowerOffset() + pr[0].getIsolationWindowUpperOffset(); widths[round(w, 2)] += 1; centers.append(round(pr[0].getMZ(), 2))
print('MS levels:', dict(lv), '| MS2 without precursor:', noprec)
print('isolation widths (Th): count', dict(widths.most_common(5)))
c = sorted(set(centers)); print('distinct window centres:', len(c), '| first/last:', c[:3], c[-3:])
lo = pd.Series([x - widths.most_common(1)[0][0] / 2 for x in c]); hi = pd.Series([x + widths.most_common(1)[0][0] / 2 for x in c])
print('adjacent windows overlap (would need demultiplexing):', bool((hi.iloc[:-1].values > lo.iloc[1:].values + 1e-6).any()))
