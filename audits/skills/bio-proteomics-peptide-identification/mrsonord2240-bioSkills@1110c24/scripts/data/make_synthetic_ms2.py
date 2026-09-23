"""SYNTHETIC data for the bio-proteomics-peptide-identification audit (2026-09-11).

Builds
  target_decoy.fasta : 50 random target proteins (UniProt-like aa frequencies) + 50 reversed DECOY_ proteins
                       (protein-level reversal, as the Skill recommends).
  sample.mzML        : 600 MS2 spectra.
                       * 300 TRUE spectra: tryptic target peptides (7-25 aa, C carbamidomethylated),
                         b/y ions from pyOpenMS TheoreticalSpectrumGenerator, charge 2/3, 3 ppm m/z jitter,
                         only 15-70% of fragment peaks kept, 50-200 random noise peaks, lognormal intensities.
                       * 300 NOISE spectra: precursor m/z of a random peptide drawn 50/50 from the target and
                         decoy digests (so both kinds of candidates are in the window -> a fair null), fragments
                         entirely random (150-400 peaks). Any hit on a noise spectrum is false by construction.
  truth.csv          : native_id, kind (true/noise), peptide (for true spectra), charge.
Seeded (numpy default_rng(20260911)); re-running gives identical files.
"""
import csv
import os
import numpy as np
from pyopenms import (AASequence, FASTAEntry, FASTAFile, MSExperiment, MSSpectrum, MzMLFile, Peak1D,
                      Precursor, ProteaseDigestion, TheoreticalSpectrumGenerator)

OUT = os.environ.get('SYN_OUT', 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/')
rng = np.random.default_rng(int(os.environ.get('SYN_SEED', 20260911)))  # replicate runs: SYN_SEED / SYN_OUT
AA = 'ACDEFGHIKLMNPQRSTVWY'
FREQ = np.array([8.25, 1.37, 5.45, 6.75, 3.86, 7.07, 2.27, 5.96, 5.84, 9.66, 2.42, 4.06, 4.70, 3.93, 5.53,
                 6.56, 5.34, 6.87, 1.08, 2.92])
FREQ = FREQ / FREQ.sum()
PROTON = 1.007276

targets = []
for i in range(50):
    L = int(rng.integers(200, 600))
    seq = 'M' + ''.join(rng.choice(list(AA), size=L - 1, p=FREQ))
    targets.append((f'sp|SYN{i:03d}|SYN{i:03d}_HUMAN', seq))
entries = []
for acc, seq in targets:
    e = FASTAEntry(); e.identifier = acc; e.sequence = seq; e.description = 'synthetic target'; entries.append(e)
for acc, seq in targets:
    e = FASTAEntry(); e.identifier = 'DECOY_' + acc; e.sequence = seq[::-1]; e.description = 'reversed'; entries.append(e)
FASTAFile().store(OUT + 'target_decoy.fasta', entries)


def digest(seq):
    d = ProteaseDigestion(); d.setEnzyme('Trypsin'); d.setMissedCleavages(0)
    out = []
    d.digest(AASequence.fromString(seq), out, 7, 25)
    return [p.toString() for p in out]


tpep = sorted({p for _, s in targets for p in digest(s)})
dpep = sorted({p for _, s in targets for p in digest(s[::-1])} - set(tpep))
print('target peptides', len(tpep), 'decoy peptides', len(dpep))


def mod(p):
    return p.replace('C', 'C(Carbamidomethyl)')


tsg = TheoreticalSpectrumGenerator()
prm = tsg.getParameters()
prm.setValue('add_b_ions', 'true'); prm.setValue('add_y_ions', 'true'); prm.setValue('add_metainfo', 'false')
tsg.setParameters(prm)

exp = MSExperiment()
truth = []
true_peps = rng.choice(tpep, size=300, replace=False)
order = []
for p in true_peps:
    order.append(('true', p))
for _ in range(300):
    src = tpep if rng.random() < 0.5 else dpep
    order.append(('noise', src[int(rng.integers(len(src)))]))
rng.shuffle(order)

for k, (kind, p) in enumerate(order):
    seq = AASequence.fromString(mod(p))
    z = int(rng.choice([2, 3], p=[0.7, 0.3]))
    mz = (seq.getMonoWeight() + z * PROTON) / z
    mz *= 1 + rng.normal(0, 2e-6)
    peaks = []
    if kind == 'true':
        th = MSSpectrum()
        tsg.getSpectrum(th, seq, 1, min(z - 1, 2))
        mzs = np.array([pk.getMZ() for pk in th])
        keep = rng.random(len(mzs)) < rng.uniform(0.15, 0.7)
        for m in mzs[keep]:
            peaks.append((m * (1 + rng.normal(0, 3e-6)), rng.lognormal(10, 1)))
        n_noise = int(rng.integers(50, 200))
    else:
        n_noise = int(rng.integers(150, 400))
    hi = min(2000.0, seq.getMonoWeight() + 20)
    for m in rng.uniform(150, hi, n_noise):
        peaks.append((m, rng.lognormal(9, 1)))
    peaks.sort()
    s = MSSpectrum()
    s.setMSLevel(2)
    s.setRT(600.0 + 2.0 * k)
    s.setNativeID(f'controllerType=0 controllerNumber=1 scan={k + 1}')
    pc = Precursor(); pc.setMZ(mz); pc.setCharge(z); pc.setIntensity(1e6)
    s.setPrecursors([pc])
    s.set_peaks((np.array([a for a, _ in peaks]), np.array([b for _, b in peaks], dtype=np.float32)))
    exp.addSpectrum(s)
    truth.append({'scan': k + 1, 'kind': kind, 'peptide': p if kind == 'true' else '',
                  'noise_source_peptide': p if kind == 'noise' else '', 'charge': z})

MzMLFile().store(OUT + 'sample.mzML', exp)
with open(OUT + 'truth.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(truth[0]))
    w.writeheader(); w.writerows(truth)
print('spectra', exp.getNrSpectra(), 'true', sum(t['kind'] == 'true' for t in truth))
