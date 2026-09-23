"""Phase-2 regressions for prior inputs 1--7; executed only from audit copies."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(r"F:\OpenScience\audits\bio-proteomics-peptide-identification")
DATA = ROOT / "data"
SKILL = ROOT / "run" / "skill"
PY = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\Scripts\python.exe")


def call(*args: str) -> str:
    run = subprocess.run([str(PY), *args], text=True, capture_output=True, check=True)
    print(run.stdout.strip())
    if run.stderr.strip():
        print("stderr:", run.stderr.strip())
    return run.stdout


def main() -> None:
    search = ROOT / "run" / "input1_search.idXML"
    fdr = ROOT / "run" / "input1_fdr.idXML"
    print("INPUT 1: pyOpenMS canonical search + FDR")
    call(str(SKILL / "scripts" / "pyopenms_search.py"), str(DATA / "sample.mzML"), str(DATA / "target_decoy.fasta"), str(search))
    out = call(str(SKILL / "scripts" / "pyopenms_fdr.py"), str(search), str(DATA / "target_decoy.fasta"), str(fdr))
    assert "311 target PSMs" in out and fdr.exists() and fdr.stat().st_size > 0

    print("INPUT 2: Comet-style ranked table")
    t2 = ROOT / "run" / "input2_1pct.tsv"
    out = call(str(SKILL / "scripts" / "table_fdr.py"), str(DATA / "comet_concat.txt"), "--scan", "scan", "--score", "xcorr", "--protein", "protein", "--out", str(t2))
    assert "2632 target PSMs" in out and t2.exists()

    print("INPUT 3: sparse and zero-decoy boundaries")
    for name, expected in [("pulldown_nodecoy.tsv", "no decoy PSMs recognised"), ("pulldown_topdecoy.tsv", "0 target PSMs")]:
        run = subprocess.run([str(PY), str(SKILL / "scripts" / "table_fdr.py"), str(DATA / name), "--scan", "scan", "--score", "xcorr", "--protein", "protein"], text=True, capture_output=True)
        text = run.stdout + run.stderr
        print(name, "exit", run.returncode, text.strip())
        assert expected in text, text

    print("INPUT 4: shipped PEP versus q-value example")
    out = call(str(SKILL / "examples" / "fdr_filtering.py"))
    assert "Target PSMs at q <= 0.01: 481" in out and "Target PSMs at PEP <= 0.01: 289" in out

    print("INPUT 5: separate target/decoy pi0 estimator")
    out = call(str(SKILL / "examples" / "separate_search_fdr.py"), str(DATA / "separate_target.tsv"), str(DATA / "separate_decoy.tsv"))
    assert "pi0-hat 0.611" in out and "kept at q <= 0.01: 2888" in out

    print("INPUT 6: lowercase and MaxQuant-style decoy tags")
    base = pd.read_csv(DATA / "comet_concat.txt", sep="\t")
    for tag in ("rev_", "REV__"):
        path = ROOT / "run" / f"input6_{tag.replace('_', 'u')}.tsv"
        x = base.copy()
        x["protein"] = x["protein"].str.replace("DECOY_", tag, regex=False)
        x.to_csv(path, sep="\t", index=False)
        out = call(str(SKILL / "scripts" / "table_fdr.py"), str(path), "--scan", "scan", "--score", "xcorr", "--protein", "protein")
        assert "3813 decoy hits" in out and "2632 target PSMs" in out

    print("INPUT 7: lower-is-better E-value rejection and orientation")
    raw = ROOT / "run" / "input7_raw.tsv"
    oriented = ROOT / "run" / "input7_oriented.tsv"
    x = base.copy()
    x["score"] = x["e-value"]
    x.to_csv(raw, sep="\t", index=False)
    raw_out = call(str(SKILL / "scripts" / "table_fdr.py"), str(raw), "--scan", "scan", "--score", "score", "--protein", "protein")
    assert "0 target PSMs" in raw_out
    x["score"] = -np.log10(x["e-value"].clip(lower=1e-300))
    x.to_csv(oriented, sep="\t", index=False)
    oriented_out = call(str(SKILL / "scripts" / "table_fdr.py"), str(oriented), "--scan", "scan", "--score", "score", "--protein", "protein")
    assert "2574 target PSMs" in oriented_out


if __name__ == "__main__":
    main()
