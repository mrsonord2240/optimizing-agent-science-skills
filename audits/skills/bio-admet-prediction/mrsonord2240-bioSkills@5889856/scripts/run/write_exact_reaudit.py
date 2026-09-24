"""Render the retained exact-commit report and viewer after fix_reaudit.py passes."""

import json
import subprocess
from pathlib import Path


audit_dir = Path(__file__).parents[1]
worktree = Path(r"F:\OpenScience\wt\bio-admet-prediction")
commit = subprocess.check_output(
    ["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True
).strip()
assert commit == "5889856f17650bafa9b1169bafb5dedb97db79d6"

inputs = [
    (1, "Canonical", "Offline batch triage with structural alerts and ADMET-AI", 95, 4, 4,
     "Exact-commit source route predicted hERG/AMES/DILI/BBB and 5 CYP endpoints for 293/300 gate-passing organic molecules; 7 are retained as rejects rather than silently dropped."),
    (2, "Variant A", "Optional ADMETlab hosted-output contract", 90, 4, 4,
     "The service client remains deliberately external to the live official contract; the exact source validates structure, uncertainty and optional task-ID columns and gives named missing-file/contract errors."),
    (3, "Variant B", "Chemprop custom-endpoint reproducibility", 93, 4, 4,
     "Exact Chemprop 2.3.1 help exposes --data-seed and --pytorch-seed; the obsolete --seed advice is removed. The unchanged prior model-training evidence is reused."),
    (4, "Edge", "hERG triage against measured series", 96, 5, 5,
     "The exact source emits hERG predictions after an auditable gate; no point prediction is offered for rejected chemistry and manual-review results remain visible."),
    (5, "Stress", "Five-CYP DDI panel", 93, 4, 4,
     "All five documented CYP inhibitor columns were selected successfully from the exact source route; prior 300-compound inhibitor/substrate ambiguity results are unchanged and reused."),
    (6, "Scope Boundary", "Safety-to-dose request", 92, 4, 4,
     "Unchanged guardrails continue to reject a clinical or regulatory conclusion from a point prediction; pre-fix text evidence is reused after a direct exact-commit diff check."),
    (7, "Adversarial", "OOD metals, salts, macrocycles, peptides and PROTACs", 96, 5, 5,
     "Exact source rejects cisplatin and sodium chloride and sends macrocycles, peptide, PROTAC and paclitaxel to manual review before prediction."),
]

report = {
    "meta": {
        "skill_name": "bio-admet-prediction",
        "description": "Offline ADMET-AI 2.x triage with explicit local similarity screening; optional validated ADMETlab hosted results; chemprop and structural-alert safeguards.",
        "source": f"mrsonord2240/bioSkills@{commit}:chemoinformatics/admet-prediction",
        "evaluated_on": "2026-09-24",
        "evaluator_version": "skill-auditor@1.0 exact-commit fix pass",
        "category": "Data Analysis",
        "execution_mode": "A",
        "complexity": "Complex",
        "n_inputs": 7,
        "executed_inputs": "7/7 (changed paths executed; unchanged evidence explicitly reused)"
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Existing study/split attribution remains intact; the new offline route is explicitly point-prediction triage rather than a performance claim."},
            "practice_boundaries": {"result": "PASS", "detail": "The hERG and dosing guardrails remain explicit; all gate and prediction guidance says that experiments and applicable ICH/regulatory guidance control important decisions."},
            "methodological_ground": {"result": "PASS", "detail": "The new gate uses a caller-supplied relevant reference set and a leave-one-out calibrated threshold, and explicitly disclaims that this proves a model training domain."},
            "code_usability": {"result": "PASS", "detail": "The committed example executed with ADMET-AI 2.0.1: named endpoint predictions, ADMETlab contract failures, and salt/metal/OOD handling all passed."}
        }
    },
    "static_score": {
        "subtotal": 96, "max": 100,
        "categories": {
            "functional_suitability": {"score": 12, "max": 12, "note": "Primary tool is now an executable offline prediction route."},
            "reliability": {"score": 12, "max": 12, "note": "Named loader failures, endpoint validation, input gate and version-major pin close all reported reliability gaps."},
            "security": {"score": 11, "max": 12, "note": "No credentials or unverified hosted endpoint are embedded."},
            "performance_context": {"score": 7, "max": 8, "note": "The gate and batch predictor are compact, but model loading remains a substantial local dependency."},
            "maintainability": {"score": 11, "max": 12, "note": "One bundled example owns the executable mechanics; task names are validated rather than duplicated."},
            "agent_usability": {"score": 16, "max": 16, "note": "The primary executable route, optional hosted boundary, and stop conditions are unambiguous."},
            "human_usability": {"score": 8, "max": 8, "note": "Decision table and runnable batch example map directly to triage requests."},
            "agent_specific": {"score": 19, "max": 20, "note": "No silent filtering, no fabricated universal similarity cutoff, and no implied uncertainty from percentiles."}
        }
    },
    "dynamic_score": {
        "execution_avg": 93.6, "max": 100,
        "assertion_pass_rate": {"passed": 30, "total": 30},
        "inputs": [
            {"index": index, "type": kind, "label": label, "status": "COMPLETED", "status_flag": "✅", "basic": round(total * .4), "specialized": total - round(total * .4), "total": total, "assertions_passed": passed, "assertions_total": assertion_total, "note": note}
            for index, kind, label, total, passed, assertion_total, note in inputs
        ]
    },
    "final": {"static_weighted": 38.4, "dynamic_weighted": 56.2, "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The declared primary workflow now executes fully offline in the installed ADMET-AI 2.0.1 environment.",
        "The gate is operational: salts/metals reject before prediction, unusual large organic chemistry stays visible for manual review, and similarity thresholds derive from relevant reference chemistry.",
        "The hosted ADMETlab route is no longer misrepresented as bundled execution: its optional result loader validates the contract and preserves current-service responsibility.",
        "Chemprop 2.3.1 seed guidance now names two valid flags and the established hERG/CYP/clinical-boundary safeguards remain intact."
    ],
    "recommendations": []
}

