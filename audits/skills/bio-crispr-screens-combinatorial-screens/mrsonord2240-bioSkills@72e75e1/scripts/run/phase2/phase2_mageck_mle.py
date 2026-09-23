"""Phase 2 re-run of the SKILL.md MAGeCK MLE design-matrix workflow."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parent
MAGECK = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck")
rng = np.random.default_rng(2026092304)
samples = ["NT_r1", "NT_r2", "A_r1", "A_r2", "B_r1", "B_r2", "AB_r1", "AB_r2"]
rows = []
for gene in ["GENEA", "GENEB"] + [f"BG{i:02d}" for i in range(1, 39)]:
    for guide in range(5):
        row = {"sgRNA": f"{gene}_sg{guide}", "gene": gene}
        for sample in samples:
            factor = 1.0
            condition = sample.split("_")[0]
            if gene == "GENEA" and condition in ("A", "AB"):
                factor *= 0.55
            if gene == "GENEB" and condition in ("B", "AB"):
                factor *= 0.55
            if gene == "GENEA" and condition == "AB":
                factor *= 0.5
            row[sample] = rng.poisson(500 * factor)
        rows.append(row)
pd.DataFrame(rows).to_csv(RUN / "combo_counts.txt", sep="\t", index=False)
(RUN / "combo_design.txt").write_text("""Samples\tbaseline\tgeneA\tgeneB\tinteraction
NT_r1\t1\t0\t0\t0
NT_r2\t1\t0\t0\t0
A_r1\t1\t1\t0\t0
A_r2\t1\t1\t0\t0
B_r1\t1\t0\t1\t0
B_r2\t1\t0\t1\t0
AB_r1\t1\t1\t1\t1
AB_r2\t1\t1\t1\t1
""", encoding="utf-8")
for suffix in ("phase2_mle_run1", "phase2_mle_run2"):
    command = [sys.executable, str(MAGECK), "mle", "--count-table", "combo_counts.txt",
               "--design-matrix", "combo_design.txt", "--output-prefix", suffix]
    done = subprocess.run(command, cwd=RUN, text=True, capture_output=True, check=True)
    (RUN / f"{suffix}.stdout.txt").write_text(done.stdout + done.stderr, encoding="utf-8")
a = pd.read_csv(RUN / "phase2_mle_run1.gene_summary.txt", sep="\t").set_index("Gene")
b = pd.read_csv(RUN / "phase2_mle_run2.gene_summary.txt", sep="\t").set_index("Gene")
assert {"geneA|beta", "geneB|beta", "interaction|beta", "interaction|fdr"} <= set(a.columns)
rank = int((a["interaction|beta"] < a.loc["GENEA", "interaction|beta"]).sum() + 1)
beta_same = bool((a["interaction|beta"].round(12) == b["interaction|beta"].round(12)).all())
fdr_diff = int((a["interaction|fdr"] != b["interaction|fdr"]).sum())
assert rank == 1
assert beta_same
print(f"ASSERT PASS: GENEA interaction beta rank={rank}/40; beta_identical={beta_same}; fdr_differences={fdr_diff}/40.")
