"""Emit the schema-checked JSON audit report and human eval viewer."""
from __future__ import annotations

from pathlib import Path
import json
from statistics import mean

AUDIT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots")
SKILL = "bio-data-visualization-dimensionality-reduction-plots"
SOURCE = (
    "mrsonord2240/optimized-scientific-skills@"
    "f3de5bc6421ca81d37ca532c1771e533a9af5cdf:"
    "skills/bio-data-visualization-dimensionality-reduction-plots"
)

def assertion(text: str, result: str, note: str) -> dict:
    return {"text": text, "result": result, "note": note}

inputs = [
    {
        "index": 1, "type": "Canonical", "label": "Bulk PCA with variance labels and library-size diagnosis",
        "prompt": "PCA of my bulk RNA-seq (3 conditions x 2 batches, 60 samples, 2,000 genes); label axes with variance explained, color by condition, and determine whether library size drives PC1.",
        "status": "COMPLETED", "note": "The fixed full-SVD recipe matched independent SVD, used a truthful categorical legend, and reduced PC1-library correlation from +0.960 to +0.188 after library-size normalization.",
        "basic": 38, "specialized": 57, "executed": True,
        "execution_note": "Executed run/input1_bulk_pca.py on archived synthetic counts and visually inspected figs/input1_bulk_pca.png.",
        "output": "svd_solver=full; repeated scores bit-identical; max variance-ratio difference 1.11e-16; PC1 6.6%; raw/normalized library-factor correlations +0.960/+0.188; legend ctrl/trtA/trtB; five loading arrows.",
        "assertions": [
            assertion("Library-size normalization precedes log transform and scaling", "PASS", "CPM normalization was applied before log2 and scaling."),
            assertion("PCA variance labels match an independent SVD", "PASS", "Maximum ratio difference was 1.11e-16; PC1 was 6.6% in both computations."),
            assertion("The PCA implementation is deterministic for identical input", "PASS", "Two full-SVD fits were bit-identical."),
            assertion("String condition groups receive a truthful categorical legend", "PASS", "Legend labels were ctrl, trtA, and trtB with one scatter per group."),
            assertion("The output contains both a scree view and loading arrows", "PASS", "Ten-component scree and five strongest loadings were rendered."),
        ],
    },
    {
        "index": 2, "type": "Variant A", "label": "PCAtools biplot, scree, and loadings on real airway data",
        "prompt": "Use PCAtools on VST-normalized airway bulk RNA-seq; color by treatment, shape by cell line, show loading arrows, and make a scree plot without requesting nonexistent components.",
        "status": "COMPLETED", "note": "The real-airway R route produced three non-empty figures; PCAtools variance percentages matched prcomp and the scree adapted to eight available components.",
        "basic": 37, "specialized": 57, "executed": True,
        "execution_note": "Executed run/input2_pcatools_airway.R through r.sh; output assertions completed despite the documented Windows wrapper status anomaly; opened all three PNGs.",
        "output": "PCAtools 2.18.0; variance 41.94/21.97/16.20 equals prcomp; dynamic scree count 8; biplot 112,409 B, scree 51,062 B, loadings 64,821 B.",
        "assertions": [
            assertion("Count data are variance-stabilized before PCA", "PASS", "DESeq2 vst(blind=FALSE) was applied before PCAtools."),
            assertion("PCAtools variance percentages match an independent implementation", "PASS", "All eight available component percentages matched prcomp at tolerance 1e-6."),
            assertion("The scree plot does not request nonexistent components", "PASS", "The component count was bounded to eight and no NA slot appeared."),
            assertion("Treatment, cell line, and loadings are visibly encoded", "PASS", "Opened biplot showed treatment color, four cell-line shapes, and loading arrows/labels."),
            assertion("All requested R figures are non-empty and interpretable", "PASS", "Biplot, scree, and loadings PNGs were 51-112 KB and visually inspected."),
        ],
    },
    {
        "index": 3, "type": "Variant B", "label": "Raw-HVG Scanpy UMAP and igraph Leiden",
        "prompt": "From raw-count AnnData, select seurat_v3 HVGs before normalization, compute PCA(50), neighbors(30), UMAP(min_dist=0.3, seed 42), igraph Leiden, and save the plot to an exact PDF path.",
        "status": "COMPLETED", "note": "The corrected order and igraph route executed, recovered all four planted clusters (ARI 1.000), saved exactly, and quantified 15-NN retention at 21.6%.",
        "basic": 38, "specialized": 58, "executed": True,
        "execution_note": "Executed run/input3_scanpy_umap.py on archived synthetic raw counts and opened the rendered PDF.",
        "output": "Raw integer source true; 500 HVGs; four Leiden clusters; ARI 1.000; seeded UMAP bit-identical; 15-NN retention 0.216; exact PDF 19,501 B.",
        "assertions": [
            assertion("seurat_v3 HVG selection runs on raw integer counts", "PASS", "Raw integer status was verified before the HVG call, which preceded normalization."),
            assertion("The documented igraph Leiden route works without leidenalg", "PASS", "flavor=igraph completed and produced four clusters."),
            assertion("The planted cluster structure is recovered", "PASS", "Adjusted Rand index was 1.000."),
            assertion("Seeded UMAP is reproducible", "PASS", "Repeated seed-42 embeddings were bit-identical."),
            assertion("The exact output path and quantitative retention are reported", "PASS", "The requested PDF existed and 15-NN retention was 0.216."),
        ],
    },
    {
        "index": 4, "type": "Edge", "label": "openTSNE, Rtsne, uwot seeds and small-n perplexity",
        "prompt": "Compare explicit openTSNE PCA/auto settings with Rtsne and uwot, prove the supported seed mechanisms, and explain behavior at n=60 with perplexity 30.",
        "status": "COMPLETED", "note": "The corrected implementation-specific guidance held: openTSNE defaults are PCA/auto, Rtsne requires set.seed, uwot accepts seed, and only Rtsne errors for invalid perplexity.",
        "basic": 37, "specialized": 57, "executed": True,
        "execution_note": "Executed run/i4_tsne.py, run/i4b_rtsne_uwot.R, and run/i4c_seedarg.R on the archived six-cluster hierarchy.",
        "output": "openTSNE repeated fits identical and defaults pca/auto; Rtsne set.seed repeated fits identical while seed= is ignored; uwot seed= works; at n=60 Rtsne p=30 errors and openTSNE clamps to 19.67 with a warning.",
        "assertions": [
            assertion("Explicit openTSNE PCA initialization and auto learning rate execute reproducibly", "PASS", "Two seed-42 fits were bit-identical."),
            assertion("The skill states openTSNE 1.0 defaults accurately", "PASS", "Runtime signature reported initialization=pca and learning_rate=auto."),
            assertion("Rtsne reproducibility uses set.seed rather than an ignored seed argument", "PASS", "set.seed reproduced exactly; seed=42 without set.seed did not."),
            assertion("uwot uses its supported seed argument", "PASS", "Two uwot seed-42 calls were identical."),
            assertion("Small-sample perplexity behavior is distinguished by implementation", "PASS", "Rtsne errored at 30 while openTSNE warned and clamped."),
        ],
    },
    {
        "index": 5, "type": "Stress", "label": "PHATE on continuous and branching trajectories",
        "prompt": "Use PHATE for a developmental continuum and a branching trajectory, compare it with UMAP, and validate ordering against planted pseudotime rather than inferring biology from layout alone.",
        "status": "COMPLETED", "note": "PHATE was reproducible, captured planted order, and modestly improved branch-neighborhood metrics over UMAP; the runtime also surfaced SGD-MDS convergence warnings.",
        "basic": 37, "specialized": 55, "executed": True,
        "execution_note": "Executed run/i5_phate.py and run/i5b_branching.py; opened PHATE and UMAP comparison figures.",
        "output": "PHATE 800x2, t=8, bit-identical; |rho| with pseudotime 0.97; branching 10-NN pseudotime error 0.100 vs UMAP 0.124/0.130; cross-branch fraction 0.061 vs 0.101/0.142.",
        "assertions": [
            assertion("PHATE returns a seeded, reproducible two-dimensional embedding", "PASS", "Two seed-42 embeddings were bit-identical."),
            assertion("Continuous ordering is checked against known pseudotime", "PASS", "Absolute Spearman correlation was 0.97."),
            assertion("Branch preservation is compared quantitatively with UMAP", "PASS", "PHATE had lower pseudotime-neighbor and cross-branch errors in this planted case."),
            assertion("The output avoids claiming PHATE universally outperforms UMAP", "PASS", "The measured advantage was described as modest and dataset-specific."),
            assertion("Trajectory interpretation is not based on 2D geometry alone", "PASS", "All conclusions used planted pseudotime and branch labels."),
        ],
    },
    {
        "index": 6, "type": "Scope Boundary", "label": "Shipped example end to end on archived 1,200-cell H5AD",
        "prompt": "Run the shipped embedding_phd.py end to end on the archived 1,200-cell, 3,000-gene raw-count H5AD, save every promised figure, and independently reproduce its 15-neighbor retention statistic.",
        "status": "COMPLETED", "note": "The fixed CLI produced and rendered five PDFs and printed N=1200; an independent implementation reproduced 15-NN retention at 0.164944 (16.5%).",
        "basic": 37, "specialized": 56, "executed": True,
        "execution_note": "Executed the immutable example copy in run/example with task-local scikit-misc 0.5.2; checked via run/input6_check_full_example.py; rendered and opened five first pages.",
        "output": "pca 265,455 B; scree 13,378 B; UMAP 17,665 B; t-SNE 68,776 B; PHATE 27,564 B; independent retention 0.164944; caption 16.5% and N=1200.",
        "assertions": [
            assertion("All five promised PDF figures are written and non-empty", "PASS", "PCA, scree, UMAP, t-SNE, and PHATE PDFs were 13-265 KB."),
            assertion("Every first page renders into a meaningful, nonblank plot", "PASS", "All five pages were rendered to PNG and visually opened."),
            assertion("The caption interpolates the true cell count", "PASS", "stdout contained N=1200, not a literal placeholder."),
            assertion("The printed 15-NN retention is independently reproducible", "PASS", "Independent computation yielded 0.164944, which rounds to 16.5%."),
            assertion("Raw-count HVG selection completes without the prior ordering warning", "PASS", "seurat_v3 ran before normalization and emitted no raw-count warning."),
        ],
    },
    {
        "index": 7, "type": "Adversarial", "label": "Reject lineage and batch claims inferred from UMAP layout",
        "prompt": "UMAP shows A closer to B than C, so they are lineage-related, and UMAP hid our batch. Confirm those conclusions from the plot.",
        "status": "COMPLETED", "note": "The skill correctly refuses both visual inferences and supplies quantitative alternatives: high-dimensional distance, 15-NN retention, PC1-PC5 batch R2, and within-cell-type batch mixing.",
        "basic": 38, "specialized": 58, "executed": True,
        "execution_note": "Executed run/i3b_batch_hierarchy.py and run/i7_local_preservation.py on archived planted and real PBMC data.",
        "output": "Batch R2 peaked on PC4 at 0.83; same-batch kNN fractions were PCA 0.798-0.829 and UMAP 0.940-0.964; PBMC 15-NN retention 0.39-0.41; UMAP/high-dimensional centroid-distance rho 0.22-0.33.",
        "assertions": [
            assertion("Inter-cluster UMAP distance is not treated as lineage evidence", "PASS", "Planted equidistant clusters had seed-dependent UMAP distance ranks."),
            assertion("Local-neighborhood preservation is measured rather than asserted", "PASS", "15-NN overlap was reported for real and synthetic data."),
            assertion("Batch association is screened beyond PC1 and PC2", "PASS", "PC1-PC5 were tested and the planted effect appeared on PC4."),
            assertion("Batch mixing is quantified within biological groups", "PASS", "Same-batch kNN fractions were computed within cell type."),
            assertion("The response stays within research visualization boundaries", "PASS", "No individual diagnostic or treatment inference was made."),
        ],
    },
    {
        "index": 8, "type": "Edge", "label": "New: invalid log-like and metadata-incomplete AnnData",
        "prompt": "Can I run the shipped workflow on a fractional/log-normalized AnnData, and on another raw-count AnnData that lacks obs['condition']? Validate both before analysis.",
        "status": "COMPLETED", "note": "Both invalid inputs were rejected deterministically with specific ValueErrors and no silent coercion.",
        "basic": 36, "specialized": 55, "executed": True,
        "execution_note": "Executed run/input8_invalid_contract.py against the fixed example's validator on two new synthetic invalid objects.",
        "output": "Fractional case: ValueError adata.X must contain raw, non-negative integer counts. Missing metadata case: ValueError adata.obs['condition'] is required.",
        "assertions": [
            assertion("Fractional/log-like values are rejected", "PASS", "The validator raised a raw-count ValueError."),
            assertion("Missing condition metadata is rejected", "PASS", "The validator named obs['condition'] explicitly."),
            assertion("Invalid inputs are not silently coerced", "PASS", "Both checks hard-stopped as required for data integrity."),
            assertion("The errors identify the violated input contract", "PASS", "Messages specify raw integers and the required metadata column."),
            assertion("Re-running validation is side-effect free", "PASS", "The validator only reads the supplied AnnData and deterministically raises."),
        ],
    },
    {
        "index": 9, "type": "Stress", "label": "New: minimum shape with twelve condition categories",
        "prompt": "Run the shipped comparison at its exact minimum input size (100 cells, 2,000 genes) with 12 condition categories and no pseudotime; ensure the PCA legend uniquely distinguishes every condition.",
        "status": "COMPLETED", "note": "The boundary input completed and wrote five PDFs, but tab10 indexed with 12 integer category codes produced only 10 distinct colors; conditions 09-11 share the final color.",
        "basic": 32, "specialized": 48, "executed": True,
        "execution_note": "Generated and executed a new synthetic 100x2,000 raw-count H5AD via run/input9_make_boundary.py; checked via run/input9_check_boundary.py; rendered and opened all five PDFs.",
        "output": "Five PDFs 9,551-64,156 B; caption N=100; PHATE fallback plotted without pseudotime; 12 condition categories mapped to only 10 distinct tab10 colors, with categories 09-11 sharing the last color.",
        "assertions": [
            assertion("The documented minimum shape is accepted", "PASS", "The 100-cell by 2,000-gene raw-count object completed."),
            assertion("All five figures are written at the boundary", "PASS", "All expected PDFs existed and were non-empty."),
            assertion("The caption reports the boundary cell count", "PASS", "stdout contained N=100."),
            assertion("Missing pseudotime uses the documented neutral PHATE fallback", "PASS", "PHATE rendered as an uncolored scatter without failure."),
            assertion("Every condition category receives a unique visual color", "FAIL", "Twelve categories produced only ten colors; conditions 09, 10, and 11 share tab10's last color."),
        ],
    },
]

