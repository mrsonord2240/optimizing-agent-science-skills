"""Phase 2 regression of the shipped GI example on fresh synthetic data."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
SOURCE_EXAMPLE = Path(r"F:\OpenScience\wt\crispr-screens-combinatorial-screens\crispr-screens\combinatorial-screens\examples\gi_scoring.py")
rng = np.random.default_rng(20260923)
genes = [f"P{i:04d}" for i in range(500)]
singles = pd.DataFrame({"gene": genes, "lfc": rng.normal(-0.25, 0.12, len(genes))})
lookup = dict(zip(singles.gene, singles.lfc))
rows, planted_sl, planted_sr = [], set(), set()
for i in range(250):
    a, b = genes[2 * i], genes[2 * i + 1]
    pair = (a, b)
    gi = -1.7 if i < 8 else (1.7 if 8 <= i < 12 else rng.normal(0, 0.12))
    if i < 8:
        planted_sl.add(pair)
    elif i < 12:
        planted_sr.add(pair)
    for rep in range(4):
        rows.append({"cassette_id": f"C{i:03d}_{rep}", "gene_A": a, "gene_B": b,
                     "lfc": lookup[a] + lookup[b] + gi + rng.normal(0, 0.025)})
pd.DataFrame(rows).to_csv(RUN / "paired_lfc.tsv", sep="\t", index=False)
singles.to_csv(RUN / "single_lfc.tsv", sep="\t", index=False)
completed = subprocess.run([sys.executable, str(SOURCE_EXAMPLE)], cwd=RUN, text=True,
                           capture_output=True, check=True)
(RUN / "phase2_gi_regression.stdout.txt").write_text(completed.stdout, encoding="utf-8")
result = pd.read_csv(RUN / "gi_scores.tsv", sep="\t")
fdr_sl = set(map(tuple, result.loc[result.gi_class_fdr.eq("synthetic_lethal"), ["gene_A", "gene_B"]].to_numpy()))
fdr_sr = set(map(tuple, result.loc[result.gi_class_fdr.eq("synthetic_rescue"), ["gene_A", "gene_B"]].to_numpy()))
assert planted_sl <= fdr_sl, planted_sl - fdr_sl
assert planted_sr <= fdr_sr, planted_sr - fdr_sr
assert len(fdr_sl - planted_sl) == 0
assert len(fdr_sr - planted_sr) == 0
assert {"gi_pvalue", "gi_fdr", "gi_class_fdr"} <= set(result.columns)
print(f"ASSERT PASS: BH-FDR recovered {len(fdr_sl)}/8 planted SL and {len(fdr_sr)}/4 planted rescue; 0 false calls.")
