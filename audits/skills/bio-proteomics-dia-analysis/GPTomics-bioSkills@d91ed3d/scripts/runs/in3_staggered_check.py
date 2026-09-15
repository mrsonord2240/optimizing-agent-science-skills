"""Input 3 (Edge) - staggered-window DIA. The Skill gives no code for detecting the window scheme (usage-guide step 1 says
the agent should identify it), so this is agent-written Mode A code. It builds two SYNTHETIC mzML files with pyOpenMS
(one staggered 2 x 8 Th overlap-by-half scheme, one plain 8 Th scheme), then reads the MS2 isolation windows back and
decides whether demultiplexing applies. msconvert / DIA-NN are NOT run (no build here).
"""
import os
import numpy as np
import pyopenms as oms

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def make_mzml(path, staggered):
    exp = oms.MSExperiment()
    rt = 0.0
    lo, hi, width = 400.0, 480.0, 8.0
    for cycle in range(6):
        ms1 = oms.MSSpectrum(); ms1.setMSLevel(1); ms1.setRT(rt); rt += 0.05
        ms1.set_peaks((np.array([450.0, 451.0]), np.array([1e5, 5e4], dtype=np.float32)))
        exp.addSpectrum(ms1)
        shift = width / 2.0 if (staggered and cycle % 2 == 1) else 0.0  # odd cycles offset by half a window
        starts = np.arange(lo - shift, hi, width)
        for s in starts:
            ms2 = oms.MSSpectrum(); ms2.setMSLevel(2); ms2.setRT(rt); rt += 0.01
            p = oms.Precursor(); p.setMZ(s + width / 2.0)
            p.setIsolationWindowLowerOffset(width / 2.0); p.setIsolationWindowUpperOffset(width / 2.0)
            ms2.setPrecursors([p])
            ms2.set_peaks((np.array([300.0, 500.0, 700.0]), np.array([1e3, 2e3, 5e2], dtype=np.float32)))
            exp.addSpectrum(ms2)
    oms.MzMLFile().store(path, exp)


def window_scheme(path):
    exp = oms.MSExperiment(); oms.MzMLFile().load(path, exp)
    wins = []
    for sp in exp:
        if sp.getMSLevel() == 2:
            p = sp.getPrecursors()[0]
            wins.append((round(p.getMZ() - p.getIsolationWindowLowerOffset(), 4),
                         round(p.getMZ() + p.getIsolationWindowUpperOffset(), 4)))
    uniq = sorted(set(wins))
    widths = sorted({round(b - a, 4) for a, b in uniq})
    # partial overlap between distinct windows = staggered/overlapping design
    partial = sum(1 for i, (a, b) in enumerate(uniq) for (c, d) in uniq[i + 1:] if c < b and d > a and (a, b) != (c, d))
    return len(uniq), widths, partial


for name, stag in (('synthetic_staggered_8Th.mzML', True), ('synthetic_fixed_8Th.mzML', False)):
    path = os.path.join(DATA, name)
    make_mzml(path, stag)
    n, widths, partial = window_scheme(path)
    verdict = ('OVERLAPPING windows -> staggered design: demultiplex at conversion if converting '
               '(or let DIA-NN read .raw natively)') if partial else 'non-overlapping windows -> no demultiplexing'
    print(f'{name}: {n} distinct MS2 windows, physical width(s) {widths} Th, partially-overlapping pairs {partial} -> {verdict}')
