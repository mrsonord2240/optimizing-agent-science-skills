import json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


def inp(i, typ, label, status, note, b, s, asr):
    p = sum(a["result"] == "PASS" for a in asr)
    tot = b + s
    flag = "❌" if status in ("PARTIAL", "ERROR") or any(a["result"] == "FAIL" for a in asr) else ("✅" if tot >= 75 else "⚠️")
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note,
            "basic": b, "specialized": s, "total": tot, "assertions": asr, "assertions_passed": p, "assertions_total": len(asr)}


inputs = [
    inp(1, "Canonical", "Usage-guide example verbatim: run_abc.sh, K562 chr22, real ENCODE Hi-C ENCFF621AIY read remotely (HIC_TYPE=hic)", "COMPLETED",
        "rc=0 end to end on ABC main 92ac503. 1,674,535 all-putative rows, 1,353 links at threshold 0.027, identical to ABC's shipped expected tables (ABC.Score max diff 0).", 39, 58, [
            A("run_abc.sh completes (rc=0) using only the documented environment variables and writes the predictions tables", "PASS", "rc=0; AllPutative, NonExpressed, threshold tables present"),
            A("Row counts and ABC.Score equal ABC's shipped expected output for the same inputs", "PASS", "1,674,535 rows; max abs ABC.Score diff 0.00e+00; 1,353 thresholded links"),
            A("ABC.Score equals Numerator/sum per (gene,TSS); self-promoters score 1; distance <= 5 Mb", "PASS", "max err 5.1e-07"),
            A("Calibrated threshold looked up from abc_thresholds.tsv (DHS, H3K27ac, intact_hic = 0.027) and applied", "PASS", "file name threshold0.027; all thresholded scores >= 0.027"),
            A("Candidate regions follow ABC (summit +/- 250 bp, blocklist, TSS regions kept) and non-self promoters are removed after scoring", "PASS", "17,732 candidates, median 500 bp; no non-self promoter link in thresholded table")]),
    inp(2, "Variant A", "run_abc.sh no-Hi-C powerlaw contact (HIC_TYPE=none), K562 chr22, with H3K27ac", "COMPLETED",
        "rc=0. Score column powerlaw.Score; threshold 0.017 from the table; 1,674,535 rows; 2,340 links.", 38, 54, [
            A("Script runs to completion with HIC_TYPE=none and no Hi-C file", "PASS", "rc=0"),
            A("Score column is powerlaw.Score, in [0,1], equal to Numerator/sum, self-promoters 1", "PASS", "max err 5.7e-07"),
            A("Threshold 0.017 (DHS, TRUE, powerlaw) selected from the table", "PASS", "threshold0.017 file, all scores >= 0.017"),
            A("Thresholded table equals an independent filter of AllPutative + NonExpressed (non-self promoters removed)", "PASS", "2,340 == 2,340")]),
    inp(3, "Variant A", "run_abc.sh accessibility-only (ACCESS_TYPE=ATAC on the DNase BAM, no H3K27ac, powerlaw); mechanics only", "COMPLETED",
        "rc=0. Threshold 0.013 (ATAC, FALSE, powerlaw); 1,675,272 rows; 3,462 links; no H3K27ac columns. The assay label is nominal (same BAM), so values are mechanics-only.", 37, 53, [
            A("Runs with H3K27AC_BAM unset and writes tables", "PASS", "rc=0"),
            A("No H3K27ac columns in the prediction tables", "PASS", "columns checked"),
            A("Threshold 0.013 is selected for ATAC without H3K27ac", "PASS", "threshold0.013; scores >= 0.013"),
            A("Thresholded table equals independent filter", "PASS", "3,462 == 3,462")]),
    inp(4, "Variant B", "run_abc.sh with PEAKS= from MACS3 3.0.4 (documented macs2-shim alternative), powerlaw", "COMPLETED",
        "rc=0. The MACS3 peaks route yields 17,732 candidates, the same count as the macs2 route, and identical row counts.", 36, 52, [
            A("PEAKS= route skips macs2 and completes", "PASS", "rc=0"),
            A("Candidate set matches the macs2 route (17,732; median 500 bp)", "PASS", "identical count"),
            A("Scores and thresholded table satisfy the same invariants as the macs2 route", "PASS", "2,340 links at 0.017; Numerator invariant max err 5.7e-07")]),
    inp(5, "Variant B", "run_abc.sh HIC_TYPE=avg on a SUBSTITUTE avg-format directory (real K562 chr22 Hi-C, not the cross-cell-type ENCFF134PUN average)", "COMPLETED",
        "rc=0. Mechanics of the avg branch only (hic_dir/chrN/chrN.bed.gz, gamma/scale, avg threshold row 0.016). The real 58 GB ENCODE average was not fetched (B-1, resource-infeasible); avg on real data is not counted as executed. The Skill states the 58 GB requirement and does not claim it was run.", 34, 50, [
            A("avg branch completes and writes predictions using the documented directory layout", "PASS", "rc=0; 1,731,043 rows"),
            A("Threshold row for avg (0.016) is used", "PASS", "threshold0.016"),
            A("Score invariants and thresholded table hold", "PASS", "max err 5.0e-07; 2,246 == 2,246"),
            A("Scientific validity of the avg branch on the real cross-cell-type average Hi-C is demonstrated", "FAIL", "not executed: ENCFF134PUN (58 GB) infeasible here; the substitute is same-cell-type Hi-C and proves mechanics only")]),
    inp(6, "Edge", "run_abc.sh on the ABC v1.1.2 tag (script header says tested on v1.1.2 and main), powerlaw", "COMPLETED",
        "rc=0 and scores correct (same counts and invariants), but v1.1.2's abc_thresholds.tsv has CRLF line endings, so THRESHOLD carries a carriage return and every threshold output is named EnhancerPredictionsFull_threshold0.017<CR>.tsv.", 33, 47, [
            A("Runs to completion on v1.1.2", "PASS", "rc=0; 1,674,535 rows; invariants pass"),
            A("Thresholded values correct on v1.1.2", "PASS", "2,340 links, all >= 0.017, non-self promoters removed"),
            A("Threshold value read from the table is clean and produces valid output file names", "FAIL", "file name contains a carriage return; the awk lookup does not strip CR (EGL-013)"),
            A("Calibrated threshold lookup selects the right row on v1.1.2", "PASS", "0.017 for DHS/TRUE/powerlaw")]),
    inp(7, "Canonical", "scripts/combine_predictions.py on my usage-example ABC output x upstream ENCODE-rE2G K562 chr22 (7,218 links); HiChIP flag on SYNTHETIC loops with planted truth", "COMPLETED",
        "rc=0. 939 shared links equal an independently computed (name,TargetGene) intersection; both scores in range and above their calibrated cut-offs. Synthetic loops (planted truth): 5/5 planted supported incl. reversed orientation, 0/3 decoys, 2 extras that share the enhancer or gene with a planted link. Missing required argument exits 2.", 38, 55, [
            A("Runs on real ABC and real rE2G tables with their real column keys", "PASS", "rc=0; ABC 1,353, rE2G 7,218"),
            A("Intersection equals an independently computed set and carries the rE2G score correctly", "PASS", "939 == 939; score max diff < 1e-9"),
            A("Scores lie in [0,1] and above the calibrated ABC (0.027) and rE2G (0.243) cut-offs", "PASS", "asserted"),
            A("HiChIP flag finds planted loops in either orientation and no decoys (synthetic truth)", "PASS", "5/5 planted, 0/3 decoys; 2 extras share enhancer or gene"),
            A("Missing required argument fails with a clear message", "PASS", "argparse error, rc=2")]),
    inp(8, "Adversarial", "run_abc.sh input guards: missing ABC_REPO, hic without HIC_FILE, HIC_FILE with HIC_TYPE=none, bad ACCESS_TYPE, bad HIC_TYPE, non-ABC repo", "COMPLETED",
        "All six invalid combinations exit non-zero (1 or 2) before any computation, with a message naming the problem.", 37, 53, [
            A("Missing ABC_REPO stops with a named message", "PASS", "rc=1 'set ABC_REPO'"),
            A("Contradictory Hi-C settings (hic without file, file with none, unknown type) are refused", "PASS", "rc=1/2 with messages"),
            A("Invalid ACCESS_TYPE is refused rather than silently defaulted", "PASS", "rc=2"),
            A("A directory that is not an ABC clone is refused", "PASS", "rc=2, no predict.py")]),
]
ex = [i["total"] for i in inputs]
avg = round(sum(ex) / len(ex), 1)
cats = {
    "functional_suitability": (11, 12, "Matched-Hi-C, powerlaw, accessibility-only and avg-mechanics paths execute; thresholds and rE2G routing accurate; juicebox/bedpe branches and real avg Hi-C unexecuted"),
    "reliability": (10, 12, "Input guards fail fast with messages; reruns match ABC's own tables; ABC v1.1.2 CRLF threshold file leaves CR in output names (EGL-013)"),
    "performance_context": (7, 8, "Lean SKILL.md with detail routed to two references; method-reference prose is dense"),
    "agent_usability": (14, 16, "Clear method table, documented env vars, tested example with expected counts; macs2 shim knowledge lives only in the usage guide"),
    "human_usability": (7, 8, "Natural request examples and a copy-paste example that reproduces the ABC chr22 result"),
    "security": (11, 12, "Variables quoted, no destructive commands; remote Hi-C URL and git clones are unauthenticated downloads without checksums"),
    "maintainability": (10, 12, "Parameterised script with documented header and a real-key combine script; no shipped tests; upstream layout drift is a standing risk"),
    "agent_specific": (17, 20, "Routing and provenance good; stale claims removed; description is long; avg branch on real data is labelled unexecuted"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
P = sum(i["assertions_passed"] for i in inputs)
T = sum(i["assertions_total"] for i in inputs)
report = {
    "meta": {"skill_name": "bio-atac-seq-enhancer-gene-linking",
             "description": "Predict enhancer-gene regulatory connections from ATAC-seq using ABC, ENCODE-rE2G, HiChIP, or Cicero; choose contact-aware, accessibility-only or orthogonal approaches, threshold and validate predictions.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "B", "complexity": "Complex", "n_inputs": len(inputs)},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; the avg-Hi-C branch is labelled as run on a same-cell-type substitute and the real 58 GB average as not executed; synthetic HiChIP loops are labelled with planted truth."},
            "practice_boundaries": {"result": "PASS", "detail": "Predictions are framed as hypotheses; therapeutic nomination requires two methods plus CRISPRi validation."},
            "methodological_ground": {"result": "PASS", "detail": "Outputs reproduce ABC's own expected tables exactly; candidate regions, quantile normalisation, calibrated thresholds and promoter handling now follow ABC."},
            "code_usability": {"result": "PASS", "detail": "run_abc.sh and combine_predictions.py run end to end on real K562 chr22 inputs; the prior P0 crash does not reproduce."}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": P, "total": T}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
              "grade": "Production Ready" if score >= 85 else "Limited Release",
              "grade_symbol": "⭐" if score >= 85 else "✅", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The prior P0 is fixed: the documented usage example runs end to end in one command and reproduces ABC's own chr22 K562 tables exactly (1,674,535 rows, 1,353 links at 0.027).",
        "Hi-C, powerlaw, accessibility-only, MACS3-peaks and avg-mechanics branches execute with calibrated thresholds and correct promoter handling; the avg branch is honestly labelled as run on a substitute.",
        "combine_predictions.py uses the real column keys and detects planted HiChIP loops in both orientations without decoys.",
        "Fail-fast input guards and routed references keep SKILL.md lean and consistent with executed behaviour."],
    "recommendations": [{
        "priority": "P2", "title": "CR left in threshold on ABC v1.1.2 (CRLF table)", "observed_in": [6],
        "problem": "On the v1.1.2 tag abc_thresholds.tsv has CRLF endings, so the awk lookup keeps a carriage return and output files are named threshold0.017<CR>.tsv; scores are still correct.",
        "root_cause": "The awk lookup prints field 4 without stripping CR, while the header claims v1.1.2 is tested.",
        "fix": "Pipe the lookup through tr -d '\\r' and rerun the v1.1.2 powerlaw case. (EGL-013)"}],
}
json.dump(report, open(os.path.join(R, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(sub, avg, sw, dw, score, P, T, sum(i["basic"] for i in inputs) / 8, sum(i["specialized"] for i in inputs) / 8)
