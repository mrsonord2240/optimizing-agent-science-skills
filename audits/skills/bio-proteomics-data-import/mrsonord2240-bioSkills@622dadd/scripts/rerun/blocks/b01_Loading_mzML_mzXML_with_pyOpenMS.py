from pyopenms import MSExperiment, MzMLFile

exp = MSExperiment()
MzMLFile().load('sample.mzML', exp)  # fills exp in place; returns None

for spectrum in exp:
    if spectrum.getMSLevel() == 1:
        mz, intensity = spectrum.get_peaks()  # tuple of two numpy arrays
    elif spectrum.getMSLevel() == 2:
        precs = spectrum.getPrecursors()  # a list; empty for all-ion (AIF/MSE) MS2 scans
        if not precs:
            continue  # record as no-precursor MS2 instead of indexing [0]
        precursor = precs[0]
        precursor_mz = precursor.getMZ()
        window = precursor.getIsolationWindowLowerOffset() + precursor.getIsolationWindowUpperOffset()
        if window == 0:
            print(f'{spectrum.getNativeID()}: isolation offsets not written (width unknown, not 0 Th)')
