"""Build the c3ca7ea exact-commit report after validating saved run evidence."""

import copy
import json
import subprocess
from pathlib import Path


AUDIT = Path("F:/OpenScience/audits/bio-single-cell-preprocessing")
RUN = AUDIT / "run/final-corrective-20260924"
SOURCE = Path("F:/OpenScience/worktrees/bio-single-cell-preprocessing-fixpass")
REPORT = AUDIT / "eval_report_bio-single-cell-preprocessing_result.json"


def require(path, *markers):
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        assert marker in text, f"{path.name} lacks expected evidence: {marker}"
    return text


head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True
).strip()
assert head == "c3ca7ea1aa3aacf4efebc322b9b01dee31fe3917"

require(RUN / "input1-rerun.log", "VERBATIM_SKILL_BLOCK_OK = True", "HVGs: 2000")
require(RUN / "input2-rerun.log", "mean |error| = 0.0515", "counts removed: 1 %", "DONE")
require(RUN / "input3-rerun.log", "survivors=84/120")
require(RUN / "input4-rerun.log", "SCTransform: ", "scran size factors:", "DONE")
require(RUN / "input5-rerun.log", "precision=0.510", "reciprocal condition number", "DONE")
require(RUN / "input7-rerun.log", "ratio 0.662", "DONE")
require(RUN / "sources.log", "PASS: 10/10 exact-source assertions")
require(
    RUN / "qc.log",
    "PASS: nuclei MAD guard stopped",
    "PASS: per-batch seurat_v3 HVG completed with 2000 genes",
)
require(RUN / "soupx-current.log", "PASS: SoupX 1.6.2", "removed= 8.5 %")
require(
    RUN / "scanpy-example-rerun.log",
    "Raw: 707 cells, 12521 genes",
    "Filtered: 657 cells, 11109 genes",
    "Saved preprocessed data",
)
require(
    RUN / "seurat-example-rerun.log",
    "Filtered: 658 cells",
    "PASS: packaged Seurat example produced 658 cells and 3000 variable features",
)

report = json.loads(REPORT.read_text(encoding="utf-8"))
report["meta"].update(
    {
        "n_inputs": 9,
        "source": (
            "mrsonord2240/bioSkills@"
            "c3ca7ea1aa3aacf4efebc322b9b01dee31fe3917:single-cell/preprocessing"
        ),
        "executed_inputs": "8/9",
        "regression_inputs": [1, 2, 3, 4, 5, 6, 7],
        "new_inputs": [8, 9],
        "n_inputs_note": (
            "The seven archived inputs were rerun as regressions and two fresh packaged-example "
            "inputs were added, as required by the final-pass brief. Input 6 is text-only."
        ),
        "audit_type": "final-pass exact-commit corrective re-audit",
    }
)

categories = report["static_score"]["categories"]
categories["functional_suitability"]["note"] = (
    "Core QC, ambient-correction, normalization, and feature-selection routes are present; "
    "the audited Scanpy, Seurat, SoupX, and batch-HVG paths execute on the saved fixtures."
)
categories["maintainability"]["note"] = (
    "Python and R routes are separated and both packaged examples now share the documented "
    "adaptive-QC policy; the repository still has no general automated test harness."
)

inputs = report["dynamic_score"]["inputs"][:7]
report["dynamic_score"]["inputs"] = inputs
inputs[1]["note"] = inputs[1]["execution_note"] = (
    "The archived eight-sample and real-PBMC regression reran, and the exact corrected SoupX "
    "route completed on 707 cells with rho 0.085 and 8.5% of counts removed."
)
inputs[1]["assertions"][0]["note"] = (
    "Exact corrected route rerun from the saved audit harness against Cell Ranger raw and "
    "filtered matrices; clustering was supplied before autoEstCont."
)
inputs[2]["note"] = inputs[2]["execution_note"] = (
    "The archived fixture reproduced its former 70% survivor result; the exact corrected guard "
    "separately stopped on zero MAD before subsetting, and nuclei now use MAD-only mito policy."
)
inputs[2]["assertions"][1]["note"] = (
    "The c3ca7ea exact-path check raised the documented MAD-collapse ValueError before subsetting."
)
inputs[4]["note"] = inputs[4]["execution_note"] = (
    "The archived stress regression reproduced the former singular loess failure; the exact "
    "corrected per-batch filter retained 7,846 genes and selected 2,000 HVGs successfully."
)
inputs[4]["assertions"][1]["note"] = (
    "The c3ca7ea per-batch helper retained 7,846/12,521 genes and seurat_v3 selected 2,000 HVGs."
)