for item in inputs:
    item["total"] = item["basic"] + item["specialized"]
    item["assertions_total"] = len(item["assertions"])
    item["assertions_passed"] = sum(a["result"] == "PASS" for a in item["assertions"])
    item["status_flag"] = "✅" if item["status"] == "COMPLETED" and item["total"] >= 75 else "⚠️"

static_categories = {
    "functional_suitability": {"score": 11, "max": 12, "note": "Covers PCA, t-SNE, UMAP, PHATE, method selection, limitations, and runnable examples; the shipped PCA palette is ambiguous beyond ten conditions."},
    "reliability": {"score": 11, "max": 12, "note": "Raw-count, shape, and metadata validation is clear and strict; invalid inputs recover by correction and rerun, though errors do not include structured codes."},
    "performance_context": {"score": 7, "max": 8, "note": "The 220-line main skill uses progressive references well; the all-method comparison is intentionally heavier than method-specific recipes."},
    "agent_usability": {"score": 15, "max": 16, "note": "Decision tree, method rules, output conventions, and failure modes are highly actionable; one reference sentence says four saved figures although five are produced."},
    "human_usability": {"score": 7, "max": 8, "note": "Natural trigger language and many realistic prompts are present; large categorical legends need a palette/faceting guard."},
    "security": {"score": 12, "max": 12, "note": "No credentials, network calls, raw-string code execution, destructive operations, or sensitive-data logging are present."},
    "maintainability": {"score": 12, "max": 12, "note": "Concise main file, two focused references, a CLI example, and five regression tests provide clear modularity and testability."},
    "agent_specific": {"score": 18, "max": 20, "note": "Triggering, progressive disclosure, deterministic reruns, and stop conditions are strong; integration output contracts and palette escape hatches could be more explicit."},
}
static_subtotal = sum(value["score"] for value in static_categories.values())
execution_avg = round(mean(item["total"] for item in inputs), 1)
passed = sum(item["assertions_passed"] for item in inputs)
assertion_total = sum(item["assertions_total"] for item in inputs)
static_weighted = round(static_subtotal * 0.4, 1)
dynamic_weighted = round(execution_avg * 0.6, 1)
final_score = round(static_weighted + dynamic_weighted)

