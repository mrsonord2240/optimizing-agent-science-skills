"""Phase 2 dynamic checks 1-6 for bio-crispr-screens-prime-editing-screens.

Runs only the audit copy of shipped code.  It uses the provisioned PRIDICT2
runtime and records concise, assertion-bearing evidence in phase2_summary.json.
"""
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skill"
PRIDICT_REPO = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\PRIDICT2")
PRIDICT_PY = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\pridict2-venv\Scripts\python.exe")
CLI = PRIDICT_REPO / "pridict2_pegRNA_design.py"
RESULTS: dict[str, dict] = {}


def run(label: str, cmd: list[str], cwd: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
    cwd.mkdir(parents=True, exist_ok=True)
    cp = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, encoding="utf-8", errors="replace")
    (cwd / f"{label}.stdout.txt").write_text(cp.stdout, encoding="utf-8")
    (cwd / f"{label}.stderr.txt").write_text(cp.stderr, encoding="utf-8")
    if cp.returncode != expected:
        raise RuntimeError(f"{label}: expected rc={expected}, got {cp.returncode}\n{cp.stdout[-2000:]}\n{cp.stderr[-2000:]}")
    return cp


def record(i: int, status: str, assertions: list[tuple[str, bool, str]], note: str) -> None:
    RESULTS[str(i)] = {
        "status": status,
        "executed": True,
        "execution_note": note,
        "assertions": [{"text": text, "result": "PASS" if ok else "FAIL", "note": why} for text, ok, why in assertions],
    }