scanpy_input = {
    "index": 8,
    "type": "Fresh Variant A",
    "label": "Packaged Scanpy example on a 707-cell PBMC fixture",
    "status": "COMPLETED",
    "status_flag": "✅",
    "note": "The example shipped at c3ca7ea ran end to end: 707 raw cells, 657 retained cells, 11,109 genes, 2,000 HVGs, PCA, and an h5ad output.",
    "executed": True,
    "execution_note": "The example shipped at c3ca7ea ran end to end: 707 raw cells, 657 retained cells, 11,109 genes, 2,000 HVGs, PCA, and an h5ad output.",
    "basic": 38,
    "specialized": 57,
    "total": 95,
    "assertions_passed": 4,
    "assertions_total": 4,
    "assertions": [
        {"text": "The packaged Scanpy example executes without modification", "result": "PASS", "note": "Ran the exact source file from c3ca7ea; exit 0 and preprocessed.h5ad was written."},
        {"text": "Adaptive QC replaces the former flat mitochondrial cutoff", "result": "PASS", "note": "Four medians/MADs printed and unknown tissue used no hard mitochondrial cap."},
        {"text": "The survival guard permits this plausible fixture", "result": "PASS", "note": "657/707 cells survived, above the documented 80% stop boundary."},
        {"text": "Raw counts feed seurat_v3 HVG selection", "result": "PASS", "note": "The example stored layers['counts'] and selected exactly 2,000 HVGs from that layer."},
    ],
}

seurat_input = {
    "index": 9,
    "type": "Fresh Variant B",
    "label": "Packaged Seurat example on the same PBMC fixture",
    "status": "COMPLETED",
    "status_flag": "✅",
    "note": "The exact packaged R example ran through the audit library wrapper: 707 raw cells, 658 retained cells, 3,000 variable features, and an RDS output.",
    "executed": True,
    "execution_note": "The exact packaged R example ran through the audit library wrapper: 707 raw cells, 658 retained cells, 3,000 variable features, and an RDS output.",
    "basic": 38,
    "specialized": 57,
    "total": 95,
    "assertions_passed": 4,
    "assertions_total": 4,
    "assertions": [
        {"text": "The packaged Seurat example executes without source modification", "result": "PASS", "note": "The saved wrapper only prepended the private audit library and sourced the exact c3ca7ea example."},
        {"text": "Adaptive QC replaces the former fixed percent.mt filter", "result": "PASS", "note": "Counts, features, and mitochondrial MADs printed; no flat percent.mt < 20 filter remains."},
        {"text": "The survival guard permits this plausible fixture", "result": "PASS", "note": "658/707 cells survived, above the documented 80% stop boundary."},
        {"text": "The normalization route produces its declared artifact", "result": "PASS", "note": "SCTransform completed with 3,000 variable features and preprocessed.rds passed the wrapper checks."},
    ],
}

inputs.extend([scanpy_input, seurat_input])
dynamic = report["dynamic_score"]
dynamic["execution_avg"] = round(sum(row["total"] for row in inputs) / len(inputs), 1)
dynamic["assertion_pass_rate"] = {
    "passed": sum(row["assertions_passed"] for row in inputs),
    "total": sum(row["assertions_total"] for row in inputs),
}

report["final"].update(
    {
        "static_weighted": round(report["static_score"]["subtotal"] * 0.4, 1),
        "dynamic_weighted": round(dynamic["execution_avg"] * 0.6, 1),
        "score": 93,
    }
)
report["key_strengths"] = [
    "Both packaged preprocessing examples now implement the same MAD-adaptive, tissue-aware QC policy as the main Skill and execute end to end.",
    "The corrected SoupX path creates clusters before autoEstCont and completes on both synthetic and real Cell Ranger outputs.",
    "Zero-MAD and low-survival guards stop unsafe filtering, while nuclei and unknown tissues avoid copied mitochondrial hard caps.",
    "Per-batch gene filtering prevents the reproduced seurat_v3 shallow-batch loess failure and preserves 2,000 HVGs.",
]
report["recommendations"] = []

assert len(inputs) == report["meta"]["n_inputs"] == 9
assert dynamic["execution_avg"] == 92.9
assert dynamic["assertion_pass_rate"] == {"passed": 36, "total": 36}
assert report["final"]["static_weighted"] + report["final"]["dynamic_weighted"] == 92.5

REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"wrote {REPORT}")
print("9 inputs, 8 executed plus 1 text-only, 36/36 assertions, score 93")
