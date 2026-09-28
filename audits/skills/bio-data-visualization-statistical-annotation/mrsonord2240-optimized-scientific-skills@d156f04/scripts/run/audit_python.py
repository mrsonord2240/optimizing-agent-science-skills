"""Execute Python regressions and the new Welch-test case against the fixed skill."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu, ttest_ind
from statannotations.Annotator import Annotator
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "run" / "output"
SKILL = ROOT / "run" / "skill-copy"
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pairwise_module = load_module("fixed_pairwise", SKILL / "scripts" / "annotate_pairwise.py")
paired_module = load_module("fixed_paired", SKILL / "scripts" / "annotate_paired.py")

metrics: dict[str, object] = {}


def expected_mann_whitney(df: pd.DataFrame, method: str) -> tuple[list[tuple[str, str]], np.ndarray, np.ndarray]:
    groups = list(dict.fromkeys(df["group"].astype(str)))
    pairs = [(left, right) for i, left in enumerate(groups) for right in groups[i + 1 :]]
    raw = np.array(
        [
            mannwhitneyu(
                df.loc[df.group.astype(str) == left, "value"],
                df.loc[df.group.astype(str) == right, "value"],
                alternative="two-sided",
                method="auto",
            ).pvalue
            for left, right in pairs
        ]
    )
    method_map = {"BH": "fdr_bh", "bh": "fdr_bh", "fdr": "fdr_bh"}
    adjusted = multipletests(raw, method=method_map.get(method, method))[1]
    return pairs, raw, adjusted


# Inputs 1 and 3: explicit adjusted values must equal an independent SciPy +
# statsmodels computation, rather than statannotations' type-1 Holm display.
for stem, adjustment in (("three_group", "holm"), ("border", "holm")):
    df = pd.read_csv(DATA / f"{stem}.csv")
    result = pairwise_module.annotate_pairwise(
        str(DATA / f"{stem}.csv"), str(OUTPUT / f"py_{stem}_{adjustment}.png"), adjustment
    )
    pairs, raw, adjusted = expected_mann_whitney(df, adjustment)
    assert list(zip(result.group1, result.group2, strict=True)) == pairs
    np.testing.assert_allclose(result.p.to_numpy(), raw, rtol=0, atol=1e-12)
    np.testing.assert_allclose(result.p_adj.to_numpy(), adjusted, rtol=0, atol=1e-12)
    metrics[f"{stem}_{adjustment}"] = {
        "raw": raw.tolist(),
        "adjusted": adjusted.tolist(),
        "pairs": pairs,
    }

border_adjusted = np.asarray(metrics["border_holm"]["adjusted"])
assert sum(border_adjusted <= 0.05) == 1

# Input 4: exercise the repaired Python BH path on the full six-comparison
# family and prove the result table contains BH-adjusted values.
four_group = pd.read_csv(DATA / "four_group.csv")
four_bh = pairwise_module.annotate_pairwise(
    str(DATA / "four_group.csv"), str(OUTPUT / "py_four_group_bh.png"), "BH"
)
four_pairs, four_raw, four_adjusted = expected_mann_whitney(four_group, "BH")
np.testing.assert_allclose(four_bh.p_adj.to_numpy(), four_adjusted, rtol=0, atol=1e-12)
assert len(four_pairs) == 6
metrics["four_group_bh"] = {
    "raw": four_raw.tolist(),
    "adjusted": four_adjusted.tolist(),
    "pairs": four_pairs,
}

# Input 2: shuffled rows must not alter subject-ID pairing.  Also retain the
# negative regression that incomplete subject pairs are rejected.
paired_path = DATA / "paired.csv"
paired = paired_module.annotate_paired(str(paired_path), str(OUTPUT / "py_paired.png"), "holm")
shuffled_path = OUTPUT / "paired_shuffled.csv"
pd.read_csv(paired_path).sample(frac=1.0, random_state=20260927).to_csv(shuffled_path, index=False)
paired_shuffled = paired_module.annotate_paired(
    str(shuffled_path), str(OUTPUT / "py_paired_shuffled.png"), "holm"
)
np.testing.assert_allclose(paired.p_adj.to_numpy(), paired_shuffled.p_adj.to_numpy(), atol=1e-15)

incomplete_path = OUTPUT / "paired_incomplete.csv"
pd.read_csv(paired_path).iloc[1:].to_csv(incomplete_path, index=False)
try:
    paired_module.annotate_paired(str(incomplete_path), str(OUTPUT / "must_not_exist.png"), "holm")
except ValueError as error:
    incomplete_error = str(error)
else:
    raise AssertionError("incomplete subject pairs were not rejected")
assert "identical complete subject IDs" in incomplete_error
metrics["paired"] = {
    "p": float(paired.loc[0, "p"]),
    "p_adj": float(paired.loc[0, "p_adj"]),
    "shuffled_p_adj": float(paired_shuffled.loc[0, "p_adj"]),
    "incomplete_error": incomplete_error,
}

# New input 8: a complete Welch route following the skill's documented test
# name.  Compare the displayed p-value with an independent SciPy Welch test,
# and save magnitude as Hedges' g in both the table and caption.
welch = pd.read_csv(DATA / "welch_unequal_variance.csv")
reference = welch.loc[welch.group == "Reference", "value"].to_numpy()
treatment = welch.loc[welch.group == "Treatment", "value"].to_numpy()
welch_test = ttest_ind(reference, treatment, equal_var=False)
student_test = ttest_ind(reference, treatment, equal_var=True)
n1, n2 = len(reference), len(treatment)
s_pool = np.sqrt(((n1 - 1) * reference.var(ddof=1) + (n2 - 1) * treatment.var(ddof=1)) / (n1 + n2 - 2))
cohen_d = (treatment.mean() - reference.mean()) / s_pool
hedges_g = cohen_d * (1 - 3 / (4 * (n1 + n2) - 9))

fig, ax = plt.subplots(figsize=(6.5, 5.5))
sns.boxplot(data=welch, x="group", y="value", order=["Reference", "Treatment"], ax=ax)
sns.stripplot(
    data=welch,
    x="group",
    y="value",
    order=["Reference", "Treatment"],
    color="black",
    alpha=0.45,
    ax=ax,
)
annotator = Annotator(
    ax,
    [("Reference", "Treatment")],
    data=welch,
    x="group",
    y="value",
    order=["Reference", "Treatment"],
)
annotator.configure(test="t-test_welch", text_format="simple", show_test_name=True)
annotator.apply_and_annotate()
displayed_p = float(annotator.annotations[0].data.pvalue)
ax.set_title("Welch unequal-variance comparison")
ax.set_xlabel("")
fig.text(0.5, 0.01, f"Welch t; exact p={welch_test.pvalue:.6g}; Hedges' g={hedges_g:.3f}", ha="center")
fig.tight_layout(rect=(0, 0.04, 1, 1))
welch_plot = OUTPUT / "py_welch_unequal_variance.png"
fig.savefig(welch_plot, dpi=160)
annotation_text = [text.get_text() for text in ax.texts]
plt.close(fig)
np.testing.assert_allclose(displayed_p, welch_test.pvalue, rtol=0, atol=1e-12)
assert abs(displayed_p - student_test.pvalue) > 1e-4

pd.DataFrame(
    {
        "test": ["Welch independent t-test"],
        "p": [welch_test.pvalue],
        "student_p_for_contrast": [student_test.pvalue],
        "hedges_g": [hedges_g],
        "n_reference": [n1],
        "n_treatment": [n2],
    }
).to_csv(OUTPUT / "py_welch_unequal_variance.results.csv", index=False)
metrics["welch"] = {
    "welch_p": float(welch_test.pvalue),
    "student_p": float(student_test.pvalue),
    "displayed_p": displayed_p,
    "hedges_g": float(hedges_g),
    "annotation_text": annotation_text,
}

(OUTPUT / "python_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(json.dumps(metrics, indent=2))
print("Python re-audit assertions passed")
