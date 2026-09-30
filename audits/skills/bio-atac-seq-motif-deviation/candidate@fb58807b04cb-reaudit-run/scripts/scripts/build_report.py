import json, hashlib, os
RR = r'F:\OpenScience\audits\bio-atac-seq-motif-deviation\reaudit-run'
SK = r'F:\OpenScience\wt\atac-motif-deviation\skills\bio-atac-seq-motif-deviation'


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


def inp(i, typ, label, status, note, b, s, asr):
    tot = b + s
    p = sum(a["result"] == "PASS" for a in asr)
    flag = "✅" if status == "COMPLETED" and tot >= 75 else ("⚠️" if status == "COMPLETED" else "❌")
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note,
            "basic": b, "specialized": s, "total": tot, "assertions_passed": p,
            "assertions_total": len(asr), "assertions": asr}


inputs = [
    inp(1, "Canonical", "Shipped bulk script, unmodified, with depth.tsv on ENCODE GM12878 x3 vs K562 x3 (chr1:1-30 Mb, 6,357 peaks); run twice", "COMPLETED",
        "Exit 0 twice, CSVs byte-identical; biology correct; one numeric claim in SKILL.md is wrong", 35, 53, [
            A("Script exits 0 and writes deviations, variability and differential CSVs plus two PDFs; 879 motifs x 6 samples, 0 NA, 5,340 peaks pass filters", "PASS",
              "Parsed: 879 x 6, 0 NA; 742 motifs at adj.P.Val<0.05 and |logFC|>=0.5, matching the SKILL.md count"),
            A("depth.tsv requirement is documented and enforced (stopifnot on sample names)", "PASS",
              "Documented in SKILL.md steps 1-2 and the script header; guard run in input 2"),
            A("Two clean-directory runs give byte-identical outputs and the reproducibility comes from set.seed", "PASS",
              "Runs A and B: identical sha256 for all three CSVs, also identical to fix-run and tooling-delta; a control copy with set.seed removed differs (max |dz| 1.485, significant-set Jaccard 0.866)"),
            A("Contrast recovers known biology: K562 erythroid GATA/TAL1 up, GM12878 lymphoid SPIB/Spi1/IRF/REL/EBF1/PAX5 up; labels read 'ID (name)'; heatmap legible", "PASS",
              "GATA2 +8.39, GATA1::TAL1 +6.0, Spi1 -11.05, SPIB -12.32, EBF1 -3.62; heat.png re-drawn from the shipped call shows two clean column blocks and readable row labels"),
            A("Numeric statements in SKILL.md match the run", "FAIL",
              "SKILL.md says top GM12878-vs-K562 motifs 'exceeded 9 in absolute value' under the z-score definition; measured max |z| is 7.24 (0 motifs above 9); only group logFC (up to about 14) exceeds 9")]),
    inp(2, "Variant A", "Failure guard and stochasticity control on the bulk script", "COMPLETED",
        "Guard stops before compute; unseeded control demonstrates the set.seed need", 35, 53, [
            A("depth.tsv lacking one sample stops early with an actionable stopifnot error and no outputs", "PASS",
              "Exit 1 'all(colnames(se) %in% names(depth)) is not TRUE'; directory holds only inputs and logs"),
            A("Removing set.seed changes z-scores and hit list (proves the fix is what makes outputs reproducible)", "PASS",
              "Max |dz| 1.485; 742 vs 721 significant motifs"),
            A("Prose claim 'unseeded reruns changed z by up to 1.25 and the significant set by about 12%' is consistent with a fresh control", "PASS",
              "Observed 1.485 and 13.4% (Jaccard 0.866); the claim is an observed example, not a bound")]),
    inp(3, "Variant B", "Signac direct-chromVAR route extracted verbatim from single-cell.md, run on Signac 1.17.1 and 1.16.0 (10x PBMC 5k slice)", "COMPLETED",
        "Same results on both versions; RunChromVAR presence/absence verified", 36, 54, [
            A("Verbatim snippet completes on Signac 1.17.1 (where RunChromVAR is absent)", "PASS",
              "RunChromVAR exported FALSE in 1.17.1, TRUE in 1.16.0; snippet exit 0"),
            A("chromvar assay is 879 motifs x 1,853 cells with 0 NA and a plausible range", "PASS",
              "dim 879x1853, NA 0, range -4.17..4.61; NA-count guard line prints 0"),
            A("FindAllMarkers with mean.fxn=rowMeans, fc.name='avg_diff' returns avg_diff and lineage-plausible TFs", "PASS",
              "Columns p_val,avg_diff,pct.1,pct.2,p_val_adj,cluster,gene,tf; cluster 0 TCF7/Gata3 (T lineage), cluster 2 SPIB/NFIA (B/myeloid-like)"),
            A("Route is version-independent (1.16.0 identical to 1.17.1)", "PASS",
              "Identical dimensions, range and marker lists on both")]),
    inp(4, "Variant B", "ArchR NA guard and getMarkerFeatures on the saved 216-cell ArchR project (upstream chain lines identical to origin; first-pass evidence reused)", "COMPLETED",
        "Guard works on the slice; root cause guarded not solved; full-scale recurrence unproven and stated as such", 31, 46, [
            A("Without the guard, getMarkerFeatures fails on NA z-scores as the Skill states", "PASS",
              "Control run exit 1: wilcoxauc X contains NA values"),
            A("Verbatim guard drops the NA cells and getMarkerFeatures completes", "PASS",
              "6 cells dropped, 210 remain; C3 34 markers at FDR<=0.05 and MeanDiff>=0.5, other clusters 0"),
            A("Post-guard MotifMatrix z is NA-free", "PASS", "NA 0, dim 870 x 210"),
            A("Skill states honestly that full-scale recurrence is untested and gives a report-the-count instruction", "PASS",
              "single-cell.md: 'Whether this recurs on a full-depth dataset is untested; count NA first and report how many cells were dropped'; SKILL.md guardrail says check and drop first"),
            A("Full-scale recurrence or a root-cause fix is demonstrated", "FAIL",
              "Not tested (slice only, 216 cells); C3 hits (OTX2, KDM2B, HOXB2, VAX2) are not PBMC-plausible, consistent with the stated weakness at this size")]),
    inp(5, "Variant B", "Reused identity-matched evidence: chromVAR hand-check, JASPAR2024/TFBSTools workaround; DecoupleR removal (static)", "COMPLETED",
        "Reused: env fingerprint unchanged, Skill code paths for these surfaces untouched; removal verified by grep", 36, 54, [
            A("computeDeviations and z equal an independent hand computation", "PASS",
              "Reused smoke_chromvar_handcheck.log (environment fingerprint 91dcd670... verified live): max |diff| 1.1e-16, planted signal 17.08"),
            A("SQLite-handle getMatrixSet workaround is required and returns 879 CORE vertebrate PFMs (1,912 with all_versions=TRUE)", "PASS",
              "Reused jaspar_direct.log; direct call errors, SQLite handle gives 879; the same 879 reproduced in every fresh run this phase"),
            A("DecoupleR block and TF-activity claim removed from the shipped Skill", "PASS",
              "grep for decoupler/collectri in the candidate matches only a method-reference caution that decoupleR on chromVAR z is not TF activity")]),
]
ex = round(sum(i["total"] for i in inputs) / len(inputs), 1)
pp = sum(i["assertions_passed"] for i in inputs)
tt = sum(i["assertions_total"] for i in inputs)
cats = {
    "functional_suitability": (11, 12, "Bulk, Signac and ArchR routes execute and reproduce known biology; one measured-number claim (z above 9) is wrong"),
    "reliability": (10, 12, "depth stopifnot, set.seed and NA guard all verified; ArchR NA cause is guarded not solved and unproven at full scale (stated)"),
    "performance_context": (7, 8, "SKILL.md 77 lines with routed references; method-reference 106 lines but sectioned"),
    "agent_usability": (14, 16, "Clear workflow table and step list; condition vector and genome still hard-coded and flagged for editing"),
    "human_usability": (7, 8, "Outputs use ID (name); heatmap legible; caveats and heuristics labelled"),
    "security": (10, 12, "No credentials, network or destructive operations; local files only"),
    "maintainability": (10, 12, "License and provenance preserved; tested stack stated; Bioc 3.23 not run; one stale number"),
    "agent_specific": (17, 20, "Trigger-rich description, progressive disclosure, honest labelling of unexecuted paths"),
}
st = sum(v[0] for v in cats.values())
sw = round(st * .4, 1)
dw = round(ex * .6, 1)
score = round(sw + dw)
rep = {
    "meta": {"skill_name": "bio-atac-seq-motif-deviation",
             "description": "Analyze TF motif accessibility variability across samples or single cells using chromVAR. Use when identifying TF motifs whose accessibility correlates with conditions, computing per-sample motif z-scores after matched background correction, comparing to ArchR / Signac equivalents, or distinguishing motif-accessibility signal from per-site footprinting.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "D", "complexity": "Moderate", "n_inputs": 5},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; unexecuted paths and heuristics are labelled; one wrong measured number filed as P2 (MOTDEV-013), not a fabricated result"},
            "practice_boundaries": {"result": "PASS", "detail": "Research-only genomics skill; no clinical conclusions"},
            "methodological_ground": {"result": "PASS", "detail": "chromVAR core equals hand computation; K562 vs GM12878 contrast recovers GATA/TAL1 versus SPIB/Spi1/IRF/EBF1/PAX5; DecoupleR misuse removed"},
            "code_usability": {"result": "PASS", "detail": "Shipped script runs unmodified with documented depth.tsv and is byte-identical across reruns; Signac direct route and ArchR guard run verbatim"}}},
    "static_score": {"subtotal": st, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": ex, "max": 100, "assertion_pass_rate": {"passed": pp, "total": tt}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
              "grade": "Production Ready" if score >= 85 else "Limited Release",
              "grade_symbol": "⭐" if score >= 85 else "✅", "deployable": score >= 85, "veto_override": False},
    "key_strengths": [
        "Both former P0s verified fixed independently: the unmodified bulk script runs with depth.tsv and outputs are byte-identical across clean reruns, while removing set.seed demonstrably breaks reproducibility",
        "Signac direct chromVAR route runs verbatim on 1.17.1 and 1.16.0 with identical 879 x 1,853 NA-free results",
        "ArchR NA failure reproduced without the guard and resolved with it; the Skill states honestly that full-scale recurrence is untested",
        "Biology matches the cell lines: K562 GATA1/GATA2/TAL1 up, GM12878 SPIB/Spi1/IRF/REL/EBF1/PAX5 up, with readable ID (name) labels",
        "Provenance, license and tested-stack statement retained; DecoupleR misuse removed"],
    "recommendations": [
        {"priority": "P2", "title": "Correct the 'top motifs exceeded 9' z-score statement", "observed_in": [1],
         "problem": "SKILL.md says GM12878 vs K562 top motifs exceeded 9 in absolute z-score; the fresh run has max |z| 7.24 and no motif above 9; only the group difference (logFC) reaches about 14 (MOTDEV-013).",
         "root_cause": "The fix rewrote the range sentence without checking it against the run outputs.",
         "fix": "State max |z| about 7 per sample and logFC up to about 14 between groups, or drop the number."},
        {"priority": "P2", "title": "ArchR NA z-scores guarded, not root-caused (MOTDEV-004)", "observed_in": [4],
         "problem": "The guard drops NA cells so getMarkerFeatures completes, but recurrence at full depth is untested and dropped cells change cluster composition.",
         "root_cause": "Zero-read motif peaks give zero background SD in sparse cells; not investigated at full scale.",
         "fix": "Optionally test on whole-genome PBMC 5k fragments and add a minimum-fragment cell filter before addDeviationsMatrix if NA recurs."}]}
