#!/usr/bin/env python
"""Fresh Phase 2 dynamic audit for bio-crispr-screens-hit-calling.

Runs against worktree tip 51cfb2078674ff6e8cb4412b9ae229f173a0b19d only.
Inputs 1-9 replay the prior audit's cases; 10-11 are new independent fixtures.
Usage: F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe phase2_dynamic.py
"""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import sys
from pathlib import Path
import importlib.util

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "phase2_data"
WORK = ROOT / "phase2_work"
OUT = ROOT / "phase2_outputs"
SOURCE = Path(r"F:\OpenScience\wt\crispr-screens-hit-calling\crispr-screens\hit-calling")
PY = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe")
WORK.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

def stage(*names: str) -> None:
    for name in names:
        shutil.copy2(DATA / name, WORK / name)

def run(label: str, argv: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ | {"PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(argv, cwd=WORK, text=True, capture_output=True, env=env)
    log = f"$ {' '.join(argv)}\nexit={result.returncode}\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    (OUT / f"{label}.log").write_text(log, encoding="utf-8")
    print(f"{label}: exit={result.returncode}")
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    assert result.returncode == 0, log
    return result

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

stage("mageck_hap1.gene_summary.txt", "mageck_hap1.sgrna_summary.txt", "bayes_factor.txt", "bayes_factor_rep2.txt", "drugz_drug_output.txt", "CEGv2.txt", "NEGv1.txt")

# Input 1: canonical two-method consensus, exact shipped example.
shutil.copy2(DATA / "mageck_hap1.gene_summary.txt", WORK / "mageck.gene_summary.txt")
shutil.copy2(DATA / "bayes_factor.txt", WORK / "bagel_bf.txt")
r1 = run("input01", [str(PY), str(SOURCE / "examples" / "consensus_hits.py")])
cons = pd.read_csv(WORK / "consensus_hits.csv")
ceg = set(pd.read_csv(DATA / "CEGv2.txt", sep="\t")["GENE"])
neg = set(pd.read_csv(DATA / "NEGv1.txt", sep="\t")["GENE"])
assert len(cons) == 844 and len(set(cons.gene) & neg) == 0
print(f"INPUT1: consensus={len(cons)} CEGv2_overlap={len(set(cons.gene)&ceg)} NEGv1_overlap=0")

# Input 2: decision tree answer, tested against the exact source text.
skill = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
answer2 = ("Chronos is primary: this is a multi-cell-line cancer dependency panel, so it models copy-number bias and screen quality jointly. "
           "Run MAGeCK MLE per line as a secondary analysis, retaining a cell-line indicator before downstream meta-analysis. "
           "Do not use JACKS as the primary analysis because the tree reserves it for multi-screen joint analyses with the same library.")
assert "Multi-cell-line panel (cancer dependency)" in skill and "Chronos" in skill and "MAGeCK MLE per line" in skill
(OUT / "input02_response.txt").write_text(answer2 + "\n", encoding="utf-8")
print("INPUT2: Chronos primary; MLE per-line secondary; JACKS excluded")

# Input 3: exact shipped second-best CLI on real data.
r3 = run("input03", [str(PY), str(SOURCE / "scripts" / "second_best_lfc.py"), "mageck_hap1.sgrna_summary.txt", "-o", "input03_second_best.tsv"])
second = pd.read_csv(WORK / "input03_second_best.tsv", sep="\t")
assert len(second) == 18056 and int(second.single_guide.sum()) == 231
assert second.loc[second.single_guide, "second_best_lfc"].isna().all()
print("INPUT3: 18056 genes; 231 single-guide genes all NaN and flagged")

# Input 4: sign-corrected score correlation and its instructions.
mageck = pd.read_csv(DATA / "mageck_hap1.gene_summary.txt", sep="\t")[["id", "neg|score"]].rename(columns={"id": "gene"})
bagel = pd.read_csv(DATA / "bayes_factor.txt", sep="\t").rename(columns={"GENE": "gene"})
joined = mageck.merge(bagel, on="gene")
naive = spearmanr(joined["neg|score"], joined["BF"]).statistic
corrected = spearmanr(-joined["neg|score"], joined["BF"]).statistic
assert len(joined) == 18053 and round(naive, 3) == -0.806 and round(corrected, 3) == 0.806
assert "Correlating MAGeCK and BAGEL2 Scores" in skill and "sign-correct" in skill.lower()
print(f"INPUT4: n={len(joined)} naive_rho={naive:.3f} corrected_rho={corrected:.3f}")

# Inputs 5 and 9: source implementation sensitivity and specificity.
mod = load_module("phase2_consensus", SOURCE / "scripts" / "consensus_hits.py")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mismatch = mod.consensus_hits(DATA / "mageck_hap1.gene_summary.txt", DATA / "bayes_factor.txt", DATA / "drugz_drug_output.txt")
warning_text = buf.getvalue()
assert warning_text.count("WARNING:") == 2 and int((mismatch.consensus_count == 3).sum()) == 0
(OUT / "input05_warnings.txt").write_text(warning_text, encoding="utf-8")
print("INPUT5: mismatched essentiality/drugZ pair emitted 2 warnings and 0 three-method calls")

rep1 = pd.read_csv(DATA / "bayes_factor.txt", sep="\t").rename(columns={"BF": "BF1"})
rep2 = pd.read_csv(DATA / "bayes_factor_rep2.txt", sep="\t").rename(columns={"BF": "BF2"})
rerun = rep1.merge(rep2, on="GENE")
rerun["h1"] = rerun.BF1 > 6; rerun["h2"] = rerun.BF2 > 6
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    warnings_rerun = mod._check_comparable(rerun, ["h1", "h2"])
assert warnings_rerun == []
matched = pd.read_csv(DATA / "mageck_hap1.gene_summary.txt", sep="\t")[["id", "neg|fdr"]].rename(columns={"id": "gene"}).merge(bagel[["gene", "BF"]], on="gene")
matched["m"] = matched["neg|fdr"] < .05; matched["b"] = matched.BF > 6
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    warnings_matched = mod._check_comparable(matched, ["m", "b"])
assert warnings_matched == []
print("INPUT9: no false-positive warning on BAGEL reruns or matched MAGeCK+BAGEL pair")

# Input 6: known BAGEL unseeded rerun variance and source-side prevention.
max_diff = float((rerun.BF1-rerun.BF2).abs().max()); flips = int((rerun.h1 != rerun.h2).sum())
usage = (SOURCE / "usage-guide.md").read_text(encoding="utf-8")
assert round(max_diff, 1) == 26.7 and flips == 33 and "-s <int>" in skill and "sign-correcting" in usage
print(f"INPUT6: BF max_diff={max_diff:.3f}; threshold_flips={flips}; fixed-seed advice present")

# Input 7: empty-consensus reasoning answer is grounded in the failure-mode reference.
failure = (SOURCE / "references" / "failure-modes.md").read_text(encoding="utf-8")
answer7 = ("Do not attribute an empty three-method consensus to QC alone. First verify that all files represent the same experimental comparison, "
           "inspect the overlap-enrichment warnings, and then assess each method's own QC (including PR-AUC). Only after ruling out a mismatched comparison should QC be re-audited.")
assert "not from the same experimental comparison" in failure and "Only re-audit QC" in failure
(OUT / "input07_response.txt").write_text(answer7 + "\n", encoding="utf-8")
print("INPUT7: empty consensus response distinguishes mismatched comparisons from QC")

# Input 8: source example and source three-method code share the documented thresholds.
inline = mod.consensus_hits(DATA / "mageck_hap1.gene_summary.txt", DATA / "bayes_factor.txt", DATA / "drugz_drug_output.txt")
source_example = (SOURCE / "examples" / "consensus_hits.py").read_text(encoding="utf-8")
assert "< 0.05" in source_example and "> 6" in source_example
assert int((inline.mageck_hit & inline.bagel_hit).sum()) == len(cons) == 844
print("INPUT8: source example and source 3-method implementation give 844 same-pair consensus calls")

# Input 10: new synthetic NTC-calibrated custom z-score run through the shipped CLI.
rng = np.random.default_rng(20260923)
rows = []
for gene_i in range(200):
    gene = f"NonTargeting_{gene_i:03d}" if gene_i < 60 else f"GENE_{gene_i:03d}"
    dropout = 60 <= gene_i < 90
    for guide in range(4):
        ctrl = rng.poisson(1000, 2)
        treat = rng.poisson(150 if dropout else 1000, 2)
        rows.append([f"{gene}_g{guide}", gene, *ctrl, *treat])
synthetic = pd.DataFrame(rows, columns=["sgRNA", "Gene", "T0_1", "T0_2", "T18_1", "T18_2"]).set_index("sgRNA")
synthetic.to_csv(WORK / "input10_counts.tsv", sep="\t")
r10 = run("input10", [str(PY), str(SOURCE / "scripts" / "custom_zscore_hit_calling.py"), "input10_counts.tsv", "--ctrl", "T0_1,T0_2", "--treat", "T18_1,T18_2", "--ntc-prefix", "NonTargeting", "-o", "input10_zscore.tsv"])
z = pd.read_csv(WORK / "input10_zscore.tsv", sep="\t")
calls = set(z.loc[z.fdr < .05, "gene"]); planted = {f"GENE_{i:03d}" for i in range(60,90)}; ntc = {f"NonTargeting_{i:03d}" for i in range(60)}
nonplanted = {f"GENE_{i:03d}" for i in range(90,200)}
false_positives = calls & nonplanted
assert planted <= calls and len(calls & ntc) <= 3 and len(false_positives) <= 6
print(f"INPUT10: planted_recovered={len(planted & calls)}/30 NTC_calls={len(calls & ntc)} nonplanted_calls={len(false_positives)}")

# Input 11: new matched three-method synthetic fixture exercises all consensus_count=3.
genes = [f"SYN{i:03d}" for i in range(100)]; hits = set(genes[:12])
pd.DataFrame({"id": genes, "neg|fdr": [.001 if g in hits else .8 for g in genes]}).to_csv(WORK / "input11_mageck.tsv", sep="\t", index=False)
pd.DataFrame({"GENE": genes, "BF": [12 if g in hits else 0 for g in genes]}).to_csv(WORK / "input11_bagel.tsv", sep="\t", index=False)
pd.DataFrame({"GENE": genes, "fdr_synth": [.001 if g in hits else .8 for g in genes]}).to_csv(WORK / "input11_drugz.tsv", sep="\t", index=False)
r11 = run("input11", [str(PY), str(SOURCE / "scripts" / "consensus_hits.py"), "input11_mageck.tsv", "input11_bagel.tsv", "input11_drugz.tsv", "-o", "input11_consensus.tsv"])
syn = pd.read_csv(WORK / "input11_consensus.tsv", sep="\t")
assert int((syn.consensus_count == 3).sum()) == 12 and "WARNING" not in r11.stdout
print("INPUT11: matched synthetic three-method run recovered 12/12 tier-1 hits without warning")

print("ALL_PHASE2_DYNAMIC_ASSERTIONS=PASS")
