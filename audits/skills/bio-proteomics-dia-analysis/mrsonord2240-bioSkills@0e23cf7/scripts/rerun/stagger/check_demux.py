'''Check what the Skill's msconvert filter chain produced: MS2 count and isolation-window widths before vs after demultiplexing.'''
import collections
from pyopenms import MSExperiment, MzMLFile

def summarise(path):
    e = MSExperiment(); MzMLFile().load(path, e)
    lv = collections.Counter(); w = collections.Counter(); centres = set()
    for s in e:
        lv[s.getMSLevel()] += 1
        if s.getMSLevel() == 2 and s.getPrecursors():
            p = s.getPrecursors()[0]
            w[round(p.getIsolationWindowLowerOffset() + p.getIsolationWindowUpperOffset(), 3)] += 1
            centres.add(round(p.getMZ(), 3))
    return lv, w, sorted(centres)

for lab, p in [('input  ', 'staggered_cycles.mzML'), ('demuxed', 'demux/staggered_cycles.mzML')]:
    lv, w, c = summarise(p)
    print(f'{lab}: MS levels {dict(lv)} | isolation widths(Th)->count {dict(w)} | distinct centres {len(c)} first {c[:4]}')
