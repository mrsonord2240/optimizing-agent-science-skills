"""Assemble report.json (skill-auditor@1.0 schema, same shape as the prior record) from the re-audit's scored inputs."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def A(text, note, result="PASS"):
    return {"text": text, "result": result, "note": note}


inputs = [
    dict(index=1, type="Canonical", label="run_tobias.sh unmodified, GM12878 vs K562 chr1:1-30 Mb, with the new bias check",
         status="COMPLETED", status_flag="✅",
         note="rc 0; bias check r(corrected, expected) -0.138 / -0.218 (pass); ranking equals independent pandas order; PDFs rendered and inspected",
         basic=37, specialized=53, assertions=[
             A("rc 0 with bigwigs, bindetect_results.txt and per-condition CTCF aggregate PDF and txt (uncorrected, expected, corrected x all, bound, unbound)", "9 profiles of 120 bp per condition; PDF rendered at 80 dpi, 4x4 grid legible"),
             A("Top-motif table equals an independent pandas ranking of |change| among p <= 0.05", "12 rows, IRF4 first, GATA1 second"),
             A("Direction of change matches biology: GATA1 < 0 (K562), IRF4 > 0 (GM12878)", "GATA1 -0.385, IRF4 +0.588"),
             A("Bias check passes on genuinely corrected signal in both conditions", "r(corrected, expected) -0.138 and -0.218 against a 0.2 ceiling; r(uncorrected, expected) 0.653 and 0.397"),
             A("Corrected CTCF profile dips at bound sites and is flat at unbound sites", "flank-minus-core bound 7.44 / 10.40 vs unbound 0.26 / 0.59 (513 bound, 690 unbound, 1203 all)")]),
    dict(index=2, type="Adversarial", label="Bias correction absent (corrected track replaced by uncorrected) at full depth, 20% depth and NFR-only fragments; threshold edge",
         status="COMPLETED", status_flag="✅",
         note="rc 4 in all three absent-correction runs, rc 0 in all three real runs; half-strength correction is not always caught (P2)",
         basic=36, specialized=52, assertions=[
             A("With the corrected track replaced by the uncorrected one the script exits 4 with a per-condition WARNING and an ERROR", "run N: r 0.653 / 0.397, rc 4; bound-site dip still as deep (8.11 vs 7.44), so the dip alone would not have caught it"),
             A("The check still fires on different uncorrected tracks: 20% subsample and NFR-only BAMs", "SN r 0.636 / 0.408 rc 4; FN r 0.583 / 0.362 rc 4"),
             A("No false alarm on real correction at 20% depth or on NFR-only fragments", "S -0.112 / -0.245 rc 0; F -0.161 / -0.254 rc 0"),
             A("The awk Pearson equals numpy and TOBIAS PlotAggregate's own correlation statistic", "12/12 values match to 3 decimals; PlotAggregate STATS 0.65299 and 0.39698"),
             A("Threshold semantics: r equal to BIAS_R_MAX passes, r above it fails, nan fails", "candidate's comparison code extracted and run: -0.138 vs -0.138 pass, vs -0.139 fail, nan fail")]),
    dict(index=3, type="Edge", label="Guards: no-CTCF motif set, missing BAM, scPrinter missing inputs and malformed --shift, empty call set",
         status="COMPLETED", status_flag="✅",
         note="rc 3, rc 2, rc 2 x3, rc 2; no output directory created by any rejected call",
         basic=36, specialized=52, assertions=[
             A("Motif set without CTCF exits 3 with WARNING and ERROR and still prints the differential table", "run X rc 3"),
             A("Missing BAM exits 2 before creating the output directory", "run M rc 2, outdir absent"),
             A("scprinter_footprint.py exits 2 with a named one-line message for a missing --fragments or --groups file", "rc 2, 'ERROR: input not found: --fragments nope.tsv.gz'; no outdir"),
             A("scprinter_footprint.py rejects a malformed --shift with rc 2", "message names the accepted forms 'auto' or 'PLUS,MINUS'"),
             A("site_concordance.sh rejects an empty call set", "rc 2, 'missing or empty: empty.bed'")]),
    dict(index=4, type="Variant B", label="SKILL.md HINT-ATAC and Wellington -A commands, site_concordance.sh against this run's TOBIAS calls",
         status="COMPLETED", status_flag="✅",
         note="HINT 358 footprints; concordance equals a pure-python recomputation and the reference's stated fractions; live envs (fingerprints unchanged), not rebuilt",
         basic=35, specialized=51, assertions=[
             A("rgt-hint command from SKILL.md runs to rc 0 with a scored footprint BED", "358 footprints in 60 peaks"),
             A("wellington_footprints.py -A runs to rc 0 and yields FDR footprints", "71-line FDR 0.01 BED, 45 unique inside the regions"),
             A("site_concordance.sh output equals an independent python interval-overlap recomputation", "HINT 58/143 bound, 0/31 unbound, 54/358 reverse; Wellington 16/143, 0/31, 13/45"),
             A("The reference's measured concordance values match", "41% and 15% (HINT), 12% and 29% (Wellington -A) reproduced"),
             A("Bound-site overlap is clearly above unbound-site overlap for both second call sets", "0.406 vs 0 and 0.112 vs 0")]),
    dict(index=5, type="Variant A", label="scPrinter bulk route and --shift guidance in a fresh usage-guide env (GPU)",
         status="COMPLETED", status_flag="✅",
         note="fresh env built from the extracted recipe lines; 0,0 for raw fragments confirmed by scPrinter source and its detector; contrast does not identify the right shift (P2)",
         basic=35, specialized=51, assertions=[
             A("The three scPrinter recipe lines, extracted verbatim, build a working env", "29 min; torch 2.11.0+cu128 CUDA true, scPrinter 1.2.0, tangermeme 0.4.4, snapatac2 2.8.0, pip check clean"),
             A("The usage-guide fragment recipe yields an indexed raw fragment file", "521,478 fragments, tabix ok"),
             A("Bulk run with default --shift 0,0 predicts Tn5 bias on GPU and writes finite scores regions x modes x width", "(400, 99, 200), rc 0, 7 min 53 s; center_by_mode.tsv equals an npz recomputation"),
             A("CTCF bound sites score above unbound at modes 10-30 and not at 50, as SKILL.md states", "0.659/0.378 (p 2e-16), 1.562/0.501 (p 1e-12), 0.754/0.335 (p 1e-6); mode 50 0.095/0.188"),
             A("--shift guidance is correct: 0,0 for raw BAM fragments, 4,-5 for Cell Ranger", "scPrinter 1.2.0 documents plus/minus_shift as the shift already done and adds 4-plus / -5-minus; detect_shift returned (0, 0) on the raw fragments")]),
    dict(index=6, type="Stress", label="scPrinter per-cluster mode (--groups) on 10x PBMC 5k and a bounded seq2PRINT training run",
         status="COMPLETED", status_flag="✅",
         note="cluster mode rc 0 with documented numbers reproduced exactly; seq2PRINT rc 0 in 29 min with a weak model, as the guide says; LoRA mode not run (resource-infeasible, labelled)",
         basic=34, specialized=50, assertions=[
             A("The usage-guide per-cluster command runs to rc 0 and writes finite scores regions x groups x modes x width", "(400, 5, 4, 200); 697 cells in 5 clusters of 49-198, 0 dropped; 1 min 21 s with an existing bias file"),
             A("The guide's per-cluster numbers reproduce on its region set", "bound > unbound in 20/20 cells, 1 with p < 0.05, cross-cluster r 0.04-0.59; on this audit's own region sample 17/20 and 2, same conclusion"),
             A("--shift auto on the sparse 10x fragments gives the implausible shift the guide warns about", "detected 22 / 12 with a low-confidence warning"),
             A("The seq2PRINT blocks, extracted verbatim with only path and split substitutions, run to rc 0 inside the 45 min cap", "prep 2.5 min, 12,579 cleaned peaks; train plus attribution 29 min 20 s; GPU peak 15.8 of 16.3 GB"),
             A("The seq2PRINT text claims only what ran: model saved with finite parameters and a 99 x 800 output, attribution bigwigs written, model not usable", "11,756,644 finite params, forward (2, 99, 800); 2 DeepSHAP bigwigs; best validation profile Pearson 0.032")]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
n = len(inputs)
avg = round(sum(i["total"] for i in inputs) / n, 1)
cats = {
    "functional_suitability": (11, 12, "TOBIAS, HINT-ATAC, Wellington, bulk and per-cluster scPrinter and seq2PRINT training all have executed commands; LoRA single-cell seq2PRINT and PIQ are labelled not run"),
    "reliability": (11, 12, "Input, glob, CTCF, bias-correction and scPrinter argument guards all verified; the bias check catches absent but not always half-strength correction"),
    "performance_context": (7, 8, "95-line SKILL.md with routed references; the usage guide grew to hold the seq2PRINT recipe but stays conditional"),
    "agent_usability": (15, 16, "Clear workflow, exit codes and limits; --shift is explained by fragment provenance; no warning that contrast cannot be used to pick the shift"),
    "human_usability": (7, 8, "Natural request examples, documented exit codes and opt-outs; positional-argument TOBIAS script"),
    "security": (11, 12, "No secrets or destructive operations; quoted expansions; inputs checked before use"),
    "maintainability": (10, 12, "Provenance and MIT license preserved; tested versions recorded; the scPrinter pin set needs a 30 min source build"),
    "agent_specific": (18, 20, "Description covers the four tools; scripts and references routed from SKILL.md; stop conditions for missing control and failed bias check"),
}
static = sum(v[0] for v in cats.values())
report = {
    "meta": {
        "skill_name": "bio-atac-seq-footprinting",
        "description": "Detect transcription factor binding footprints in ATAC-seq using TOBIAS, HINT-ATAC, Wellington, or scprinter. Use when identifying bound TF sites within accessible regions, correcting Tn5 insertion bias before footprinting, choosing between cleavage-based and aggregate-based footprinters, or comparing differential TF activity between conditions.",
        "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
        "execution_mode": "D", "complexity": "Moderate", "n_inputs": n},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Every measured value quoted in the Skill that was re-run reproduced (bias-check correlations, concordance fractions, scPrinter contrasts, per-cluster counts, seq2PRINT run facts); values are labelled as chr1 low-depth observations."},
            "practice_boundaries": {"result": "PASS", "detail": "Public ENCODE and 10x data; single-tool calls labelled exploratory; per-cluster and seq2PRINT results labelled as route checks, not usable results."},
            "methodological_ground": {"result": "PASS", "detail": "The positive control now tests bias correction on sites not selected by footprint score; absent correction exits 4 in all three absent-correction runs; the limits of the check are a P2."},
            "code_usability": {"result": "PASS", "detail": "run_tobias.sh, site_concordance.sh, scprinter_footprint.py and the usage-guide seq2PRINT blocks ran unmodified to their documented exit codes."}}},
    "static_score": {"subtotal": static, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {
        "execution_avg": avg, "max": 100,
        "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
        "inputs": inputs},
    "final": {"static_weighted": round(static * 0.4, 1), "dynamic_weighted": round(avg * 0.6, 1),
              "score": int(round(static * 0.4 + avg * 0.6)), "max": 100,
              "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The redesigned CTCF control does what it says: it exits 4 when bias correction is absent and 0 when it is real, at full depth, at 20% depth and on NFR-only fragments.",
        "The bias statistic is verifiable three ways: the script's awk, numpy on the same profile, and TOBIAS PlotAggregate's own correlation all agree.",
        "Per-cluster scPrinter and seq2PRINT text claims only what ran; the guide's numbers reproduced exactly and both are labelled as not resolving or not usable at the tested depth.",
        "The --shift guidance matches scPrinter's source and its own shift detector for raw fragments, and the guide's warning about auto-detection on sparse 10x fragments reproduced.",
        "All three prior P2 findings are fixed: bias check added, scPrinter recipe names its environment, missing inputs exit 2 with a one-line message."],
    "recommendations": [
        {"priority": "P2", "title": "Bias check catches absent correction, not always partial correction",
         "observed_in": [2],
         "problem": "Removing only part of the expected bias from the uncorrected aggregate passes the check once 40% (K562) or 60% (GM12878) is removed. Uncorrected r was as low as 0.362 (K562, NFR fragments), 0.16 above the 0.2 ceiling, and an independent pyBigWig aggregation of the same tracks gave 0.31. The default rests on two libraries.",
         "root_cause": "A single Pearson ceiling is applied to the corrected profile without reference to how strongly the uncorrected profile followed the bias.",
         "fix": "In references/method-reference.md state that the check detects absent, not under-strength, correction and that 0.2 was set on GM12878 and K562. In scripts/run_tobias.sh warn that the check is uninformative when r(uncorrected, expected) is itself at or below BIAS_R_MAX."},
        {"priority": "P2", "title": "No warning that bound-versus-unbound contrast cannot pick the scPrinter shift",
         "observed_in": [5],
         "problem": "On raw BAM fragments the wrong setting (--shift 4,-5) gave a larger CTCF bound-minus-unbound centre score than the correct 0,0 (mode 10: 0.629 vs 0.281; mode 30: 0.663 vs 0.419). A reader who tries both and keeps the stronger contrast would pick the wrong shift.",
         "root_cause": "The usage guide says which shift fits which fragment source but not how to tell when it is wrong.",
         "fix": "Add one sentence to the fragment section of references/usage-guide.md: set --shift from how the fragments were made, never from which setting gives the stronger contrast; the wrong shift scored higher in the tested slice."}],
}
with open(os.path.join(R, "report.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
    f.write("\n")
l1 = sum(i["basic"] for i in inputs) / n
l2 = sum(i["specialized"] for i in inputs) / n
print("static", static, "exec avg", avg, "final", report["final"]["score"], "L1", round(l1, 1), "L2", round(l2, 1), report["dynamic_score"]["assertion_pass_rate"])
