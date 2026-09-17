"""Input 3 - Variant B: multi-dose consistency using the SKILL.md-documented
`dose_consistent_hits()` function verbatim (copy-pasted below exactly as it appears in
SKILL.md's "Drug-Dose and Time-Course Designs" section). Regression of pre-fix Input 3,
now testing the *runnable* code path instead of hand-written substitute logic.
"""
import subprocess, sys
import pandas as pd

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work\threedose_counts.txt"
WORK = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"

dose_files = {}
for dose, samples in [("low", "LowDose_r1,LowDose_r2,LowDose_r3"),
                       ("mid", "MidDose_r1,MidDose_r2,MidDose_r3"),
                       ("high", "Drug_r1,Drug_r2,Drug_r3")]:
    out = f"{WORK}\\input3_{dose}.txt"
    r = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", out,
                         "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", samples, "-p", "5"],
                        capture_output=True, text=True)
    print(dose, "returncode:", r.returncode)
    dose_files[dose] = out

# === Exact copy of SKILL.md's dose_consistent_hits() ===
def dose_consistent_hits(dose_files, top_dose, fdr=0.05, direction='synth'):
    """dose_files: {'low': 'drugz_low.txt', 'mid': ..., 'high': ...}; top_dose: key of the highest dose.

    A hit is dose-consistent if normZ has the same sign at every dose and passes FDR at the top dose.
    """
    frames = {d: pd.read_csv(f, sep='\t').set_index('GENE') for d, f in dose_files.items()}
    normz = pd.DataFrame({d: f['normZ'] for d, f in frames.items()}).dropna()
    sign_ok = (normz.gt(0).all(axis=1)) | (normz.lt(0).all(axis=1))
    top = frames[top_dose]
    passes = top['fdr_%s' % direction] < fdr
    hits = normz[sign_ok & passes.reindex(normz.index).fillna(False)].copy()
    hits['normZ_top_dose'] = top['normZ'].reindex(hits.index)
    hits['monotonic'] = (normz.abs().diff(axis=1).iloc[:, 1:] >= 0).all(axis=1)  # |normZ| grows with dose
    return hits.sort_values('normZ_top_dose')

hits = dose_consistent_hits(dose_files, top_dose='high', direction='synth')
print("\ndose-consistent sensitizer hits (n=%d):" % len(hits))
print(hits.to_string())

planted_sensitizers = set("CCDC89,CER1,CFL2,GALNT11,IL18R1,OSTM1".split(","))
found = set(hits.index)
print("\nplanted sensitizers recovered:", len(found & planted_sensitizers), "/", len(planted_sensitizers))
print("false positives (hit but not planted):", sorted(found - planted_sensitizers))
print("missed planted:", sorted(planted_sensitizers - found))