json.dump(rep, open(RR + r'\report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
assert [r["priority"] for r in rep["recommendations"]] == sorted(r["priority"] for r in rep["recommendations"])
assert all(r["priority"] in ("P0", "P1", "P2") for r in rep["recommendations"])
assert all(i["total"] == i["basic"] + i["specialized"] and i["assertions_total"] == len(i["assertions"]) for i in inputs) and len(inputs) == rep["meta"]["n_inputs"]
b = sum(i["basic"] for i in inputs) / 5
s = sum(i["specialized"] for i in inputs) / 5
print("static", st, "exec", ex, "L1", b, "L2", s, "pass", pp, tt, pp / tt, "score", score, sw, dw)
rows = []
for r, d, f in os.walk(SK):
    for n in f:
        p = os.path.join(r, n)
        rel = os.path.relpath(p, SK).replace(os.sep, '/')
        by = open(p, 'rb').read()
        rows.append((rel.encode(), rel, len(by), hashlib.sha256(by).hexdigest()))
rows.sort()
man = hashlib.sha256('\n'.join(f'{a}\t{l}\t{h}' for _, a, l, h in rows).encode()).hexdigest()
si = json.load(open(r'F:\OpenScience\audits\bio-atac-seq-motif-deviation\initial-audit-20260930\source-identity.json', encoding='utf-8'))
si["phase"] = "final re-audit"
si["independent_auditor"] = True
si["candidate"].update({"manifest_sha256": man, "file_count": len(rows), "byte_total": sum(r[2] for r in rows),
                        "status_before": "skill directory untracked; no other working-tree edits",
                        "status_after_execution": "unchanged (manifest recomputed after execution)"})
si["files"] = [{"path": a, "sha256": h, "bytes": l} for _, a, l, h in rows]
si["tooling"] = {"tools_md": r"F:\OpenScience\audits\bio-atac-seq-motif-deviation\TOOLS.md",
                 "tools_md_sha256": hashlib.sha256(open(r'F:\OpenScience\audits\bio-atac-seq-motif-deviation\TOOLS.md', 'rb').read()).hexdigest(),
                 "environment_fingerprint_sha256": "91dcd6702bfba8518d2ff53ff1fec2bf447b62d06a091c00124c7ee4e1118ecd",
                 "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de"}
si["prior_audit"] = {"path": r"F:\OpenScience\audits\bio-atac-seq-motif-deviation\initial-audit-20260930",
                     "identity": "d645db4df84650ecf90027b9013e38b0d9adce73fb985a605d769c730d68fefc", "score": 60}
si["candidate_cache_artifacts_after_execution"] = []
json.dump(si, open(RR + r'\source-identity.json', 'w', encoding='utf-8'), indent=2)
print(man, len(rows), sum(r[2] for r in rows))