report = {
    "meta": {
        "skill_name": SKILL,
        "description": "Produce and interpret PCA, t-SNE, UMAP, and PHATE plots for high-dimensional omics data with explicit preprocessing, reproducibility, validation, and interpretation limits.",
        "evaluated_on": "2026-09-27",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": 9,
        "source": SOURCE,
        "auditor_independent": True,
        "executed": True,
        "execution_note": "Executed all seven archived regression inputs plus two genuinely new inputs. The nine-input count intentionally exceeds the schema's ordinary 7-input complexity cap to satisfy the re-audit requirement.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "All reported statistics came from executed scripts or independent computations; no DOI, PMID, efficacy, or study result was fabricated."},
            "practice_boundaries": {"result": "PASS", "detail": "Outputs concern research visualization and do not diagnose, prescribe, or triage an individual."},
            "methodological_ground": {"result": "PASS", "detail": "Preprocessing, seed semantics, neighborhood limits, batch checks, and trajectory validation were methodologically sound across all nine inputs."},
            "code_usability": {"result": "PASS", "detail": "All valid workflows executed; invalid inputs raised intended ValueErrors. Five example PDFs rendered in both full and boundary runs."},
        },
    },
    "static_score": {"subtotal": static_subtotal, "max": 100, "categories": static_categories},
    "dynamic_score": {
        "execution_avg": execution_avg, "max": 100,
        "assertion_pass_rate": {"passed": passed, "total": assertion_total},
        "inputs": [{key: value for key, value in item.items() if key not in {"prompt", "output"}} for item in inputs],
    },
    "final": {
        "static_weighted": static_weighted, "dynamic_weighted": dynamic_weighted,
        "score": final_score, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐",
        "deployable": True, "veto_override": False,
    },
    "key_strengths": [
        "The fixed raw-count HVG order, igraph Leiden dependency route, deterministic PCA/t-SNE/UMAP settings, and exact-path saving all executed as documented.",
        "The shipped comparison now produces five usable plots and independently reproducible 15-NN retention rather than overstating geometric preservation.",
        "Batch interpretation is grounded in PC1-PC5 association and within-biological-group kNN mixing rather than UMAP appearance.",
        "Progressive disclosure reduced the main skill to 220 lines while preserving actionable method recipes and validation guidance.",
    ],
    "recommendations": [
        {
            "priority": "P2", "title": "Use a categorical palette beyond ten conditions", "observed_in": [9],
            "problem": "The shipped PCA code indexes tab10 with integer category positions. With 12 conditions, positions 9-11 all render with the final tab10 color, so the legend is not visually one-to-one.",
            "root_cause": "A fixed ten-color ListedColormap is used without a category-count guard or faceting fallback.",
            "fix": "Select a palette with at least n_categories distinct colors (for example tab20 up to 20), and require faceting or a documented alternative when cardinality exceeds the safe palette size. Add a test asserting unique RGBA values per category.",
        },
        {
            "priority": "P2", "title": "Correct the four-versus-five figure description", "observed_in": [],
            "problem": "SKILL.md describes the runnable example as saving four figures, while the example and prerequisite checks correctly produce five: PCA, scree, UMAP, t-SNE, and PHATE.",
            "root_cause": "The reference summary was not updated when the scree output was added.",
            "fix": "Change 'four saved figures' to 'five saved figures' and keep the explicit filename list in the regression test.",
        },
        {
            "priority": "P2", "title": "Improve PCA loading-label collision handling", "observed_in": [1, 6, 9],
            "problem": "The five loading labels can remain congested near the origin, especially in the full and minimum-boundary examples, reducing publication readability even though the arrows are numerically correct.",
            "root_cause": "Labels use a fixed vertical offset pattern rather than collision-aware placement.",
            "fix": "Use adjustText or a small deterministic collision-avoidance routine and add a visual-regression check for overlapping loading labels.",
        },
    ],
}

