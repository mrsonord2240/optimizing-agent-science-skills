"""Build report.json, findings.json, source-identity.json, execution-classifications.json, viewer.md, candidate-manifest.tsv
for the independent final re-audit of bio-atac-seq-co-accessibility (fixed candidate 0aac567b...)."""
import hashlib, json, os

R = r'F:\OpenScience\audits\bio-atac-seq-co-accessibility\reaudit-run'
root = r'F:\OpenScience\wt\atac-co-accessibility\skills\bio-atac-seq-co-accessibility'
SKILL = 'bio-atac-seq-co-accessibility'
EXPECT = '0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa'

rows = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f)
        b = open(p, 'rb').read().replace(b'\r\n', b'\n')
        rows.append((os.path.relpath(p, root).replace(chr(92), '/'), len(b), hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda x: x[0].encode())
man = "\n".join(f"{a}\t{b}\t{c}" for a, b, c in rows).encode()
ident = hashlib.sha256(man).hexdigest()
assert ident == EXPECT, ident
open(os.path.join(R, 'candidate-manifest.tsv'), 'wb').write(man)

sid = {
    "schema": "scientific-skill-audit-source-identity-v1", "phase": "final re-audit", "skill_id": SKILL,
    "independent_auditor": True,
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
               "path": "atac-seq/co-accessibility", "license": "MIT"},
    "candidate": {
        "root": root, "worktree": r"F:\OpenScience\wt\atac-co-accessibility", "branch": "fix/atac-co-accessibility",
        "product_head": "3186916406e9cc6b0e6dc24ffe47880951fc0f93", "identity_scheme": "sha256-manifest-v1",
        "content_sha256": ident, "manifest_bytes": len(man), "file_count": len(rows),
        "manifest_recipe": "Ordinal POSIX relative paths; each UTF-8 line is path, TAB, byte count, TAB, lowercase file SHA-256 of the CRLF->LF normalized bytes; lines joined by LF without a trailing LF; SHA-256 over the manifest bytes.",
        "manifest_path": "candidate-manifest.tsv", "identity_before": ident, "identity_after": ident,
        "prior_audit_identity": "3c8089b0496fa6375512ece4b85ce85c10c47f3cb4a9c8e48c7288a62b9162e3",
        "tree_status": "Candidate skill directory is staged/modified (uncommitted) in the worktree; identity recomputed live before and after this re-audit; no candidate bytes modified."},
    "tooling": {"tools_md": r"F:\OpenScience\audits\bio-atac-seq-co-accessibility\TOOLS.md",
                "environment_lock_sha256": "2fcd3fc2a5de3bd194b80bf864b2f7ce9762eafc45c35179df9713958db7d552",
                "environment_live_check": "conda-list sha256 recomputed live and equal; cicero 1.3.9, monocle3 1.3.1, ArchR 1.0.3, Signac 1.17.1, R 4.4.3 (logs/env_live.log)"},
    "rubric": {"zip": r"F:\optimizing-agent-science-skills\skill-auditor.zip", "evaluator_version": "skill-auditor@1.0"},
    "files": [{"path": a, "bytes": b, "sha256": c} for a, b, c in rows]}