def main() -> None:
    # Input 1: PRIDICT2 canonical single-mode sequence from the upstream README.
    p1 = ROOT / "input1_single"
    seq = "GCCTGGAGGTGTCTGGGTCCCTCCCCCACCCGACTACTTCACTCTCTGTCCTCTCTGCCCAGGAGCCCAGGATGTGCGAGTTCAAGTGGCTACGGCCGA(G/C)GTGCGAGGCCAGCTCGGGGGCACCGTGGAGCTGCCGTGCCACCTGCTGCCACCTGTTCCTGGACTGTACATCTCCCTGGTGACCTGGCAGCGCCCAGATGCACCTGCGAACCACCAGAATGTGGCCGC"
    (p1 / "predictions").mkdir(parents=True, exist_ok=True)
    cp = run("pridict_single", [str(PRIDICT_PY), str(CLI), "single", "--sequence-name", "phase2_single", "--sequence", seq, "--output-dir", "predictions", "--use_5folds"], p1)
    outputs = list((p1 / "predictions").glob("phase2_single_pegRNA_Pridict_full.csv"))
    assert len(outputs) == 1, outputs
    df1 = pd.read_csv(outputs[0])
    score_cols = [c for c in df1.columns if c.startswith("PRIDICT2_0_editing_Score")]
    assert len(df1) > 0 and score_cols and df1[score_cols].notna().all().all()
    record(1, "COMPLETED", [
        ("Single-mode invocation produces a non-empty per-pegRNA CSV", len(df1) > 0, f"{len(df1)} rows"),
        ("Real PRIDICT2 score columns are present and non-NaN", bool(score_cols and df1[score_cols].notna().all().all()), str(score_cols)),
        ("The documented five-fold option completes", "Running in single mode" in cp.stdout, "mode banner observed"),
    ], "Fresh upstream-README single-mode input; 5-fold run written under run/phase2/input1_single.")

    # Input 2: Skill's batch recipe, from an empty directory, using two valid diverse edits.
    p2 = ROOT / "input2_batch"
    (p2 / "input").mkdir(parents=True, exist_ok=True)
    (p2 / "predictions").mkdir(parents=True, exist_ok=True)
    template = pd.read_csv(PRIDICT_REPO / "input" / "batch_template.csv")
    template.iloc[[0, 2]].to_csv(p2 / "input" / "variants.csv", index=False)
    cp2 = run("pridict_batch", [str(PRIDICT_PY), str(CLI), "batch", "--input-fname", "variants.csv", "--output-dir", "predictions", "--cores", "3", "--summarize", "K562"], p2)
    summaries = list((p2 / "predictions").glob("*_summary_K562_batch_summary.csv"))
    assert len(summaries) == 1, summaries
    df2 = pd.read_csv(summaries[0])
    required = {"sequence_name", "PRIDICT2_0_editing_Score_deep_K562", "PBSrevcomp", "RTrevcomp", "pegRNA", "Target-Strand", "Editing_Position"}
    assert len(df2) >= 2 and required.issubset(df2.columns) and df2["PRIDICT2_0_editing_Score_deep_K562"].notna().all()
    record(2, "COMPLETED", [
        ("Literal documented input/ and fresh predictions/ batch recipe completes", "Batch processing completed" in cp2.stdout, "completion banner observed"),
        ("Summary contains real prediction rows", len(df2) >= 2, f"{len(df2)} rows"),
        ("Documented real output columns are present", required.issubset(df2.columns), f"missing={sorted(required-set(df2.columns))}"),
        ("K562 scores are numeric and non-NaN", bool(df2["PRIDICT2_0_editing_Score_deep_K562"].notna().all()), "all rows populated"),
    ], "Fresh two-edit batch run from an initially empty audit directory; exact --cores 3 and --summarize K562 recipe executed.")

    # Input 3: an intentional second summarize into the same directory must fail clearly.
    cp3 = run("pridict_second_run", [str(PRIDICT_PY), str(CLI), "batch", "--input-fname", "variants.csv", "--output-dir", "predictions", "--cores", "3", "--summarize", "K562"], p2, expected=1)
    joined = cp3.stdout + cp3.stderr
    expected_msg = "Output directory is not empty"
    assert expected_msg in joined
    record(3, "COMPLETED", [
        ("A second --summarize into an occupied CSV directory fails", cp3.returncode != 0, f"rc={cp3.returncode}"),
        ("Failure gives the documented remediation signal", expected_msg in joined, expected_msg),
        ("The first-run summary remains parseable", pd.read_csv(summaries[0]).shape == df2.shape, str(df2.shape)),
    ], "Regression of the documented no-CSV-in-output-dir precondition; deliberately expected failure was observed.")

    # Input 4: shipped design example on one constructible and one no-PAM variant.
    p4 = ROOT / "input4_example"
    p4.mkdir(parents=True, exist_ok=True)
    fixture = pd.DataFrame([
        {"variant_id": "constructible", "chrom": "chr1", "pos": 118, "ref": "C", "alt": "T", "context": "CGACGTTGACCTGGAACGTTCATGGCGATCCGTAAGCTTGGCCAATGGCCTTAAGGCCTT"},
        {"variant_id": "no_pam", "chrom": "chr3", "pos": 30, "ref": "G", "alt": "A", "context": "CAACATGTAGAATGCTTCTGTATTAGTGATGCATCGTACATGTAACGTTCACTTTAGCTT"},
    ])
    fixture.to_csv(p4 / "intended_variants.csv", index=False)
    cp4 = run("design_example", [sys.executable, str(SKILL / "examples" / "design_pegrna_pridict2.py")], p4)
    lib = pd.read_csv(p4 / "peg_library_filtered.csv")
    assert "constructible" in set(lib.variant_id) and "no_pam" not in set(lib.variant_id)
    assert all(lib.extension_seq == lib.rtt + lib.pbs)
    record(4, "COMPLETED", [
        ("A constructible variant yields a filtered library entry", "constructible" in set(lib.variant_id), f"rows={len(lib)}"),
        ("No-PAM variants are skipped rather than crashing the batch", "no_pam" in cp4.stdout.lower(), cp4.stdout.splitlines()[0]),
        ("Every emitted extension is RTT then PBS", bool(all(lib.extension_seq == lib.rtt + lib.pbs)), "rowwise equality"),
    ], "Copied shipped example ran on a new two-variant fixture, including a no-PAM edge case.")

    # Input 5: shipped summary filtering script, with real output then explicit empty-summary failure.
    p5 = ROOT / "input5_filter"
    p5.mkdir(parents=True, exist_ok=True)
    shutil.copy2(summaries[0], p5 / "summary.csv")
    cp5 = run("filter_real", [sys.executable, str(SKILL / "scripts" / "filter_pridict2_summary.py"), "summary.csv", "--threshold", "0", "--top", "1", "--out", "filtered.csv"], p5)
    fdf = pd.read_csv(p5 / "filtered.csv")
    assert len(fdf) == 2 and set(fdf.sequence_name) == set(df2.sequence_name)
    (p5 / "empty.csv").write_text('""\n', encoding="utf-8")
    cp5e = run("filter_empty", [sys.executable, str(SKILL / "scripts" / "filter_pridict2_summary.py"), "empty.csv", "--out", "never.csv"], p5, expected=1)
    record(5, "COMPLETED", [
        ("Filter script retains top one per sequence on a real summary", len(fdf) == 2, f"rows={len(fdf)}"),
        ("Output has the two input sequence names", set(fdf.sequence_name) == set(df2.sequence_name), sorted(fdf.sequence_name)),
        ("A literal empty PRIDICT2 summary exits nonzero with guidance", cp5e.returncode == 1 and "Failure Modes" in (cp5e.stdout + cp5e.stderr), "clear guard observed"),
    ], "Copied shipped filtering script checked against fresh real PRIDICT2 summary and a literal empty-summary sentinel.")

    # Input 6: PE/BE concordance script against planted truth.
    p6 = ROOT / "input6_crossvalidate"
    p6.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"variant_id":["v1","v2","v3","v4","be_only"],"be_fdr":[.01,.2,.01,.04,.01],"be_lfc":[1.5,1.5,1.5,-2.0,.9]}).to_csv(p6 / "be.tsv", sep="\t", index=False)
    pd.DataFrame({"variant_id":["v1","v2","v3","v4","pe_only"],"pe_fdr":[.01,.01,.01,.03,.01],"pe_lfc":[1.2,1.2,-1.2,-.5,.7]}).to_csv(p6 / "pe.tsv", sep="\t", index=False)
    run("crossvalidate", [sys.executable, str(SKILL / "scripts" / "crossvalidate_pe_be.py"), "be.tsv", "pe.tsv", "--fdr", "0.05", "--out", "concordance.tsv"], p6)
    cdf = pd.read_csv(p6 / "concordance.tsv", sep="\t")
    highs = set(cdf.loc[cdf.high_confidence, "variant_id"])
    assert highs == {"v1", "v4"}
    record(6, "COMPLETED", [
        ("Only shared variants are inner-joined", set(cdf.variant_id) == {"v1", "v2", "v3", "v4"}, f"rows={len(cdf)}"),
        ("Exactly the two planted same-sign FDR-passing variants are high confidence", highs == {"v1", "v4"}, sorted(highs)),
        ("Discordant sign and failed FDR are excluded", not bool(cdf.loc[cdf.variant_id == "v3", "high_confidence"].iloc[0]) and not bool(cdf.loc[cdf.variant_id == "v2", "high_confidence"].iloc[0]), "v2/v3 false"),
    ], "Copied shipped cross-validation script executed on a newly planted four-shared-variant fixture.")

    (ROOT / "phase2_summary.json").write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")
    print(json.dumps(RESULTS, indent=2))


if __name__ == "__main__":
    main()
