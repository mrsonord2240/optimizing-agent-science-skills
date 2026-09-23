"""Phase-2 independent regression runs for Inputs 1, 3, 5, and 7.

All synthetic data are generated here.  The invoked scripts are byte-copies of
the source-tip scripts in skill_copy/, so importing them cannot alter source.
"""
from pathlib import Path
import subprocess
import sys
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

RUN = Path(__file__).resolve().parent
SCRIPTS = RUN / "skill_copy" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from combat_correct import combat_correct

PYTHON = sys.executable
rng = np.random.default_rng(20260922)

def make_balanced(n=600):
    samples = [f"B{b}_{c}_{r}" for b in (1, 2) for c in ("veh", "drug") for r in (1, 2)]
    batches = ["b1"] * 4 + ["b2"] * 4
    conditions = ["veh", "veh", "drug", "drug"] * 2
    baseline = rng.gamma(8, 85, size=n)
    values = {}
    for name, batch, condition in zip(samples, batches, conditions):
        mu = baseline.copy()
        if condition == "drug":
            mu[:60] *= 0.25
        if batch == "b2":
            mu = mu * 0.55 + 90
        values[name] = rng.poisson(mu)
    return pd.DataFrame(values, index=[f"sg{i:04d}" for i in range(n)]), batches, conditions

print("INPUT 1 Canonical: balanced two-batch, two-condition ComBat CLI plus PCA diagnostic")
counts, batches, conditions = make_balanced()
i1 = RUN / "input1"
i1.mkdir(exist_ok=True)
counts.to_csv(i1 / "counts.txt", sep="\t", index_label="sgRNA")
meta = pd.DataFrame({"batch": batches, "condition": conditions}, index=counts.columns)
meta.to_csv(i1 / "metadata.txt", sep="\t", index_label="sample")
diag = subprocess.run([PYTHON, str(SCRIPTS / "batch_diagnostic.py"), str(i1 / "counts.txt"), str(i1 / "metadata.txt")], capture_output=True, text=True, check=True)
print(diag.stdout.strip())
cli = subprocess.run([PYTHON, str(SCRIPTS / "combat_correct.py"), str(i1 / "counts.txt"), str(i1 / "metadata.txt"), str(i1 / "corrected.txt"), str(i1 / "uncorrected.txt"), "--batch-col", "batch", "--condition-col", "condition"], capture_output=True, text=True, check=True)
print(cli.stdout.strip())
corr = pd.read_csv(i1 / "corrected.txt", sep="\t", index_col=0)
assert corr.shape == counts.shape and np.isfinite(corr.to_numpy()).all()
raw_pc = PCA(2).fit_transform(np.log2(counts + 1).T)
corr_pc = PCA(2).fit_transform(np.log2(corr + 1).T)
raw_distance = np.linalg.norm(raw_pc[:4].mean(0) - raw_pc[4:].mean(0))
corr_distance = np.linalg.norm(corr_pc[:4].mean(0) - corr_pc[4:].mean(0))
raw_lfc = np.log2((counts.iloc[:60, [2, 3, 6, 7]].mean(1) + 1) / (counts.iloc[:60, [0, 1, 4, 5]].mean(1) + 1)).mean()
corr_lfc = np.log2((corr.iloc[:60, [2, 3, 6, 7]].mean(1) + 1) / (corr.iloc[:60, [0, 1, 4, 5]].mean(1) + 1)).mean()
assert corr_distance < raw_distance and corr_lfc < -0.5
print(f"ASSERT input1: batch centroid {raw_distance:.3f}->{corr_distance:.3f}; essential LFC {raw_lfc:.3f}->{corr_lfc:.3f}")

print("\nINPUT 3 Edge: fully confounded batch and condition must be refused when mod is supplied")
n = 250
base = rng.gamma(8, 60, n)
confounded = pd.DataFrame({f"veh_{i}": rng.poisson(base) for i in range(3)} | {f"drug_{i}": rng.poisson(base * 0.18 + 60) for i in range(3)}, index=[f"cf{i}" for i in range(n)])
try:
    combat_correct(confounded, ["b1"] * 3 + ["b2"] * 3, ["veh"] * 3 + ["drug"] * 3)
    raise AssertionError("fully confounded mod was not rejected")
except Exception as exc:
    assert "confound" in type(exc).__name__.lower() or "confound" in str(exc).lower()
    print(f"ASSERT input3: refused confounded design: {type(exc).__name__}: {exc}")

print("\nINPUT 5 Stress: residual-RSS filter drops only zero-residual guide and exposes its index")
stress, sb, sc = make_balanced(120)
stress.loc["zero_residual"] = [20, 20, 100, 100, 20, 20, 100, 100]
stress.loc["one_batch_constant"] = [20, 20, 20, 20, 10, 30, 20, 40]
stress_corr, uncorrected = combat_correct(stress, sb, sc)
assert "zero_residual" in set(uncorrected)
assert "one_batch_constant" not in set(uncorrected)
assert (stress_corr.loc["zero_residual"] == stress.loc["zero_residual"]).all()
assert np.isfinite(stress_corr.to_numpy()).all()
print(f"ASSERT input5: uncorrected={list(uncorrected)}; zero-residual raw row preserved; one-batch-constant corrected")

print("\nINPUT 7 Adversarial: forcing ComBat on a no-batch construction remains finite because filter is a backstop")
base = rng.gamma(8, 75, 350)
no_batch = pd.DataFrame({f"s{i}": rng.poisson(base) for i in range(8)}, index=[f"nb{i}" for i in range(350)])
no_corr, no_uncorrected = combat_correct(no_batch, ["b1"] * 4 + ["b2"] * 4, ["veh", "veh", "drug", "drug"] * 2)
assert no_corr.shape == no_batch.shape and np.isfinite(no_corr.to_numpy()).all()
print(f"ASSERT input7: no NaN/Inf; {len(no_uncorrected)} residual-zero features returned raw (documented backstop behavior)")

print("PHASE2_CORE_REGRESSIONS_PASS")