(audit_dir / "eval_report_bio-admet-prediction_result.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)

rows = "\n".join(
    f"| {index} | {kind} | {total} | {passed}/{assertion_total} PASS | ✅ |"
    for index, kind, _label, total, passed, assertion_total, _note in inputs
)
details = "\n\n".join(
    f"### Input {index} — {label}\n\n{note}\n\n**Score:** {total}/100 · **Assertions:** {passed}/{assertion_total} PASS"
    for index, _kind, label, total, passed, assertion_total, note in inputs
)
viewer = f"""# Eval Viewer — bio-admet-prediction

Generated: 2026-09-24 · Exact-commit fix re-audit

Source: `mrsonord2240/bioSkills@{commit}:chemoinformatics/admet-prediction`

This replaces the 2026-09-16 report (86/100, Limited Release). The prior report is retained as `eval_viewer_bio-admet-prediction_pre_fix_d91ed3d.md` and its JSON peer. Changed behavior was freshly executed against the exact commit; unchanged findings reuse the recorded 2026-09-16 execution evidence only where a direct diff showed the relevant code/text was unchanged.

Environment: `F:\\OpenScience\\audit-envs\\cheminformatics-hit-triage-analyst\\tools\\admet-ai-venv` (ADMET-AI 2.0.1) and its Chemprop 2.3.1 sibling. Exact-commit script: `run/fix_reaudit.py`; captured output: `run/fix_reaudit_5889856.out`. It ran the committed example's loader/gate/predictor; selected hERG, AMES, DILI, BBB and five CYP columns; tested a 300-compound ChEMBL hERG series and nine OOD probes. Chemprop help is retained in `run/chemprop_2_3_1_seed_help_5889856.out`.

## Summary

| Input | Type | Total /100 | Assertions | Status |
|---|---|---:|---:|---|
{rows}

**Execution average:** 93.6/100 · **Assertions:** 30/30 (100%)

**Static:** 96/100 · **Final:** **95/100 — Production Ready** · Deployable: yes

## Exact-commit evidence

- Primary ADMET-AI route: committed code produced all nine selected endpoints for 293 gate-passing compounds. The 300-row gate retained seven rejected inputs; it did not silently drop them.
- OOD gate: cisplatin and sodium chloride were rejected before prediction. The macrocycle, cyclic peptide, linear peptide, PROTAC-like probe and paclitaxel were retained as `manual_review` rather than presented as confident point predictions.
- Optional ADMETlab result loader: valid contract passed; missing file, absent uncertainty column, and unrelated CSV each raised a named, actionable failure.
- Chemprop: installed 2.3.1 help confirms `--data-seed` and `--pytorch-seed`; the invalid `--seed` advice is gone.

{details}

## Veto and conclusion

Skill Veto and Research Veto both PASS. The original P1s are closed: the primary route is executable, and its OOD mitigation is available in the runnable code. The original P2s are closed: ADMETlab results have a real local contract, Chemprop uses current seed flags, and the ADMET-AI compatibility pin is explicitly 2.x. No P0/P1/P2 findings remain open.
"""
(audit_dir / "eval_viewer_bio-admet-prediction.md").write_text(viewer, encoding="utf-8")
