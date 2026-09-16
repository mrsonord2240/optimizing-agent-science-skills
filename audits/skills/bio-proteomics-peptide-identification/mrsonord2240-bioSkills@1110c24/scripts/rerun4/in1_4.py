"""Input 1 + Input 4 regression: both pyOpenMS blocks VERBATIM from the fork's
SKILL.md on the synthetic mzML, then the shipped examples/fdr_filtering.py."""
import os
import re
import sys

import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SKDIR = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\peptide-identification"
DATA = r"F:\OpenScience\audits\bio-proteomics-peptide-identification\data"
W = r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4"

bs = blocks(rf"{SKDIR}\SKILL.md", "python")
search_block = [b for h, l, b in bs if h.startswith("Database Search with pyOpenMS")][0]
fdr_block = [b for h, l, b in bs if h.startswith("Annotate Target/Decoy")][0]


def retarget(code, mzml, fasta, out):
    code = code.replace("'sample.mzML'", repr(mzml))
    code = code.replace("'human_target_decoy.fasta'", repr(fasta))
    code = code.replace("'search_results.idXML'", repr(out))
    return code


def run(mzml, fasta, tag):
    ns = {}
    c1 = retarget(search_block, mzml, fasta, rf"{W}\{tag}.idXML")
    exec(compile(c1, "<SKILL.md search block>", "exec"), ns)
    n_psm = len(ns["peptide_ids"])
    c2 = retarget(fdr_block, mzml, fasta, "")
    exec(compile(c2, "<SKILL.md fdr block>", "exec"), ns)
    pep = ns["peptide_ids"]
    truth = pd.read_csv(rf"{DATA}\truth.csv") if os.path.exists(rf"{DATA}\truth.csv") else None
    accepted, correct, maxq = 0, 0, 0.0
    tmap = {}
    if truth is not None:
        for _, r in truth.iterrows():
            tmap[str(r.iloc[0])] = str(r.iloc[1])
    for pid in pep:
        for hit in pid.getHits():
            accepted += 1
            maxq = max(maxq, hit.getScore())
            seq = hit.getSequence().toUnmodifiedString()
            key = str(pid.getMetaValue("spectrum_reference") or "")
            sc = key.split("=")[-1] if key else ""
            if tmap.get(sc) == seq:
                correct += 1
    return n_psm, accepted, correct, maxq


n, acc, cor, mq = run(rf"{DATA}\sample.mzML", rf"{DATA}\target_decoy.fasta", "in1_main")
print(f"main: PSMs after search {n}; accepted at q<=0.01 {acc}; max q {mq:.4f}")
print(f"      truth-matched among accepted: {cor} (FDP {1 - cor / acc:.4f})" if acc else "")

# Common Errors rows, reproduced
from pyopenms import FalseDiscoveryRate, PeptideIdentification, PeptideIdentificationList  # noqa: E402
from pyopenms import SimpleSearchEngineAlgorithm  # noqa: E402

try:
    SimpleSearchEngineAlgorithm().search(rf"{DATA}\sample.mzML",
                                         rf"{DATA}\target_decoy.fasta", [], [])
except TypeError as e:
    print("plain [] for peptide ids ->", type(e).__name__, str(e)[:90])

try:
    pl = PeptideIdentificationList()
    pl.push_back(PeptideIdentification())
    FalseDiscoveryRate().apply(pl)
except RuntimeError as e:
    print("FDR on unannotated hits ->", type(e).__name__, str(e)[:80])

print("\n--- examples/fdr_filtering.py (shipped, unchanged) ---")
os.system(f'"{sys.executable}" -B "{SKDIR}\\examples\\fdr_filtering.py"')
