import json
R = "F:/OpenScience/audits/bio-atac-seq-footprinting/reaudit-run"
files = json.load(open(f"{R}/files.json", encoding="utf-8"))
blobs = dict(l.split() for l in open(f"{R}/logs/git_blobs.txt", encoding="utf-8"))
for f in files:
    f["git_blob"] = blobs[f["path"]]
ident = "a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87"
si = {
    "phase": "final re-audit", "independent_auditor": True,
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/footprinting",
               "subtree": "7ded85e1af526f2912805fe6da472f78fe2940e8", "checkout": "F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills"},
    "candidate": {"branch": "fix/atac-footprinting", "commit": "3186916406e9cc6b0e6dc24ffe47880951fc0f93", "identity": "sha256-manifest-v1",
                  "manifest_sha256": ident, "file_count": len(files), "byte_total": sum(f["bytes"] for f in files),
                  "path": "F:\\OpenScience\\wt\\atac-footprinting\\skills\\bio-atac-seq-footprinting",
                  "status_before": "skills/bio-atac-seq-footprinting untracked (7 files); no tracked-file edits",
                  "status_after_execution": "unchanged; manifest recomputed live before and after execution (scripts/manifest.py)",
                  "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; tab-separated; LF joins; ordinal UTF-8 byte ordering; no trailing LF"},
    "files": files,
    "tooling": {"tools_md_sha256": "303b12248b7ad738192c087a72887020cd5f0ed80061eb21ea2746e66811484f",
                "environment_fingerprint_sha256": "48e27feb8a7d10a6fa41936ce8078dc4f6a5a68ac340d90ddca6a51ca4f49974",
                "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de"},
    "candidate_cache_artifacts_after_execution": []}
json.dump(si, open(f"{R}/source-identity.json", "w", encoding="utf-8"), indent=2)


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


