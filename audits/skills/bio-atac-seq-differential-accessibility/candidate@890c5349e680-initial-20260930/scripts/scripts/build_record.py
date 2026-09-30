# Builds report.json and source-identity.json for the initial audit (run from the run root).
import json, hashlib, pathlib
SK = pathlib.Path(r"F:\OpenScience\wt\atac-differential-accessibility\skills\bio-atac-seq-differential-accessibility")
files = sorted([p for p in SK.rglob("*") if p.is_file()], key=lambda p: p.relative_to(SK).as_posix())
recs = [(p.relative_to(SK).as_posix(), len(p.read_bytes()), hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
manifest = "\n".join(f"{a}\t{b}\t{c}" for a, b, c in recs)
ident = hashlib.sha256(manifest.encode()).hexdigest()
assert ident == "890c5349e6800257d819457a4704a35b14f2fd5a48fe3dd6c3b751f73ad3c7d7", ident
json.dump({
 "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/differential-accessibility",
            "normalization_note": "Candidate is a normalized derivative (references/, scripts/ routed); origin identifies the source Skill subtree, not a one-to-one file map."},
 "candidate": {"branch": "fix/atac-differential-accessibility", "base_commit": "3186916", "path": str(SK), "status": "untracked Skill subtree only; unmodified by audit",
               "content_sha256": ident,
               "content_manifest": {"file_count": len(recs), "bytes": sum(r[1] for r in recs),
                                    "recipe": "relative POSIX path, byte count, lowercase SHA-256 separated by TAB; sorted StringComparer.Ordinal; joined by LF; no trailing LF"},
               "files": [{"path": a, "bytes": b, "sha256": c} for a, b, c in recs]},
 "tooling": {"tools_md": r"F:\OpenScience\audits\bio-atac-seq-differential-accessibility\TOOLS.md",
             "env_fingerprint": "2998eae45e95156bbe8b1ec4f619756fe7f8e1803c9931270a3f7a4594d54236",
             "rubric_zip_sha256": hashlib.sha256(open(r"F:\optimizing-agent-science-skills\skill-auditor.zip", "rb").read()).hexdigest(),
             "environment": "WSL2 science, micromamba env bio-atac-seq-differential-accessibility; R 4.4.3, DiffBind 3.16.0, DESeq2 1.46.0, edgeR 4.4.0, csaw 1.40.0, ChIPseeker 1.42.0, sva 3.54.0, RUVSeq 1.40.0; /mnt/openscience only"},
 "candidate_cache_artifacts_after_execution": []}, open("source-identity.json", "w", encoding="utf-8"), indent=1)


def a(t, ok, n):
    return {"text": t, "result": "PASS" if ok else "FAIL", "note": n}


def inp(i, typ, label, status, note, b, s, asserts):
    tot = b + s
    flag = "\u274c" if status != "COMPLETED" else ("\u2705" if tot >= 75 else "\u26a0\ufe0f")
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": b, "specialized": s, "total": tot,
            "assertions_passed": sum(x["result"] == "PASS" for x in asserts), "assertions_total": len(asserts), "assertions": asserts}


