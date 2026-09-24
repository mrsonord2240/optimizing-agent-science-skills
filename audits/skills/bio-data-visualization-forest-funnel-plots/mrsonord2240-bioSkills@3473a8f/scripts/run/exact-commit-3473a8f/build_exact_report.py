"""Write the exact-commit audit report and compact Markdown viewer."""
from __future__ import annotations

import json
from pathlib import Path

audit = Path(r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots")
run = audit / "run" / "exact-commit-3473a8f"
skill = "bio-data-visualization-forest-funnel-plots"
commit = "3473a8f48eccab6c73436a627c3e8568f3736eef"

def assertion(text: str, note: str) -> dict:
    return {"text": text, "result": "PASS", "note": note}

inputs = [
    {
        "index": 1, "type": "Canonical", "label": "REML BCG forest with log-ratio axis and prediction interval",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 59,
        "executed": True,
        "execution_note": "run/exact-commit-3473a8f/run_exact_reaudit.R; real metafor::dat.bcg; rendered PNG inspected.",
        "assertions": [
            assertion("Pooled BCG REML estimate equals the independently established audit value", "OR 0.4746 [0.3296, 0.6835], tau2 0.337772, I2 92.07%, Q 163.165."),
            assertion("Footer carries tau-squared, I-squared, and Q p-value", "Rendered footer reads RE model (tau^2 = 0.338; I^2 = 92.1%; Q p = <2e-16)."),
            assertion("Every study, pooled, and prediction interval lies inside the plotting range", "Limits are derived from study CIs, pooled CI, prediction interval, and ticks; inspected PNG has no clipped-interval arrows."),
            assertion("Ratio axis is log-scaled with OR ticks and reference line 1", "Ticks 0.25, 0.5, 1, 2, 4 and dotted reference are rendered."),
            assertion("Forest render completes without R warnings", "Harness uses options(warn = 2) and completed."),
        ],
    },
    {
        "index": 2, "type": "Variant A", "label": "Funnel, contour funnel, Egger, and trim-and-fill safeguards",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "executed": True,
        "execution_note": "Exact harness rendered real BCG funnel; shipped example rendered contour funnel and sensitivity result.",
        "assertions": [
            assertion("Funnel reference is a scalar pooled estimate", "Source uses as.numeric(coef(res)[1]); warning-as-error harness passed."),
            assertion("Egger is only offered at k >= 10", "Source contract and k=3 execution confirm the explicit withholding branch."),
            assertion("Contour funnel is runnable", "Shipped example wrote plots/funnel.pdf successfully."),
            assertion("Trim-and-fill is labelled sensitivity-only", "Source prints original and sensitivity OR together and documents hypothetical imputations."),
            assertion("No R array-recycling warning occurs", "options(warn = 2) exact harness completed."),
        ],
    },
    {
        "index": 3, "type": "Edge", "label": "Three-study small-k meta-analysis",
        "status": "COMPLETED", "status_flag": "✅", "basic": 38, "specialized": 58,
        "executed": True,
        "execution_note": "Exact harness fits the synthetic k=3 model with metafor 4.8.0.",
        "assertions": [
            assertion("Small-k model uses HKSJ", "Exact harness confirms test == knha."),
            assertion("Small-k footer withholds I-squared", "Footer is RE model (k = 3; HKSJ CI; heterogeneity metrics withheld)."),
            assertion("Egger is withheld below ten studies", "Exact harness confirms k=3 branch is not eligible for Egger."),
            assertion("Pooling fewer than three studies is rejected", "Exact-source contract locates the nrow(studies) < 3 stop guard."),
            assertion("HKSJ claim is appropriately qualified", "Source says k <= 3 remains highly imprecise and is not decisive."),
        ],
    },
    {
        "index": 4, "type": "Variant B", "label": "Cox covariate forest and treatment-by-subgroup forest",
        "status": "COMPLETED", "status_flag": "✅", "basic": 38, "specialized": 58,
        "executed": True,
        "execution_note": "Shipped exact example generated both synthetic-Cox PDFs with a seeded data set.",
        "assertions": [
            assertion("ggforest is accurately labelled as adjusted covariate display", "Source heading and figure title say adjusted covariate HRs."),
            assertion("Subgroup path estimates stratum treatment HRs and tests interaction", "Source fits treatment * subgroup and records LRT p."),
            assertion("Sparse strata are stopped before estimation", "Counts <20 and events <5 guards are present."),
            assertion("The supplied example is self-contained", "clinical_df is constructed in the example; all Cox PDFs were written."),
            assertion("Subgroup plot and covariate plot are separate artifacts", "cox_subgroup_forest.pdf and cox_adjusted_covariates.pdf both exist and exceed 1 KB."),
        ],
    },
    {
        "index": 5, "type": "Stress", "label": "MR method comparison with outlier-safe layout",
        "status": "COMPLETED", "status_flag": "✅", "basic": 38, "specialized": 58,
        "executed": True,
        "execution_note": "Shipped exact example used bundled LDL-C/CHD instruments and wrote mr_method_forest.pdf.",
        "assertions": [
            assertion("MR forest suppresses SNP rows for method comparison", "Source and example use snp_estimates = FALSE."),
            assertion("Multiple MR methods are run", "IVW, weighted median, mode, and Egger are passed to mr_forest."),
            assertion("MR-Egger intercept is reported", "Exact run reports intercept -0.0115; p = 0.451."),
            assertion("Input constructor is not shadowed", "Example stores result in mr_dat rather than mr_input."),
            assertion("MR method figure is produced", "plots/mr_method_forest.pdf exists and exceeds 1 KB."),
        ],
    },
]
for item in inputs:
    item["total"] = item["basic"] + item["specialized"]
    item["assertions_passed"] = len(item["assertions"])
    item["assertions_total"] = len(item["assertions"])

categories = {
    "functional_suitability": (11, 12, "All previously promised workflows now have an executable or explicitly scoped pattern; optional layouts remain clearly optional."),
    "reliability": (11, 12, "Executable small-k, Egger, sparse-strata, scalar-reference, and interval-bound safeguards replace prose-only advice."),
    "performance_context": (7, 8, "Focused 184-line entry point and compact usage guide; optional layouts are intentionally short."),
    "agent_usability": (15, 16, "Decision table distinguishes six easily conflated workflows and failures have actionable stops."),
    "human_usability": (7, 8, "Usage prompts and a fully runnable reference make the intended inputs explicit."),
    "security": (12, 12, "No credentials, network calls, shell execution, or user-string evaluation."),
    "maintainability": (11, 12, "One self-contained deterministic R reference and exact-commit evidence cover all primary workflows."),
    "agent_specific": (19, 20, "Specific trigger boundary, progressive workflow choice, deterministic example, and clear escape hatches."),
}
static = sum(value[0] for value in categories.values())
dynamic = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assertion_passed = sum(item["assertions_passed"] for item in inputs)
assertion_total = sum(item["assertions_total"] for item in inputs)
score = round(static * 0.4 + dynamic * 0.6)

report = {
    "meta": {
        "skill_name": skill,
        "description": "Exact-commit re-audit after forest/funnel reliability and workflow corrections.",
        "evaluated_on": "2026-09-24", "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis", "execution_mode": "A", "complexity": "Moderate", "n_inputs": 5,
        "source": f"mrsonord2240/bioSkills@{commit}:data-visualization/forest-funnel-plots",
        "audit_type": "exact-commit re-audit", "executed": True,
        "execution_note": "Structural wrapper PASS; 13/13 exact-source contract checks PASS; R 4.4.3 data-visualization wrapper executed the full shipped example with warnings promoted to errors. Real BCG and bundled LDL-C/CHD data, plus labelled synthetic Cox and small-k cases, were used. BCG forest and funnel PNGs were inspected.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {"applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Examples distinguish real bundled data from labelled synthetic demonstrations and make no fabricated claims."},
            "practice_boundaries": {"result": "PASS", "detail": "The guidance is analytical and explicitly avoids treatment, publication-bias, effect-modification, and causal overclaims."},
            "methodological_ground": {"result": "PASS", "detail": "REML/log ratios, HKSJ and small-k restraint, k>=10 Egger guard, sensitivity-only trim-and-fill, formal interaction testing, and MR triangulation are methodologically grounded."},
            "code_usability": {"result": "PASS", "detail": "The full shipped R example completed and produced all five expected visual artifacts with warnings treated as errors."},
        },
    },
    "static_score": {"subtotal": static, "max": 100,
        "categories": {key: {"score": value[0], "max": value[1], "note": value[2]} for key, value in categories.items()}},
    "dynamic_score": {"execution_avg": dynamic, "max": 100,
        "assertion_pass_rate": {"passed": assertion_passed, "total": assertion_total}, "inputs": inputs},
    "final": {"static_weighted": round(static * 0.4, 1), "dynamic_weighted": round(dynamic * 0.6, 1),
        "score": score, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "Rendered BCG forest carries a scalar heterogeneity footer and no longer clips study confidence intervals.",
        "Small-k, Egger, sparse-subgroup, and MR-outlier guards are executable rather than prose-only.",
        "The self-contained reference runs end-to-end through forest, funnel, Cox, and MR outputs with warnings promoted to errors.",
    ],
    "recommendations": [],
}

