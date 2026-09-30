import json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
OK, NO = "✅", "⚠️"


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


def I(i, ty, label, st, note, b, s, asr):
    p = sum(a["result"] == "PASS" for a in asr)
    tot = b + s
    flag = OK if st == "COMPLETED" and tot >= 75 else (NO if st == "COMPLETED" else "❌")
    return {"index": i, "type": ty, "label": label, "status": st, "status_flag": flag, "note": note,
            "basic": b, "specialized": s, "total": tot, "assertions_passed": p,
            "assertions_total": len(asr), "assertions": asr}


inputs = [
    I(1, "Canonical", "Default CLI DESeq2 run on ENCODE GM12878 vs K562 (2 vs 2, hg38 chr1:1-30Mb)", "COMPLETED",
      "1181 sites (766 opened/415 closed); BED rows sum to CSV rows; 751 planted K562-only hits, 0.992 opened; diagnostics PDF (PCA, MA, volcano, heatmap) and 2-page annotation PDF rendered and inspected",
      36, 54, [
          A("Exit 0 and all five outputs written with prefix d_", "PASS", "d_opened.bed, d_closed.bed, d_annotated.csv, d_diagnostics.pdf, d_annoplot.pdf"),
          A("Opened+closed BED rows equal annotated CSV rows and all rows pass FDR<0.05 and |Fold|>=1", "PASS", "766+415=1181; max FDR 0.0499; min |Fold| 1.22"),
          A("Planted K562-only peaks are predominantly reported as opened", "PASS", "751 hits, 0.992 opened (independent overlap of narrowPeak sets)"),
          A("Rendered MA title count equals reported count and heatmap shows condition clustering", "PASS", "MA title 1181; heatmap splits GM1/GM2 vs K1/K2; TSS-distance page present"),
          A("Log states effective normalization matching docs default", "PASS", "Normalization: norm.method=lib lib.method=full")]),
    I(2, "Variant A", "--sva=2 surrogate-variable mode (P0 path); independent re-implementation and no-SV comparison", "COMPLETED",
      "svaseq capped 2->1 SV; design ~SV1 + Condition; 822 sites (383/439); output identical to my own svaseq+DESeq2 fit (max |dLFC|=0); SV changes results vs ~Condition alone (1372->822 sites); SV1 coefficient nonzero",
      35, 50, [
          A("Surrogate variable enters the fitted DESeq2 design", "PASS", "independent dds design ~SV1 + Condition, coef Intercept,SV1,Condition_treated_vs_control; skill table equals independent fit exactly"),
          A("Requested SVs beyond n-ncol(mod)-1 are capped and svaseq NaN is guarded", "PASS", "--sva=2, 4 and 9 all yield 1 SV with rc 0; NaN check present"),
          A("SV adjustment changes results in a plausible direction without destroying the planted signal", "PASS", "cor(LFC) 0.9992 vs no-SV, sites 1372->822, K562-only opened fraction 0.995"),
          A("SVA mode applies the same blacklist filter, threshold semantics and plots as the default path", "FAIL", "No blacklist step (0 removed on this data, general risk), hard |LFC|>=1 filter instead of DiffBind lfcThreshold test, no heatmap; only the script header notes part of this"),
          A("Volcano and MA figures legible with counts matching reported sites", "PASS", "MA and volcano titles read 822 sites; red/grey coding clear")]),
    I(3, "Variant B", "--method=edger backend via DiffBind", "COMPLETED",
      "1341 sites (906/435); 883 K562-only hits, 0.992 opened; rows consistent; figures rendered",
      35, 52, [
          A("edgeR backend executes end to end", "PASS", "rc 0, 'Fitting edger model', outputs with prefix e_"),
          A("Rows, BED split and thresholds are internally consistent", "PASS", "906+435=1341; max FDR 0.0495"),
          A("Planted K562-only peaks recovered as opened", "PASS", "883 hits, 0.992 opened")]),
    I(4, "Variant B", "--design='~Tissue + Condition' covariate design and DiffBind design restriction claim", "COMPLETED",
      "1020 sites (626/394), 614 K562-only hits, 0.995 opened; '~Batch + Condition' rejected by DiffBind with 'Invalid factors in design: Batch' as documented",
      35, 52, [
          A("Covariate design runs and reports consistent rows", "PASS", "626+394=1020; max FDR 0.0499"),
          A("Documented restriction to Tissue/Factor/Condition/Treatment/Replicate is true", "PASS", "Batch column: Error: Invalid factors in design: Batch (rc 1)"),
          A("Planted signal preserved under covariate adjustment", "PASS", "614 hits, 0.995 opened")]),
    I(5, "Edge", "Documented positional args and normalization choices (native; FDR 0.01, LFC 3)", "COMPLETED",
      "mypfx_* prefix honoured; FDR<0.01 and |LFC|>=3 -> 212 sites, min |Fold| 3.56, max FDR 0.0099; native reports RLE/RiP and 1096 sites (0.976 opened)",
      36, 52, [
          A("Positional prefix, normalize, fdr and lfc are honoured", "PASS", "mypfx_* files; log 'FDR < 0.01, |log2FC| >= 3.0'"),
          A("Reported sites satisfy the stricter thresholds", "PASS", "212 rows, max FDR 0.0099, min |Fold| 3.56"),
          A("native normalization is selectable and logged", "PASS", "norm.method=RLE lib.method=RiP; 1096 sites vs 1181 under lib"),
          A("Docs default (lib, full library) matches script default", "PASS", "default log norm.method=lib lib.method=full")]),
    I(6, "Edge", "Valid null result: no site passes (lfc_thr=10) in default and --sva modes", "COMPLETED",
      "Warning emitted, empty opened/closed BEDs and diagnostics PDF written, no crash, rc 0 in both modes; prior crash fixed",
      35, 50, [
          A("Zero-hit contrast does not crash", "PASS", "rc 0 for default and --sva=1"),
          A("User is warned and outputs are well-formed", "PASS", "warning 'No sites pass the thresholds'; 0-byte BEDs; diagnostics PDF present"),
          A("No misleading annotated table is produced", "PASS", "no *_annotated.csv written")]),
    I(7, "Scope Boundary", "Non-standard Condition labels and annotation scope (--case/--control, --txdb=none)", "COMPLETED",
      "Default labels error names the sheet's labels; --case=K562 --control=GM12878 reproduces 1181 sites; --txdb=none writes unannotated CSV without annotation PDF. Non-human TxDb package not executed (not installed)",
      36, 50, [
          A("Wrong labels fail early with actionable message", "PASS", "Condition labels 'treated'/'control' not found; sheet has: GM12878, K562 (set --case/--control)"),
          A("Explicit labels reproduce the standard analysis", "PASS", "1181 sites, 766/415, 751 K562-only hits"),
          A("--txdb=none skips annotation and still writes the DA table", "PASS", "nt_annotated.csv has 1181 rows, no annotation column; no annoplot PDF")]),
    I(8, "Adversarial", "Unknown flag, non-numeric thresholds, too-large --sva", "COMPLETED",
      "--bogus rejected with usage; fdr='abc' rejected; invalid --sva request capped instead of returning NaN results",
      36, 50, [
          A("Unknown flags are rejected rather than silently ignored", "PASS", "rc 1, Usage message naming 'bogus'"),
          A("Non-numeric thresholds are rejected", "PASS", "rc 1, 'fdr_thr and lfc_thr must be numeric'"),
          A("Oversized SV request cannot produce NaN model", "PASS", "--sva=4 and 9 capped to 1 SV, results identical to --sva=1")]),
]
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
cat = {
    "functional_suitability": (10, 12, "DESeq2 and edgeR DiffBind backends, covariate design and SVA shipped; csaw, RUVseq and spike-in are labelled recipe-only; non-human TxDb untested"),
    "reliability": (10, 12, "Previous crashes fixed (SVA, zero hits, CLI args); guards for labels, flags and design; SVA mode silently ignores --method and skips the blacklist filter"),
    "performance_context": (7, 8, "SKILL.md 57 lines with routed references and a single script"),
    "agent_usability": (14, 16, "Clear workflow and CLI header; SVA-mode limits documented only in the script header, and method-reference says SVA runs inside DiffBind"),
    "human_usability": (7, 8, "Actionable error messages, effective normalization logged; PCA labels overlap for identical K562 replicates"),
    "security": (11, 12, "Plain file inputs and cwd outputs; --txdb value is loaded with library() by name (local package name only)"),
    "maintainability": (10, 12, "Versions stated and satisfied, license and provenance preserved; threshold semantics differ between default and SVA paths without a note"),
    "agent_specific": (16, 20, "Precise description; body now matches the shipped script, except heatmap listed as output and SVA limits under-documented"),
}
sub = sum(v[0] for v in cat.values())
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
sc = int(round(sw + dw))
rep = {
    "meta": {"skill_name": "bio-atac-seq-differential-accessibility",
             "description": "Identify differentially accessible chromatin regions across conditions using DiffBind, csaw, DESeq2, or edgeR; covers consensus-peak vs sliding-window choice, normalization, SVA/RUVseq batch handling and effect-size thresholds.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "B", "complexity": "Complex", "n_inputs": len(inputs)},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; planted K562-only peaks recovered as opened at 0.976-1.000 across modes"},
            "practice_boundaries": {"result": "PASS", "detail": "Research-only analysis with no clinical claims"},
            "methodological_ground": {"result": "PASS", "detail": "Surrogate variables verified to enter the DESeq2 design and change results; documented design restriction verified; residual mode inconsistencies are P2"},
            "code_usability": {"result": "PASS", "detail": "All shipped CLI modes ran on real ENCODE data (rc 0) and guards rejected bad input with rc 1; the prior SVA and zero-hit failures are fixed and reproduced fixed"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cat.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100,
                      "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
                      "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": sc, "max": 100,
              "grade": "Production Ready" if sc >= 85 else "Limited Release",
              "grade_symbol": "⭐" if sc >= 85 else "✅", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The P0 SVA path is fixed: surrogate variables enter the DESeq2 design and the output equals an independent svaseq+DESeq2 fit exactly",
        "Every advertised CLI mode (DESeq2, edgeR, covariate design, SVA, native/lib normalization, thresholds) runs on real ENCODE data and recovers the planted K562-only peaks",
        "Failure guards are useful: unknown flags, wrong condition labels, invalid DiffBind design terms, zero-hit results and oversized SV requests",
        "Docs now separate shipped code from recipe-only methods and state the DiffBind design restriction, which was verified true"],
    "recommendations": [
        {"priority": "P2", "title": "SVA mode skips blacklist filter with no warning", "observed_in": [2],
         "problem": "--sva fits DESeq2 on dba.count output and never runs the DiffBind blacklist step that the default path applies in dba.analyze; on this chr1 slice 0 of 2260 intervals were affected, but genome-wide input could report blacklisted regions.",
         "root_cause": "fit_sva bypasses dba.analyze, which is where DiffBind applies blacklist and greylist filtering.",
         "fix": "Call dba.blacklist with the genome-matched blacklist before the SVA fit, or emit a runtime warning and list the limit in SKILL.md."},
        {"priority": "P2", "title": "SVA-mode limits documented only in the script header", "observed_in": [2],
         "problem": "method-reference says --sva runs inside DiffBind although it is a direct DESeq2 fit; --method is ignored silently with --sva; SKILL.md lists a heatmap output that SVA mode does not produce.",
         "root_cause": "Behavior notes live in the R header comment, not in SKILL.md or the reference.",
         "fix": "State in SKILL.md and method-reference that --sva fits DESeq2 directly, ignores --method and --design, and omits the heatmap and blacklist step; warn at runtime when --method is passed with --sva."},
        {"priority": "P2", "title": "Effect-size threshold semantics differ between modes", "observed_in": [1, 2],
         "problem": "Default and edgeR paths pass fold to DiffBind, which uses it as a DESeq2 lfcThreshold test (338 sites with FDR<0.05 and |Fold|>=1 are excluded, minimum reported |Fold| 1.22), while --sva applies a hard |LFC|>=1 post-filter (minimum 1.01); both are logged as |log2FC| >= 1.",
         "root_cause": "DiffBind dba.report(fold=) is a thresholded significance test, not a post-hoc filter, and the docs describe both paths as the same cutoff.",
         "fix": "Document the semantics difference or use a post-hoc |Fold| filter in both paths so counts are comparable across modes."},
        {"priority": "P2", "title": "Non-human TxDb untested; no SVA low-n caution", "observed_in": [2, 7],
         "problem": "--txdb=<package> was executed only for none because no non-human TxDb was installed; the 4-sample SVA yields 1 SV correlated 0.53 with Condition and no caution says it may absorb real signal.",
         "root_cause": "Only hg38 annotation packages were installed in the audit environment; no guidance on SVA validity for 2 vs 2 designs.",
         "fix": "Add a short SKILL.md caution about SVA on very small designs and validate one non-model-organism TxDb when available."}],
}
(R / "report.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
print(sub, avg, sw, dw, sc, rep["dynamic_score"]["assertion_pass_rate"])
