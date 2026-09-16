"""Input 1 + 4 regression, run from the CURRENT SKILL.md text.

Rather than retyping, the two pyOpenMS blocks are extracted from the fork's
SKILL.md, the two filenames retargeted, and the ground truth scored exactly as
the pre-fix audit's rerun/in1_search.py did.
"""
import csv
import os
import subprocess
import sys

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SKDIR = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\peptide-identification"
D = "F:/OpenScience/audits/bio-proteomics-peptide-identification/data/"
W = r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4"

bs = blocks(rf"{SKDIR}\SKILL.md", "python")
B1 = [b for h, l, b in bs if h.startswith("Database Search with pyOpenMS")][0]
B2 = [b for h, l, b in bs if h.startswith("Annotate Target/Decoy")][0]


def run_skill(mzml, fasta):
    c1 = (B1.replace("'sample.mzML'", repr(mzml))
            .replace("'human_target_decoy.fasta'", repr(fasta))
            .replace("'search_results.idXML'", repr(rf"{W}\in1.idXML")))
    c2 = B2.replace("'human_target_decoy.fasta'", repr(fasta))
    ns = {}
    exec(compile(c1, "SKILL.md::search", "exec"), ns)
    n_search = ns["peptide_ids"].size()
    exec(compile(c2, "SKILL.md::fdr", "exec"), ns)
    return ns, n_search


def score(ns, truth_path):
    truth = {int(r["scan"]): r for r in csv.DictReader(open(truth_path, encoding="utf-8"))}
    tp = fp = 0
    qs = []
    pe = ns["peptide_ids"]
    for i in range(pe.size()):
        p = pe.at(i)
        if not p.getHits():
            continue
        scan = int(str(p.getMetaValue("spectrum_reference")).split("scan=")[-1])
        h = p.getHits()[0]
        qs.append(h.getScore())
        t = truth[scan]
        ok = (t["kind"] != "noise"
              and h.getSequence().toUnmodifiedString().replace("I", "L")
              == t["peptide"].replace("I", "L"))
        tp += ok
        fp += not ok
    return tp, fp, max(qs) if qs else None


ns, n = run_skill(D + "sample.mzML", D + "target_decoy.fasta")
keys = ["precursor:mass_tolerance", "fragment:mass_tolerance",
        "fragment:mass_tolerance_unit", "peptide:missed_cleavages",
        "modifications:fixed", "modifications:variable"]
print("params read back:", {k: ns["search"].getParameters().getValue(k) for k in keys})
tp, fp, qmax = score(ns, D + "truth.csv")
print(f"main: PSMs after search {n}; accepted {tp + fp}; correct {tp}; false {fp}; "
      f"true FDP {fp / max(1, tp + fp):.4f}; max q {qmax}")

TP = FP = 0
line = []
for rep in ["rep11", "rep22", "rep33", "rep44", "rep55", "rep66", "rep77", "rep88"]:
    nsr, _ = run_skill(f"{D}{rep}/sample.mzML", f"{D}{rep}/target_decoy.fasta")
    a, b, _ = score(nsr, f"{D}{rep}/truth.csv")
    TP += a
    FP += b
    line.append(f"{rep} {b / max(1, a + b):.4f}")
print(" | ".join(line))
print(f"pooled replicates: accepted {TP + FP}, false {FP}, FDP {FP / max(1, TP + FP):.4f}")

print("\n--- examples/fdr_filtering.py (shipped, unchanged) ---")
r = subprocess.run([sys.executable, "-B", os.path.join(SKDIR, "examples", "fdr_filtering.py")],
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip()[:500])