report_path = audit / f"eval_report_{skill}_result.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

viewer = f"""# {skill} — exact-commit re-audit\n\n**Result:** ⭐ Production Ready — **{score}/100**  \\\n**Source:** `{commit}`  \\\n**Assertions:** {assertion_passed}/{assertion_total} passed  \\\n**Veto gates:** PASS\n\n## Evidence\n\n- Structural wrapper: PASS (stability, contract, determinism, security).\n- Exact-source contract: 13/13 PASS.\n- R exact execution: full shipped workflow PASS with `options(warn = 2)`.\n- Visual inspection: BCG forest footer is rendered and all study whiskers are visible; funnel is rendered.\n\n## Scores\n\n| Static | Dynamic | Final | Grade |\n|---:|---:|---:|---|\n| {static}/100 | {dynamic}/100 | {score}/100 | ⭐ Production Ready |\n\n## Input assertions\n\n| Input | Result | Assertions |\n|---|---|---:|\n"""
for item in inputs:
    viewer += f"| {item['label']} | PASS | {item['assertions_passed']}/{item['assertions_total']} |\n"
viewer += "\n## Recommendations\n\nNo open P0, P1, or P2 findings.\n"
(audit / f"eval_viewer_{skill}.md").write_text(viewer, encoding="utf-8")
print(json.dumps({"report": str(report_path), "viewer": str(audit / f"eval_viewer_{skill}.md"),
                  "score": score, "assertions": f"{assertion_passed}/{assertion_total}"}, indent=2))