inputs = [
    dict(index=1, type="Canonical", label="run_tobias.sh unmodified in a fresh recipe env, GM12878 vs K562 chr1:1-30 Mb", status="COMPLETED", status_flag="✅",
         note="rc 0; ranking equals independent |change| order; CTCF 513 bound sites; plots rendered and legible", basic=36, specialized=52,
         assertions=[
             A("rc 0 with bigwigs, bindetect_results.txt and per-condition CTCF aggregate PDFs present", "PASS", "13 motif IDs; 2 PDFs rendered at 90 dpi, 3x4 panels legible"),
             A("Top-motif table equals an independent pandas ranking of |change| among p <= 0.05", "PASS", "12 rows, IRF4 first, GATA1 second"),
             A("Direction of change matches biology: GATA1 < 0 (K562), IRF4 > 0 (GM12878)", "PASS", "GATA1 -0.385, IRF4 +0.588"),
             A("Corrected CTCF profile: bound dip deeper than unbound and minimum within 10 bp of centre, both conditions", "PASS", "flank-core 6.67/9.50 bound vs 0.23/0.50 unbound"),
             A("Uncorrected and corrected panels both present per condition at all, bound and unbound sites", "PASS", "all-sites flank-core 2.51 to 2.97 (cond1), 4.39 to 5.64 (cond2)")]),
    dict(index=2, type="Edge", label="Guards: no-CTCF motif set (default and ALLOW_NO_CTCF), missing input, spaces in every path", status="COMPLETED", status_flag="✅",
         note="B rc 3 with warning and error, C rc 0 with warning, D rc 2 with no output dir, E rc 0 identical to A", basic=35, specialized=51,
         assertions=[
             A("Motif set without CTCF exits 3, names the missing CTCF control on stderr, still prints the differential table", "PASS", "rc 3, WARNING and ERROR lines, validation/ empty"),
             A("ALLOW_NO_CTCF=1 continues with rc 0 and keeps the warning", "PASS", "rc 0, WARNING kept, no ERROR"),
             A("Missing input file stops with rc 2 before creating outputs", "PASS", "input not found, no output dir"),
             A("Paths with spaces in every argument run to completion with identical results and no stray directories", "PASS", "rc 0, results equal A, no out/ or dir/")]),
    dict(index=3, type="Adversarial", label="Bias correction absent: corrected track replaced by the uncorrected track via a TOBIAS shim", status="COMPLETED", status_flag="✅",
         note="script exits 0 with no warning; bound-site dip stays deep (7.14 vs 6.67); limitation is disclosed in SKILL.md but not detected", basic=33, specialized=47,
         assertions=[
             A("Positive-control step warns or fails when the corrected track carries no bias correction", "FAIL", "rc 0, no WARNING or ERROR; guard only tests CTCF presence (FOOT-008 residual)"),
             A("SKILL.md states that a bound-site dip alone does not prove correction and points to the uncorrected panel", "PASS", "workflow step 5 and script epilogue say so"),
             A("Uncorrected and corrected panels differ when correction is real", "PASS", "all-sites flank-core is higher corrected than uncorrected in both conditions, by 0.5 to 1.3 units"),
             A("Differential table remains scientifically sane without correction", "PASS", "CTCF_MA0139.2 change -0.231 vs -0.222")]),
    dict(index=4, type="Variant B", label="HINT-ATAC via the documented RGT data recipe, Wellington -A, site_concordance.sh", status="COMPLETED", status_flag="✅",
         note="plain pip is a no-op as documented; corrected recipe writes data.config; HINT 358 footprints; concordance recomputed independently", basic=35, specialized=51,
         assertions=[
             A("Plain pip install leaves RGTDATA empty in the bioconda env while the documented force-reinstall line writes data.config and HMMs", "PASS", "no rgtdata_plain dir; data.config, fp_hmms, hg38 present after recipe"),
             A("setupGenomicData.py and the SKILL.md rgt-hint command run to rc 0 with a scored footprint BED", "PASS", "358 footprints, score column present, 12 s"),
             A("Wellington -A runs to rc 0 on the paired-end BAM and yields FDR footprints", "PASS", "62-line FDR BED"),
             A("site_concordance.sh output equals a pure-python recomputation", "PASS", "58/143 bound, 0/31 unbound, 54/358 reverse; python script matched"),
             A("Concordance helper rejects an empty call set", "PASS", "rc 2 with message")]),
    dict(index=5, type="Variant B", label="scprinter_footprint.py bulk classic route, fresh pinned env, GPU, CTCF bound vs unbound", status="COMPLETED", status_flag="✅",
         note="fresh pinned env; 400x99x200 finite scores; mode 10-30 bound > unbound; mode 50 reported as not separating", basic=35, specialized=51,
         assertions=[
             A("Documented fragment recipe with the fresh env's samtools/bgzip/tabix produces an indexed fragment file", "PASS", "521,478 fragments, tabix rc 0"),
             A("Script runs unmodified on GPU and writes finite scores of shape regions x modes x width", "PASS", "(400, 99, 200), all finite, 14 min"),
             A("CTCF centre +/-10 bp score is higher at TOBIAS-bound than unbound sites at modes 10, 20, 30", "PASS", "0.673/0.353, 1.661/0.440, 0.717/0.341; p 9e-17, 2e-17, 8e-8"),
             A("Mode-10 bound profile peaks near the motif centre and the SKILL.md statement that mode 50 does not separate matches data", "PASS", "peak offset 2 bp; mode 50 0.085 vs 0.238 (p 1.0); figure shows central plus flank peaks"),
             A("Missing fragment file fails loudly", "PASS", "rc 1 with FileNotFoundError traceback (unfriendly but not silent)")]),
    dict(index=6, type="Variant A", label="Per-tool env recipes in fresh envs plus NFR filter and alignmentSieve --ATACshift", status="COMPLETED", status_flag="✅",
         note="all recipes rc 0 with tested versions; NFR counts match samtools -e; shift +4/-5 confirmed", basic=35, specialized=52,
         assertions=[
             A("All four usage-guide env recipes build verbatim and resolve the tested versions", "PASS", "TOBIAS 0.17.5, samtools 1.19.2, RGT 1.0.2, pyDNase 0.3.0, scPrinter 1.2.0 + torch 2.11.0+cu128 CUDA true, tangermeme 0.4.4, snapatac2 2.8.0"),
             A("pip check is clean in the scPrinter env", "PASS", "No broken requirements found"),
             A("SKILL.md NFR filter count equals the independent samtools -e expectation with no |TLEN| >= 100", "PASS", "94,478 = 94,478; max 99; 0 violations"),
             A("alignmentSieve --ATACshift moves forward starts +4 and reverse ends -5", "PASS", "119,182/119,182 at +4; 118,152/119,182 at -5"),
             A("Excluded modes (single-cell/cluster scPrinter, seq2PRINT training, ChIP-anchored CTCF validation) are labelled untested", "PASS", "SKILL.md workflow step 3, usage-guide closing note, method-reference decision table")]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    assert 3 <= i["assertions_total"] <= 5
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap = sum(i["assertions_passed"] for i in inputs)
at = sum(i["assertions_total"] for i in inputs)
cats = {
    "functional_suitability": (10, 12, "TOBIAS, HINT-ATAC, Wellington and bulk scPrinter all have tested commands; single-cell scPrinter, seq2PRINT, PIQ and ChIP-anchored validation are labelled out of scope"),
    "reliability": (10, 12, "Input, glob, CTCF and quoting guards verified; the CTCF control cannot detect absent bias correction; scprinter script gives a raw traceback on a missing file"),
    "performance_context": (7, 8, "93-line SKILL.md with routed references; method reference is large but conditional"),
    "agent_usability": (14, 16, "Clear workflow, decision table and explicit limits; scPrinter recipe lines use bare pip without naming the environment"),
    "human_usability": (7, 8, "Natural request examples, documented exit codes and opt-out; positional-argument script"),
    "security": (11, 12, "No secrets or destructive operations; all expansions quoted and verified with spaces in paths"),
    "maintainability": (10, 12, "Provenance and MIT license preserved; tested versions and per-tool env recipes verified fresh; scPrinter pinned line needs a 30 min source build"),
    "agent_specific": (18, 20, "Description covers four tools and goals; scripts route from SKILL.md; version floors replaced by tested-with list")}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
rep = {
    "meta": {"skill_name": "bio-atac-seq-footprinting",
             "description": "Detect transcription factor binding footprints in ATAC-seq using TOBIAS, HINT-ATAC, Wellington, or scprinter. Use when identifying bound TF sites within accessible regions, correcting Tn5 insertion bias before footprinting, choosing between cleavage-based and aggregate-based footprinters, or comparing differential TF activity between conditions.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Moderate", "n_inputs": len(inputs)},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {"applicable": True, "gate": "PASS",
                          "scientific_integrity": {"result": "PASS", "detail": "Reported values reproduced independently (ranking, concordance, scPrinter statistics); measured numbers are labelled as chr1 low-depth observations."},
                          "practice_boundaries": {"result": "PASS", "detail": "Public ENCODE data; single-tool calls labelled exploratory; untested modes stated as untested."},
                          "methodological_ground": {"result": "PASS", "detail": "Bias-corrected footprinting is sound; the CTCF control's limits are disclosed (FOOT-008 residual, P2)."},
                          "code_usability": {"result": "PASS", "detail": "run_tobias.sh, site_concordance.sh and scprinter_footprint.py ran unmodified to rc 0 in fresh recipe environments."}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "All three initial P1 findings reproduce as fixed: the silent CTCF skip now exits 3 with an opt-out, the scPrinter bulk route runs from a shipped script, and the per-tool env recipes build fresh with the tested versions.",
        "Outputs were verified independently of the scripts: ranking, concordance and scPrinter bound-versus-unbound statistics were recomputed separately and matched.",
        "Limits are stated honestly: single-cell scPrinter, seq2PRINT training and ChIP-anchored validation are labelled untested, and the CTCF dip is described as not proving correction.",
        "Guards are meaningful: missing inputs, paths with spaces, ambiguous globs and empty call sets fail or succeed correctly."],
    "recommendations": [
        {"priority": "P2", "title": "CTCF control cannot detect absent bias correction", "observed_in": [3],
         "problem": "With corrected signal replaced by uncorrected signal the script exits 0 with no warning and the bound-site dip stays deep (7.14 vs 6.67); the guard only tests that a CTCF motif exists.",
         "root_cause": "The positive control is evaluated on sites selected by the same footprint score and gives no numeric corrected-versus-uncorrected criterion.",
         "fix": "Compare corrected against uncorrected at all CTCF sites and warn when the corrected flank-minus-core gain is absent, or state the expected contrast (about 2.5 uncorrected and 3.0 corrected at all sites in the chr1 test) beside the panel description."},
        {"priority": "P2", "title": "scPrinter recipe lines do not name the environment", "observed_in": [6],
         "problem": "The scPrinter block runs bare pip install lines after micromamba create, so a reader can install torch and scPrinter into the wrong active environment.",
         "root_cause": "The TOBIAS line uses micromamba run -n but the scPrinter lines rely on an implied activation.",
         "fix": "Prefix the two scPrinter pip lines with micromamba run -n footprint-scprinter or add an explicit activation line."},
        {"priority": "P2", "title": "scprinter_footprint.py fails with a raw traceback on a missing input", "observed_in": [5],
         "problem": "A missing fragment file exits rc 1 through a FileNotFoundError deep in scPrinter rather than a one-line message.",
         "root_cause": "Arguments are not checked before importing and calling scPrinter.",
         "fix": "Check that --fragments, --fasta, --gtf, --blacklist and --regions exist and exit 2 with a named message, as run_tobias.sh does."}]}
assert sub == sum(c["score"] for c in rep["static_score"]["categories"].values())
json.dump(rep, open(f"{R}/report.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
l1 = sum(i["basic"] for i in inputs) / len(inputs)
l2 = sum(i["specialized"] for i in inputs) / len(inputs)
print("static", sub, "exec", avg, "assert", ap, "/", at, "final", sw, dw, score, "L1", round(l1, 1), "L2", round(l2, 1), "rate", round(ap / at * 100, 1))