json.dump(sid, open(os.path.join(R, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)


def A(t, ok, n):
    return {"text": t, "result": "PASS" if ok else "FAIL", "note": n}


inputs = [
    dict(index=1, type="Canonical", label="Shipped CLI on real 3-chromosome PBMC Multiome ATAC slice (766 peaks x 2,701 cells, pattern-format .mtx) with 4th-arg TSS BED",
         status="COMPLETED", note="exit 0 in 5.2 min; 1,121 strong pairs, 287 enhancer-gene rows; all independent checks pass", basic=36, specialized=55,
         assertions=[A("CLI exits 0 on a pattern-format binary .mtx and writes the connections TSV and enhancer-gene CSV (COACC-001)", True, "exit 0; cicero_connections.tsv 1,121 rows, CSV 287 rows"),
                     A("Strong table has one row per unordered pair, scores in (0.25,1], anchors are input peak names, no cross-chromosome pairs, span within the 500 kb window (COACC-005/007)", True, "score 0.250-0.915; max span 498,991; chr1 255 / chr19 832 / chr2 34"),
                     A("enhancer column holds peak names and the set of enhancer-gene pairs equals an independent recomputation from the BED (COACC-002/009)", True, "independent 287 vs csv 287; no integer codes; no duplicates"),
                     A("enhancer_is_promoter flag equals an independent TSS-window overlap of the enhancer peak", True, "157 TRUE of 287"),
                     A("Multi-chromosome input runs through the peak-derived genome_df without cross-chromosome scoring (COACC-003)", True, "3 chromosomes scored; 0 cross-chromosome pairs")]),
    dict(index=2, type="Variant A", label="run_cicero_pipeline API: window=1e6 (multi-chromosome), tss_bed=NULL branch, seed reproducibility",
         status="COMPLETED", note="window=1e6 run 6.2 min; NULL-TSS and repeat runs byte-identical (sha256 72bec6f9...)", basic=35, specialized=52,
         assertions=[A("window=1e6 scores pairs beyond 500 kb and stays within the window measured end-to-start (COACC-006)", True, "15,077 scored pairs >500 kb; max gap 998,051 (start-to-start 1,010,898 is inside one peak width, peaks reach 67 kb)"),
                     A("No cross-chromosome pairs and all three chromosomes scored at window=1e6", True, "16,481 / 33,793 / 853 pairs"),
                     A("tss_bed=NULL prints the skip message and writes only the connections TSV", True, "no enhancer-gene file written; message seen"),
                     A("Same seed and input give an identical strong table across three fresh processes (tss on, tss off, repeat)", True, "sha256 72bec6f9f675... identical, 78 rows"),
                     A("Scored-pair count is reported as unordered pairs with negatives counted", True, "51,127 scored (11,599 negative)")]),
    dict(index=3, type="Variant B", label="ArchR addCoAccessibility/getCoAccessibility as documented on public PBMC 5k chr1 slice",
         status="COMPLETED", note="documented calls run verbatim; SimpleList wording verified", basic=34, specialized=50,
         assertions=[A("addCoAccessibility(k=100, knnIteration=500, maxDist=250000) completes on 835 cells / 1,876 peaks", True, "4,462 loops"),
                     A("getCoAccessibility(returnLoops=TRUE) returns a SimpleList whose element 1 is a GRanges (COACC-010)", True, "class SimpleList / GRanges"),
                     A("returnLoops=FALSE returns a DataFrame of correlations within [0.5,1] respecting maxDist", True, "8,924 rows; 0.50-0.96; max distance 249,998 bp"),
                     A("Route is executed only where code ran (no claim for routes not run)", True, "SKILL.md labels ArchR executed on a PBMC chr1 slice")]),
    dict(index=4, type="Edge", label="Synthetic planted-truth dataset (60 peaks, 4 latent states, 4 co-varying peak groups) plus a threshold that leaves zero strong pairs",
         status="COMPLETED", note="planted structure recovered exactly; empty strong set handled", basic=37, specialized=55,
         assertions=[A("Within-group planted pairs are strong", True, "1.00 of 60"),
                     A("Cross-group and independent background pairs are not strong", True, "0.00 of 216 cross-group; 0.02 of 608 background"),
                     A("Cross-group scores are negative or low relative to within-group (negatives retained, range -1..1) (COACC-007)", True, "mean -0.29 vs 0.89; observed min -0.48, max 0.96"),
                     A("Threshold 0.999 (no strong pairs) with a TSS BED completes without crashing and writes header-only outputs", True, "pl_connections.tsv 0 rows; exit 0"),
                     A("Two identical seeds reproduce the connections table byte for byte", True, "sha256 equal across runs")]),
    dict(index=5, type="Stress", label="Shipped CLI on the larger real PBMC 5k chr1:1-30 Mb slice (1,726 peaks x 3,277 cells, pattern .mtx)",
         status="COMPLETED", note="exit 0 in 5.2 min (documented 8.5-14 min, load dependent); 6,035 strong / 2,027 enhancer-gene", basic=34, specialized=52,
         assertions=[A("CLI completes within the documented runtime range on the larger slice", True, "5.2 min, exit 0"),
                     A("All structural invariants hold (unique unordered pairs, scores, window, peak names)", True, "score 0.250-0.927; max span 498,272"),
                     A("Enhancer-gene set equals independent recomputation and promoter flag matches", True, "2,027 vs 2,027; 493 promoter-promoter"),
                     A("Counts match the fix worker's earlier run (deterministic result)", True, "6,035 / 2,027 identical")]),
    dict(index=6, type="Scope Boundary", label="Downstream doc snippets on the CLI output: locus arc plot (>0.5) and Hi-C concordance against a planted BEDPE",
         status="COMPLETED", note="arc plot readable; concordance snippet matches independent expectation", basic=34, specialized=52,
         assertions=[A("Visualizing Connections snippet runs verbatim (locus, GenomeAxisTrack, >0.5 filter) and renders a readable arc figure (COACC-008)", True, "1400x500 png inspected: axis, 21 arcs anchored in window, no hairball"),
                     A("Hi-C concordance snippet count equals an independent orientation-agnostic overlap count on a planted BEDPE (30 real + 30 decoy loops)", True, "46 vs 46 (4.1%)"),
                     A("Snippet is unaffected by lexicographic Peak1<Peak2 ordering (GenomicInteractions normalizes anchors)", True, "6 supported pairs had Peak1 genomically downstream; 0 missed"),
                     A("Unsourced concordance bands are labelled as heuristics, not benchmarks (COACC-011)", True, "method-reference.md states 'unsourced heuristics, not benchmarks'")]),
    dict(index=7, type="Adversarial", label="Failure guards: dimension mismatch, colon-format peak names, missing TSS BED, BED without gene column, and a cell with zero reads",
         status="COMPLETED", note="four early clear guards (0.4 s); zero-read cell halts with a cryptic monocle3 error", basic=33, specialized=45,
         assertions=[A("Dimension mismatch is rejected before any long computation", True, "stopifnot(nrow == nrow)"),
                     A("chr:start-end peak names are rejected with the chr_start_end contract in the message (COACC-009)", True, "message names the required format"),
                     A("Missing or gene-less TSS BED is rejected before the long run with a specific message", True, "'tss_bed not found' / 'needs the gene name in column 4'; all guards 0.4 s"),
                     A("Peak names, TSS and matrix guard failures do not write partial outputs or report success", True, "no output files created"),
                     A("A zero-read cell halts with an actionable message naming the cause (COACC-014)", False, "error is 'attempt to set an attribute on NULL'; only monocle3's warning names the remedy")]),
]
for i in inputs:
    i["status_flag"] = "\u2705" if i["basic"] + i["specialized"] >= 75 else "\u26a0\ufe0f"
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"]); i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
passed = sum(i["assertions_passed"] for i in inputs); total = sum(i["assertions_total"] for i in inputs)
cats = {
    "functional_suitability": (10, 12, "Cicero, ArchR, planted-truth recovery, multi-chromosome and downstream snippets all work; LinkPeaks, Hi-C, SCENIC+ and reference databases remain prose or unshipped, honestly labelled"),
    "reliability": (9, 12, "Early guards, seed, empty-set handling and deterministic output; a zero-read cell halts with a cryptic error (COACC-014); whole-genome run untested"),
    "performance_context": (7, 8, "51-line SKILL.md with routed references; runtime scaling is documented for the chr1 case only"),
    "agent_usability": (14, 16, "Clear tool selection table with per-route execution status; version guidance now consistent; one usage-guide prompt contradicts the TSS window (COACC-015)"),
    "human_usability": (6, 8, "Readable tables and status column; inputs need strict formats with limited recovery guidance"),
    "security": (11, 12, "No credentials or string execution; file arguments unchecked beyond existence"),
    "maintainability": (9, 12, "Single script mixes CLI and pipeline but is now versioned, commented and internally consistent; no tests shipped"),
    "agent_specific": (16, 20, "Precise trigger description and progressive disclosure; SCENIC+ route static-only and stated as such"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = int(round(sw + dw))
report = {
    "meta": {"skill_name": SKILL,
             "description": "Infer cis-regulatory connections (peak-to-peak co-accessibility) from scATAC-seq using Cicero, ArchR getCoAccessibility, or SCENIC+, and map them to enhancer-gene candidates.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "D", "complexity": "Complex", "n_inputs": 7},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {"applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; planted truth recovered and independent recomputations match; unsourced ranges are labelled as heuristics"},
            "practice_boundaries": {"result": "PASS", "detail": "Research analysis guidance; no clinical claims"},
            "methodological_ground": {"result": "PASS", "detail": "Co-accessibility framed as a hypothesis generator, not 3D contact; SCENIC+ stated as not executed"},
            "code_usability": {"result": "PASS", "detail": "CLI and function ran on pattern .mtx, multi-chromosome and larger slices; the zero-read failure is loud, not silent (COACC-014)"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
              "grade": "Production Ready" if score >= 85 else "Limited Release", "grade_symbol": "\u2b50" if score >= 85 else "\u2705",
              "deployable": score >= 85, "veto_override": False},
    "key_strengths": [
        "All prior P1/P2 defects reproduce as fixed on independent real-data runs: pattern .mtx CLI, enhancer names, unordered pairs, window, guards",
        "Planted-truth recovery is exact (within-group 1.00 strong, cross-group 0.00) and outputs are byte-reproducible with the seed",
        "Independent recomputation of the enhancer-gene table matches on both the 3-chromosome and the 30 Mb slices",
        "Honest per-route execution status: SCENIC+ and prose-only routes are labelled as not executed"],
    "recommendations": [
        {"priority": "P2", "title": "Cryptic zero-read halt; conflicting TSS window prompt",
         "observed_in": [7],
         "problem": "A cell with no reads in the peak set stops the CLI with 'attempt to set an attribute on NULL' (only monocle3's warning names the cause), and a usage-guide prompt says tssRegion=c(-2000, 500) while the script and SKILL use TSS +/- 2 kb.",
         "root_cause": "No guard for empty cells in run_cicero_pipeline and one prompt copied from ArchR conventions.",
         "fix": "Fail early with a message naming zero-read cells (or drop them with a count) and align the prompt to TSS +/- 2 kb; not blocking."}],
}
json.dump(report, open(os.path.join(R, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=True)

prior = [
 ("COACC-001", "P1", "fixed", "CLI on a pattern-format .mtx exits 0 (inputs 1, 5)"),
 ("COACC-002", "P1", "fixed", "enhancer column holds peak names; set equals independent recomputation (inputs 1, 5)"),
 ("COACC-003", "P2", "fixed", "genome_df from peaks; 3-chromosome and 30 Mb runs complete in 5-6 min; whole-genome run remains untested (after-action, not a finding)"),
 ("COACC-004", "P2", "fixed", "cicero 1.3.x GitHub monocle3 branch stated consistently in script header, usage-guide, method-reference; live cicero 1.3.9"),
 ("COACC-005", "P2", "fixed", "one row per unordered pair; counts reported as unordered (inputs 1, 2, 5, 6)"),
 ("COACC-006", "P2", "fixed", "window replaces genomic_distance_max; window=1e6 executed (input 2)"),
 ("COACC-007", "P2", "fixed", "range -1..1 with negatives and NA handling verified against observed -0.48..0.96 (input 4)"),
 ("COACC-008", "P2", "fixed", "locus snippet renders a readable arc figure (input 6); arc width is not score-scaled and is not claimed"),
 ("COACC-009", "P2", "fixed", "optional TSS BED, early guards, enhancer_is_promoter flag, peak-name regex (inputs 1, 2, 7)"),
 ("COACC-010", "P3", "fixed", "SimpleList wording verified by running ArchR (input 3)"),
 ("COACC-011", "P3", "fixed", "concordance bands labelled unsourced heuristics; '>50K cells' labelled unverified (static)"),
 ("COACC-012", "P3", "deferred-with-rationale", "SCENIC+ wording corrected and labelled not executed / static review only; restricted-access, not retried"),
 ("COACC-013", "P3", "fixed", "Status column in SKILL.md quick start; LinkPeaks runtime caveat matches the 8 min 23 s / 150 gene tooling log; LinkPeaks not rerun (doc-only change, env fingerprint unchanged)"),
]
F = [dict(id=i, severity=s, state=st, summary=n, evidence="reaudit-run/logs and scripts") for i, s, st, n in prior]
F += [
 dict(id="COACC-014", severity="P2", state="open", surface="scripts/cicero_workflow.R run_cicero_pipeline input validation",
      summary="A cell with zero reads in the peak set halts the pipeline with 'attempt to set an attribute on NULL'",
      evidence="logs/fn_zero.log, scripts/ra_fn.R zero mode",
      detail="Loud, not silent, and monocle3's own warning names the fix. Natural only after subsetting peaks. Not blocking.",
      fix="Check colSums(peak_matrix)==0 before new_cell_data_set and stop (or drop with a count) with a message naming the cells."),
 dict(id="COACC-015", severity="P3", state="open", surface="references/usage-guide.md Quick Start prompt",
      summary="Prompt says tssRegion=c(-2000, 500) while the script and SKILL use TSS +/- 2 kb",
      evidence="usage-guide.md line 30; scripts/cicero_workflow.R tss_pad=2000",
      detail="Copied from ArchR conventions; inconsistent window for the enhancer-gene step.",
      fix="Replace with 'TSS +/- 2 kb (tss_pad)'."),
]
json.dump({"skill_id": SKILL, "candidate_sha256": ident, "findings": F}, open(os.path.join(R, 'findings.json'), 'w', encoding='utf-8'), indent=2)

cls = [
 ("scripts/cicero_workflow.R CLI on pattern .mtx with TSS BED (3-chromosome real slice and 30 Mb real slice)", "executed", "logs/cli.log, logs/stress.log, logs/check_cli.log, logs/check_stress.log"),
 ("run_cicero_pipeline: window=1e6, tss_bed=NULL, seed reproducibility, empty strong set", "executed", "logs/fn_window.log, logs/fn_nulltss.log, logs/fn_a.log; sha256 equality"),
 ("Planted-truth synthetic recovery", "executed", "logs/fn_a.log (synthetic, planted truth 4 groups)"),
 ("Input guards (dimension, peak names, missing/gene-less BED)", "executed", "logs/guards_full.log"),
 ("Zero-read cell input", "failed", "logs/fn_zero.log; COACC-014 (loud, cryptic)"),
 ("Visualizing Connections snippet", "executed", "logs/ra_docs.log; work/reaudit/cli/locus_arcs.png inspected"),
 ("Hi-C concordance snippet (planted BEDPE)", "executed", "logs/ra_docs.log"),
 ("ArchR addCoAccessibility / getCoAccessibility", "executed", "logs/archr.log"),
 ("Cicero alpha block and permutation negative control", "executed", "reused: ../evidence/logs/viz_alpha.log; identity-matched runtime, script unchanged, doc-only edits"),
 ("Signac LinkPeaks (Multiome, 150 genes)", "executed", "reused: ../evidence/logs/linkpeaks.log; not rerun after doc-only edits, environment fingerprint unchanged"),
 ("SCENIC+ / pycisTopic Snakemake route", "static-only", "restricted (pybedtools build, cisTarget DBs, days); SKILL.md and method-reference state not executed; COACC-012"),
 ("Whole-genome (all chromosomes) run", "blocked", "resource-infeasible; 3 chromosomes and 30 Mb slices executed; after-action: full-genome run with timeout 7200"),
 ("GeneHancer/FANTOM5/EpiMap, HiChIP/ABC/CRISPRi prose routes", "static-only", "no shipped code"),
 ("Markdown routing and LICENSE", "executed", "4/4 relative links resolve; MIT LICENSE present"),
]
json.dump({"schema": "execution-classifications-v1", "skill_id": SKILL, "candidate_sha256": ident,
           "surfaces": [{"surface": a, "class": b, "evidence": c} for a, b, c in cls]},
          open(os.path.join(R, 'execution-classifications.json'), 'w', encoding='utf-8'), indent=2)

v = [f"# Audit viewer: {SKILL} (independent final re-audit, 2026-09-30)", "",
     f"Candidate `sha256-manifest-v1 {ident}` (5 files, {sum(r[1] for r in rows)} bytes), origin `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility`. Prior audit identity 3c8089b0... (63/100).", "",
     f"**Result: {score} / 100 ({sw + dw:.1f} unrounded), {report['final']['grade']}, candidate-ready.** Static {sub} (x0.4 = {sw}), execution average {avg} (x0.6 = {dw}), assertions {passed}/{total}. Layer 1 average {sum(i['basic'] for i in inputs)/7:.1f}, Layer 2 average {sum(i['specialized'] for i in inputs)/7:.1f}. Skill veto PASS, research veto PASS. The margin over the 85 gate is thin; the score is the schema's integer rounding of 84.6.", "",
     "## Inputs", "", "| # | Type | Input | Status | Total | Assertions |", "|---|---|---|---|---|---|"]
for i in inputs:
    v.append(f"| {i['index']} | {i['type']} | {i['label']} | {i['status']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} |")
v += ["", "## Prior findings", "", "| ID | Severity | Disposition | Independent evidence |", "|---|---|---|---|"]
for i, s, st, n in prior: v.append(f"| {i} | {s} | {st} | {n} |")
v += ["", "## New findings (non-blocking)", "", "| ID | Severity | Summary |", "|---|---|---|"]
for f in F[-2:]: v.append(f"| {f['id']} | {f['severity']} | {f['summary']} |")
v += ["", "Report recommendations use P2 only (schema allows P0-P2); both new findings share one P2 recommendation. Ledger: `findings.json`.", "",
      "## Execution classification", "",
      "Executed: CLI (pattern .mtx, 3-chromosome and 30 Mb real slices), function API (window=1e6, tss_bed=NULL, seed), planted-truth recovery, guards, arc plot, Hi-C snippet, ArchR. Reused with matching runtime: alpha block and permutation control, LinkPeaks (150 genes). Failed (loud): zero-read cell. Static-only restricted: SCENIC+ (the Skill states it was not executed). Blocked: whole-genome run. See `execution-classifications.json`.", "",
      "## Coverage gaps and after-action", "",
      "- Whole-genome run untested: 3 chromosomes and chr1 30 Mb complete in 5-6 min and the Skill states runtime only for chr1, so the gap is a documented limit, not a defect. Rerun with a full-genome matrix and `timeout 7200`.",
      "- LinkPeaks not rerun after doc-only edits; the documented 8 min / 150 gene figure matches the tooling log (8 m 23 s).",
      "- SCENIC+: needs Python <=3.11 env with conda-forge pybedtools, pip-built scenicplus, cisTarget databases, then the Snakemake route on the Multiome h5.",
      "- Fixture note: the cached PBMC 5k scATAC is chr1-only, so the multi-chromosome run used the public 10x PBMC granulocyte-sorted 3k Multiome ATAC peaks (chr1/chr2/chr19 up to 4 Mb).", "",
      "## Reproduction", "",
      "Scripts in `scripts/` (ra_prep.R, ra_cli.sh, ra_cli_check.R, ra_fn.R/.sh, ra_docs.R, ra_archr.R, ra_stress.sh, build_report.py); logs in `logs/`; heavy work under `F:\\OpenScience\\audit-envs\\bio-atac-seq-co-accessibility\\work\\reaudit`. Environment per `../TOOLS.md`. Run inside WSL: `bash /mnt/openscience/audits/bio-atac-seq-co-accessibility/reaudit-run/scripts/ra_cli.sh`.", ""]
open(os.path.join(R, 'viewer.md'), 'w', encoding='utf-8').write("\n".join(v))
print(ident, sub, avg, sw, dw, score, passed, total)
