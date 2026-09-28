"""Independently validate generated tables, images, source identity, and evidence inventory."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "run"
OUTPUT = RUN / "output"
SKILL_COPY = RUN / "skill-copy"
PROVIDER = Path(r"F:\OpenScience\wt\backlog-statistical-annotation")
PROVIDER_SKILL = PROVIDER / "skills" / "bio-data-visualization-statistical-annotation"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


head = subprocess.run(
    ["git", "-C", str(PROVIDER), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
expected_head = "a74fdbc6b6001691903e5051ce36f3fba93bb966"
assert head == expected_head

source_hashes: dict[str, str] = {}
for copied in sorted(path for path in SKILL_COPY.rglob("*") if path.is_file()):
    relative = copied.relative_to(SKILL_COPY)
    provider = PROVIDER_SKILL / relative
    assert provider.is_file(), f"provider file missing for {relative}"
    copied_hash = sha256(copied)
    provider_hash = sha256(provider)
    assert copied_hash == provider_hash, f"source copy differs: {relative}"
    source_hashes[str(relative).replace("\\", "/")] = copied_hash

python_metrics = json.loads((OUTPUT / "python_metrics.json").read_text(encoding="utf-8"))
assert len(python_metrics["four_group_bh"]["pairs"]) == 6
assert python_metrics["paired"]["p_adj"] == python_metrics["paired"]["shuffled_p_adj"]
assert abs(python_metrics["welch"]["welch_p"] - python_metrics["welch"]["student_p"]) > 1e-4
assert python_metrics["effect_contract"]["effect_types"] == ["rank_biserial_r"]

border = pd.read_csv(OUTPUT / "py_border_holm.results.csv")
assert (border.p < 0.05).sum() == 3
assert (border.p_adj < 0.05).sum() == 1

r_metrics = (OUTPUT / "r_metrics.txt").read_text(encoding="utf-8")
for required in (
    "input1_holm",
    "input2_shuffled_p",
    "input3_labels ns,***,ns",
    "input4_tukey",
    "input5_lmm_p",
    "input6_cohen_d",
    "input7_two_default Wilcoxon",
    "input7_three_default Kruskal-Wallis",
    "input9_error each subject_id must belong to exactly one group",
    "input10_auto_spacing 0.18",
    "input10_custom_spacing 0.2",
    "input10_alternate_guidance compact-letter limitations documented",
    "input11_r_contract group1,group2,test,adjust_method,family_size,effect_type,effect_size",
    "input11_r_effect_types rank_biserial_r,hedges_g",
):
    assert required in r_metrics, f"missing R evidence: {required}"

# Input 11 joins independently written R and Python outputs.  The pair order,
# declared effect type, and signed rank-biserial values must agree exactly
# enough to rule out a direction or persistence mismatch.
r_contract = pd.read_csv(OUTPUT / "r_four_holm.results.csv")
py_contract = pd.read_csv(OUTPUT / "py_four_group_effect_contract.results.csv")
assert list(zip(r_contract.group1, r_contract.group2, strict=True)) == list(
    zip(py_contract.group1, py_contract.group2, strict=True)
)
assert set(r_contract.effect_type) == set(py_contract.effect_type) == {"rank_biserial_r"}
np.testing.assert_allclose(r_contract.effect_size, py_contract.effect_size, rtol=0, atol=1e-12)

skill_text = (SKILL_COPY / "SKILL.md").read_text(encoding="utf-8")
assert "compact-letter display" in skill_text
assert "does not show exact per-pair p-values or effects" in skill_text

image_metrics: dict[str, dict[str, object]] = {}
pngs = sorted(OUTPUT.rglob("*.png"))
assert len(pngs) >= 25
for path in pngs:
    with Image.open(path) as image:
        rgb = np.asarray(image.convert("RGB"))
    nonwhite = float(np.mean(np.any(rgb < 250, axis=2)))
    width, height = int(rgb.shape[1]), int(rgb.shape[0])
    assert width >= 500 and height >= 500, f"undersized image: {path.name} {width}x{height}"
    assert nonwhite > 0.01, f"blank image: {path.name} nonwhite={nonwhite}"
    image_metrics[str(path.relative_to(OUTPUT)).replace("\\", "/")] = {
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "nonwhite_fraction": round(nonwhite, 6),
        "sha256": sha256(path),
    }

manifest = {
    "provider_commit": head,
    "provider_source": "mrsonord2240/optimized-scientific-skills@a74fdbc6b6001691903e5051ce36f3fba93bb966:skills/bio-data-visualization-statistical-annotation",
    "source_hashes": source_hashes,
    "image_metrics": image_metrics,
    "assertions": {
        "provider_commit_exact": True,
        "skill_copy_byte_identical": True,
        "border_holm_one_survivor": True,
        "paired_shuffle_invariant": True,
        "welch_differs_from_student": True,
        "nested_cross_group_subject_rejected": True,
        "dense_family_spacing_and_alternate_guidance": True,
        "effect_contract_persisted_cross_language": True,
    },
}
(RUN / "evidence_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
print("Evidence verification passed")
