'''DIA Input 3 (NEW run, strengthens the pre-fix Edge input): build a SYNTHETIC staggered/overlapping-window mzML with enough
complete cycles for ProteoWizard's demultiplexer to identify the scheme (the pre-fix synthetic file held 5 spectra, so msconvert
aborted with "Too few spectra to determine the number of precursor windows" before the Skill's filter chain could be judged).

Scheme: 12 cycles x (1 MS1 + 20 MS2). Physical window 8 Th, centres stepping 8 Th from 400; odd cycles offset by +4 Th, so
consecutive cycles interleave and demultiplexing should recover 4-Th effective windows (Amodei 2019). Profile-like Gaussian peaks
so that "peakPicking vendor msLevel=1-" has something to centroid. SYNTHETIC DATA -- not a real acquisition.'''
import numpy as np
from pyopenms import MSExperiment, MSSpectrum, MzMLFile, Precursor, InstrumentSettings, ScanWindow

rng = np.random.default_rng(20260915)
N_CYCLES, N_WIN, WIDTH, START = 12, 20, 8.0, 400.0
exp = MSExperiment()
rt = 0.0

def profile_peaks(centres, heights, sigma=0.01, n=7):
    mz, inten = [], []
    for c, h in zip(centres, heights):
        off = np.linspace(-3 * sigma, 3 * sigma, n)
        mz.extend(c + off)
        inten.extend(h * np.exp(-0.5 * (off / sigma) ** 2))
    o = np.argsort(mz)
    return np.array(mz)[o], np.array(inten)[o]

for cyc in range(N_CYCLES):
    offset = (WIDTH / 2) if cyc % 2 else 0.0
    s = MSSpectrum()
    s.setMSLevel(1)
    s.setRT(rt)
    s.setNativeID(f'controllerType=0 controllerNumber=1 scan={len(exp.getSpectra()) + 1}')
    isettings = InstrumentSettings()
    w = ScanWindow(); w.begin, w.end = START, START + N_WIN * WIDTH
    isettings.setScanWindows([w])
    s.setInstrumentSettings(isettings)
    c = rng.uniform(START, START + N_WIN * WIDTH, 40)
    s.set_peaks(profile_peaks(c, rng.uniform(1e4, 1e6, 40)))
    exp.addSpectrum(s)
    rt += 0.3
    for k in range(N_WIN):
        lo = START + k * WIDTH + offset
        s2 = MSSpectrum()
        s2.setMSLevel(2)
        s2.setRT(rt)
        s2.setNativeID(f'controllerType=0 controllerNumber=1 scan={len(exp.getSpectra()) + 1}')
        p = Precursor()
        p.setMZ(lo + WIDTH / 2)
        p.setIsolationWindowLowerOffset(WIDTH / 2)
        p.setIsolationWindowUpperOffset(WIDTH / 2)
        s2.setPrecursors([p])
        isettings2 = InstrumentSettings()
        w2 = ScanWindow(); w2.begin, w2.end = 150.0, 1500.0
        isettings2.setScanWindows([w2])
        s2.setInstrumentSettings(isettings2)
        cf = rng.uniform(200, 1200, 25)
        s2.set_peaks(profile_peaks(cf, rng.uniform(1e3, 1e5, 25)))
        exp.addSpectrum(s2)
        rt += 0.012

MzMLFile().store('staggered_cycles.mzML', exp)
print('SYNTHETIC staggered mzML written: staggered_cycles.mzML | spectra', exp.getNrSpectra(),
      '| cycles', N_CYCLES, '| windows/cycle', N_WIN, '| physical width', WIDTH, 'Th | stagger offset', WIDTH / 2, 'Th')