inputs = [
    inp(1, "Canonical", "CLI DESeq2 run on ENCODE GM12878 vs K562 (2 vs 2 reps, hg38 chr1:1-30Mb)", "COMPLETED",
        "1096 DA sites (535 opened/561 closed); 0.970 of planted K562-only peaks opened; annotation PDF is missing the TSS-distance plot", 33, 46, [
            a("Script exits 0 and writes opened/closed BED, annotated CSV and two PDFs", True, "TOOLS.md smoke-skill.log; evidence/cli.log"),
            a("Annotated CSV rows equal opened+closed BED rows", True, "1096 vs 1096"),
            a("Planted truth: K562-only peaks (absent from GM12878 peaks) gain accessibility in treated=K562", True, "0.970 opened in tooling run; 0.976 (541 sites) against the stricter both-GM-reps truth in norm.log"),
            a("Diagnostics PDF has legible, interpretable PCA, MA, volcano and heatmap", True, "4 pages; equivalent PNG renders inspected (work/plots); PC1 94% separates conditions; heatmap colour bars have no legend"),
            a("Annotation PDF contains both plotAnnoPie and plotDistToTSS", False, "plt_annoplot.pdf /Count 1: the ggplot returned by plotDistToTSS is never printed")]),
    inp(2, "Variant A", "run_diff(normalize_mode=DBA_NORM_LIB) via sourced function, same data", "COMPLETED",
        "1181 sites (766 opened/415 closed) vs 1096 (535/561) under NATIVE; NATIVE reports RLE + RiP library, LIB reports lib + full", 33, 47, [
            a("Run completes and reports FDR<0.05, |Fold|>=1 sites", True, "evidence/norm.log"),
            a("Normalization applied is lib/full as requested", True, "dba.normalize(bRetrieve) norm.method=lib lib.method=full"),
            a("Planted K562-only peaks opened >=85%", True, "751 sites, 0.992 opened"),
            a("Console log names the normalization mode used", False, "prints Normalizing ( nmode ) (variable name) instead of the mode")]),
    inp(3, "Variant B", "run_diff(use_sva=TRUE) on 4 samples (SVA hidden-batch branch)", "ERROR",
        "svaseq(n.sv=2) fails: density.default missing values / NaNs in pf; n.sv=1 works (tooling probe); SVs are never fed to the model", 14, 12, [
            a("SVA branch completes on a 2 vs 2 design", False, "evidence/sva.log error; TOOLS evidence sva-probe.log"),
            a("Surrogate variables enter the DESeq2/DiffBind design", False, "script only prints ncol(sv); dba.analyze is unchanged (static, script lines 39-46)"),
            a("Number of SVs adapts to sample size", False, "n.sv hard-coded 2 with 4 samples")]),
    inp(4, "Edge", "Documented CLI usage: Rscript diff_accessibility.R sheet.csv mypfx DBA_NORM_LIB 0.01 3", "COMPLETED",
        "Exit 0 but args 2-5 silently ignored: outputs named diff_atac_*, reported at FDR<0.05, |Fold|>=1, NATIVE", 22, 26, [
            a("output_prefix argument honored", False, "no mypfx_* files; diff_atac_* written"),
            a("fdr_thr / lfc_thr arguments honored", False, "log says Reporting at FDR < 0.05, |Fold| >= 1.0 despite 0.01 and 3"),
            a("Ignoring a documented argument is signalled to the user", False, "no warning; exit status 0")]),
    inp(5, "Edge", "Valid null result: lfc_thr=10 gives zero differential sites", "PARTIAL",
        "DiffBind warns No sites above threshold, then export(NULL) errors; no BED/CSV/annotation produced", 24, 28, [
            a("Zero-hit contrast finishes cleanly with empty outputs or a clear message", False, "Error in export: cannot export object of class NULL"),
            a("Failure message tells the user the result was simply empty", False, "cryptic export error"),
            a("Underlying DiffBind warning is surfaced", True, "No sites above threshold warning present")]),
    inp(6, "Edge", "Sample sheet with Condition labels GM12878/K562 instead of control/treated", "PARTIAL",
        "dba.contrast hard-coded to treated/control fails: Invalid contrast: no replicates in one group", 26, 32, [
            a("Condition labels other than control/treated are accepted or documented as required", False, "SKILL.md and usage guide never state the hard-coded labels"),
            a("Error message names the label mismatch", False, "misleading no replicates in one group"),
            a("Fails loudly rather than silently mis-signing the contrast", True, "run stops before analysis")]),
]
n = len(inputs)
avg = round(sum(i["total"] for i in inputs) / n, 1)
static = [
    ("functional_suitability", 8, 12, "Runnable script covers only a DESeq2 two-group contrast; edgeR/csaw/RUVseq/spike-in/covariate design are recipes, not code"),
    ("reliability", 6, 12, "SVA branch crashes; zero-hit contrast crashes; documented CLI args silently ignored"),
    ("performance_context", 7, 8, "SKILL.md 57 lines with routed references; method-reference is 317 lines but routed"),
    ("agent_usability", 12, 16, "Clear trigger and workflow; script usage promises parameters the CLI does not expose; default normalization contradicts SKILL.md workflow"),
    ("human_usability", 6, 8, "Undocumented control/treated label requirement; misleading errors; heatmap colour bars have no legend"),
    ("security", 11, 12, "No injection or destructive surface; plain file inputs and outputs in cwd"),
    ("maintainability", 9, 12, "Dependencies and versions stated and satisfied; license and provenance preserved; stale usage line"),
    ("agent_specific", 15, 20, "Description is precise; body oversells SVA/edgeR/RUV as supported by the script"),
]
sub = sum(s[1] for s in static)
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
recs_ = [
    ("P0", "SVA branch crashes and never corrects", [3],
     "use_sva=TRUE fails with hard-coded n.sv=2 on 4 samples; even when it runs, SVs are only printed and never enter the model, yet the log implies a correction.",
     "SVA snippet is an extraction example, not a tested analysis path, and use_sva is not reachable from the CLI.",
     "Choose n.sv with num.sv capped by sample count, feed SVs into the design and assert the model uses them; else remove the branch and route to the tested method-reference recipe. DAC-001."),
    ("P1", "Documented CLI args 2-5 silently ignored", [4],
     "Usage lists output_prefix, normalize_mode, fdr_thr, lfc_thr but only args[1] is used; requested FDR 0.01 / lfc 3 silently become 0.05 / 1.",
     "Entry point calls run_diff(args[1]) only.",
     "Parse and validate args (or named flags) including use_sva; reject unknown values. DAC-002."),
    ("P1", "Default normalization contradicts the Skill guidance", [1, 2],
     "Script default DBA_NORM_NATIVE yields RLE with RiP library size; SKILL.md calls full-library the default and the usage guide prescribes DBA_NORM_LIB for cross-cell-type comparisons. Opened/closed split moves from 535/561 to 766/415.",
     "The effective library method is never logged and the defaults were not reconciled.",
     "Pick one default consistent with the guidance, log norm.method/lib.method from dba.normalize, and state the RiP trade-off in the Skill body. DAC-003."),
    ("P2", "Annotation PDF omits TSS-distance plot", [1],
     "plotDistToTSS returns a ggplot that is never printed inside pdf(); the file has one page.",
     "ggplot objects are not auto-printed inside a function.",
     "print() the plot object and assert page count. DAC-004."),
    ("P2", "Zero-hit contrast crashes", [5],
     "A legitimate empty result stops with export(NULL) and no outputs.",
     "No length(results)==0 guard.",
     "Guard empty results: write empty BEDs/CSV and a clear message. DAC-005."),
    ("P2", "control/treated labels hard-coded and undocumented", [6],
     "Other Condition labels fail with a misleading error.",
     "dba.contrast is fixed to c(Condition, treated, control).",
     "Take group labels as parameters or document and validate them. DAC-006."),
    ("P2", "edgeR/RUV/spike-in/covariate paths lack runnable code", [],
     "Only DESeq2 two-group runs; edgeR (via DiffBind), csaw and RUV recipes executed by tooling as reference code only; spike-in and covariate design not executed.",
     "Skill body lists them as workflow options without shipped code.",
     "Ship a parameterised edgeR backend and design argument, or label the rest recipe-only. DAC-007 (NORM-001..003)."),
    ("P2", "Console log and plot titles misreport", [2, 1],
     "Log prints nmode for the normalization; MA/volcano titles count FDR<=0.05 sites (1835) while the report uses |Fold|>=1 (1096).",
     "deparse(substitute()) on a variable; DiffBind plots ignore the fold filter.",
     "Log the resolved mode; pass th/fold to plots or note the difference. DAC-008."),
    ("P2", "hg38 TxDb hard-coded", [],
     "No genome argument or annotation bypass though method-reference advertises custom genomes.",
     "Static library() of the hg38 TxDb.",
     "Add a TxDb/genome parameter or state hg38-only. DAC-009."),
]
report = {
    "meta": {"skill_name": "bio-atac-seq-differential-accessibility",
             "description": "Identify differentially accessible chromatin regions across conditions using DiffBind, csaw, DESeq2, or edgeR; covers consensus-peak vs sliding-window choice, normalization, SVA/RUVseq batch handling and effect-size thresholds.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "B", "complexity": "Complex", "n_inputs": n},
    "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
                   "research_veto": {"applicable": True, "gate": "FAIL",
                                     "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; planted K562-only peaks recovered at 0.970-0.992"},
                                     "practice_boundaries": {"result": "PASS", "detail": "No clinical claims; research-only analysis"},
                                     "methodological_ground": {"result": "PASS", "detail": "Default DESeq2 path is sound; silent CLI-arg and normalization inconsistencies are filed as P1 findings, not principled fallacies"},
                                     "code_usability": {"result": "FAIL", "detail": "Input 3: shipped use_sva=TRUE branch fails on a 4-sample design and never applies the SVs; Input 5: empty result crashes"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": s, "max": m, "note": nt} for k, s, m, nt in static}},
    "dynamic_score": {"execution_avg": avg, "max": 100,
                      "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
                      "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Reject", "grade_symbol": "\u274c", "deployable": False, "veto_override": True},
    "key_strengths": ["Default DESeq2/DiffBind CLI runs end to end on real ENCODE data and recovers planted K562-only peaks at 0.97-0.99",
                      "Diagnostics PDF contains four populated, interpretable figures (PCA, MA, volcano, heatmap)",
                      "Method reference gives a coherent decision table, normalization-trap analysis and cited literature",
                      "Stated package minimums are met by current Bioconductor releases; provenance and license preserved"],
    "recommendations": [{"priority": p, "title": t[:60], "observed_in": o, "problem": pr, "root_cause": rc, "fix": fx} for p, t, o, pr, rc, fx in recs_]}
json.dump(report, open("report.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
assert report["static_score"]["subtotal"] == sum(v["score"] for v in report["static_score"]["categories"].values())
for i in inputs:
    assert i["basic"] + i["specialized"] == i["total"] and 3 <= i["assertions_total"] <= 5
print("identity", ident, "static", sub, "exec", avg, "score", score, report["dynamic_score"]["assertion_pass_rate"])