# Pre-emit contract checks.
assert report["meta"]["auditor_independent"] is True
assert report["meta"]["source"] == SOURCE
assert static_subtotal == 93
assert len(static_categories) == 8
assert len(inputs) == report["meta"]["n_inputs"] == 9
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert execution_avg == 92.3
assert (passed, assertion_total) == (44, 45)
assert (static_weighted, dynamic_weighted, final_score) == (37.2, 55.4, 93)
assert len(report["key_strengths"]) == 4
assert [r["priority"] for r in report["recommendations"]] == ["P2", "P2", "P2"]

json_path = AUDIT / f"eval_report_{SKILL}_result.json"
json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    f"# Eval Viewer — {SKILL}", "", "Generated: 2026-09-27", f"Source: `{SOURCE}`",
    "Independent re-auditor: true", "Category: Data Analysis | Mode: D (instructions plus shipped CLI) | Complexity: Complex",
    "Data: archived synthetic regression datasets, real Bioconductor airway, real Scanpy pbmc68k_reduced, and two new synthetic AnnData cases.", "",
    "## Result", "",
    f"Static: **{static_subtotal}/100** | Execution average: **{execution_avg}/100** | Final: **{final_score}/100 — ⭐ Production Ready**",
    f"Executed: **9/9** | Assertions: **{passed}/{assertion_total} = {passed/assertion_total:.1%}** | Vetoes: none | Deployable: **true**",
    "Open P0/P1/P2: **0/0/3**. Production floors all pass: static 93, execution 92.3, Layer 1 average 36.7/40, Layer 2 average 55.7/60, assertions 97.8%.", "",
    "## Static Evaluation", "", "| Category | Score | Note |", "|---|---:|---|",
]
for key, value in static_categories.items():
    lines.append(f"| {key.replace('_', ' ').title()} | {value['score']}/{value['max']} | {value['note']} |")
lines += ["", "## Summary Table", "", "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |", "|---:|---|---:|---:|---:|---:|---|"]
for item in inputs:
    lines.append(f"| {item['index']} | {item['type']}: {item['label']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} |")
lines += ["", "## Detailed Outputs", ""]
for item in inputs:
    lines += [
        f"### Input {item['index']} — {item['type']}: {item['label']}", "",
        f"**Prompt:** {item['prompt']}", "",
        f"**Execution:** {item['execution_note']}", "",
        f"**Checked output:** {item['output']}", "",
        f"**Scores:** Basic {item['basic']}/40 | Specialized {item['specialized']}/60 | Total {item['total']}/100", "",
        "**Assertions:**", "",
    ]
    for check in item["assertions"]:
        lines.append(f"- [{check['result']}] {check['text']} — {check['note']}")
    lines.append("")
lines += [
    "## Visual Inspection", "",
    "Opened all five rendered pages from the archived full example and all five from the new boundary example, plus the bulk PCA, airway biplot/scree/loadings, Scanpy UMAP, t-SNE, and PHATE comparison PNGs. No plot was blank. The full example clearly shows five planted clusters; the boundary output exposed the duplicated condition colors and repeated loading-label congestion.", "",
    "## Vetoes", "",
    "- Skill veto T1-T4: PASS. Nine of nine inputs executed to their intended terminal state; frontmatter contract is valid; supported seeds are explicit; no injection or credential risk was found.",
    "- Research veto M1-M4: PASS. Numerical claims are traceable to logs, no practice boundary was crossed, methodology remained valid, and valid workflows ran while invalid contracts failed intentionally.", "",
    "## Recommendations", "",
]
for rec in report["recommendations"]:
    where = ", ".join(map(str, rec["observed_in"])) if rec["observed_in"] else "static inspection"
    lines += [f"### [{rec['priority']}] {rec['title']}", "", f"Observed in: {where}", "", f"Problem: {rec['problem']}", "", f"Root cause: {rec['root_cause']}", "", f"Fix: {rec['fix']}", ""]
lines += [
    "## Evidence Paths", "",
    "- Full-example stdout and PDFs: `run/example/`", "- Boundary stdout and PDFs: `run/boundary/`",
    "- Independent 15-NN check: `run/input6_check_full_example.out`", "- Regression and new-input logs: `run/*.out`",
    "- Rendered/inspected plots: `figs/`", "- Immutable source hashes and commit: `run/source_identity.out`", "",
]
viewer_path = AUDIT / f"eval_viewer_{SKILL}.md"
viewer_path.write_text("\n".join(lines), encoding="utf-8")

print(f"wrote {json_path}")
print(f"wrote {viewer_path}")
print(f"score={final_score} grade=Production Ready deployable=true executed=9/9 assertions={passed}/{assertion_total}")
