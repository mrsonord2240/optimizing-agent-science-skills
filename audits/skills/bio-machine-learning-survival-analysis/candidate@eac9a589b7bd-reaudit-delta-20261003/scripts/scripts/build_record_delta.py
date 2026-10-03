import json, hashlib, os
R = r"F:\OpenScience\audits\bio-machine-learning-survival-analysis\reaudit-delta-20261003"
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis"
IDENT = "eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb"
CERT = r"F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-survival-analysis\candidate@c60f873f52f6-reaudit-lane3b-20261003"
files = []
for dp, dn, fn in os.walk(SK):
    for f in fn:
        p = os.path.join(dp, f)
        b = open(p, "rb").read()
        files.append({"path": os.path.relpath(p, SK).replace("\\", "/"), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x["path"])
assert len(files) == 5 and sum(f["bytes"] for f in files) == 34007
sid = json.load(open(os.path.join(CERT, "source-identity.json"), encoding="utf-8"))
sid["candidate"]["content_sha256"] = IDENT
sid["candidate"]["content_manifest"] = {"file_count": 5, "bytes": 34007}
sid["files"] = files
sid["prior_audit"] = {"identity": "c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39", "path": CERT, "score": 86, "grade": "Production Ready"}
sid["delta"] = {
    "mode": "text-only delta re-audit",
    "qualification": "Four of five files (references/failure-modes.md, both scripts, usage-guide.md) are byte-identical to the certified per-file sha256 values; only SKILL.md differs (20410 to 20526 bytes), one Common Errors table row per the fix log. The pre-fix SKILL.md bytes were not retained anywhere, so the scratch-copy revert could not be reproduced by hash; instead both SKILL.md python blocks were run verbatim and give the certified numbers.",
    "fix_log": r"F:\OpenScience\audits\bio-machine-learning-survival-analysis\fix-textbatch-20261003\fix-log.md",
}
json.dump(sid, open(os.path.join(R, "source-identity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

rep = json.load(open(os.path.join(CERT, "report.json"), encoding="utf-8"))
rep["meta"]["performed_by"] = "Claude (Anthropic) delta re-audit worker D2"
rep["meta"]["auditor_independent"] = True
ins = rep["dynamic_score"]["inputs"]
inp = ins[3]
inp["note"] = inp["note"].replace("One wording inaccuracy found (SA-006).", "SA-006 wording reinspected in delta: the reworded row matches the measured sksurv behaviour for both cumulative_dynamic_auc and integrated_brier_score.")
done = False
for a in inp["assertions"]:
    if a["text"].startswith("Common Errors row on time-grid range"):
        a["text"] = "Common Errors row on time-grid range states the actual sksurv limit (SA-006)"
        a["result"] = "PASS"
        a["note"] = "Row now says a time at or above the largest test time of any status errors and times below it are accepted. Measured on GBSG2 (largest test time 2556 censored, largest uncensored 2093): AUC and IBS run at t=2092, 2324 and 2555; AUC and IBS both raise ValueError at 2556 and 2566"
        done = True
assert done
inp["specialized"] += 1
inp["assertions_passed"] = sum(a["result"] == "PASS" for a in inp["assertions"])
for i in ins:
    i["total"] = i["basic"] + i["specialized"]
avg = round(sum(i["total"] for i in ins) / len(ins), 1)
ap = {"passed": sum(i["assertions_passed"] for i in ins), "total": sum(i["assertions_total"] for i in ins)}
rep["dynamic_score"]["execution_avg"] = avg
rep["dynamic_score"]["assertion_pass_rate"] = ap
cat = rep["static_score"]["categories"]["reliability"]
cat["score"] += 1
cat["note"] = "Hard failures from sksurv are informative and the Common Errors table covers the main traps, with the time-range row now accurate (SA-006 resolved); scripts do no explicit input or time-range validation."
sub = sum(c["score"] for c in rep["static_score"]["categories"].values())
rep["static_score"]["subtotal"] = sub
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
rep["final"].update({"static_weighted": sw, "dynamic_weighted": dw, "score": score})
rep["recommendations"] = []
json.dump(rep, open(os.path.join(R, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
l1 = sum(i["basic"] for i in ins) / len(ins)
l2 = sum(i["specialized"] for i in ins) / len(ins)
print(sub, avg, l1, l2, sw, dw, score, ap)
assert sub >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and score >= 85 and ap["passed"] / ap["total"] >= .9

V = """# Eval Viewer - bio-machine-learning-survival-analysis

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes), lane D2
Exact candidate content SHA-256: `@IDENT@` (5 files, 34007 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `c60f873f52f6` (86, Production Ready), record `candidate@c60f873f52f6-reaudit-lane3b-20261003`
Scores carry forward from the certified report; only the reliability category and the one assertion touched by the change were re-scored.

## Result

**Static @SUB@/100; Execution average @AVG@/100; Final @FIN@ (@SCORE@); assertion pass rate @AP@; Layer 1 @L1@/40; Layer 2 @L2@/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `eac9a589b7bd`. No open finding remains from the certified record.

## Delta qualification

- Four files (references/failure-modes.md, scripts/competing_risks_cif.py, scripts/cox_regression.py, usage-guide.md) are byte-identical to the certified per-file sha256 values. Only SKILL.md differs (20410 to 20526 bytes); no script or executable statement changed.
- Limitation: the pre-fix SKILL.md bytes were not retained anywhere (no copy of sha256 81ae775e... found under the OpenScience or records trees), so the scratch-copy revert to the certified identity could not be reproduced. The fix log's single-row claim is therefore corroborated by the size delta (+116 bytes, one table row) and by the verbatim run of both SKILL.md python blocks, which reproduce the certified output exactly (alpha 0.3968, 3 of 9 nonzero; Uno C 0.669, mean AUC 0.728, IBS 0.161 vs KM 0.178; scripts/rd_run_skill_snippets.py).

## Changed claim versus measured values

Row: "`times` for AUC/IBS out of range - a time at or above the largest test time of any status (censored or not); times below it are accepted, even past the largest uncensored time - Keep `times` strictly below the largest test time".

GBSG2, stratified 70/30 split, seed 0: largest test time 2556 (censored), largest uncensored 2093.

| Grid end t | cumulative_dynamic_auc | integrated_brier_score |
|---|---|---|
| 2092 (below largest uncensored) | 0.738 | 0.207 |
| 2324 (past largest uncensored) | 0.742 | 0.211 |
| 2555 (one below max) | 0.749 | 0.209 |
| 2556 (max, censored) | ValueError [8; 2556[ | ValueError [8; 2556[ |
| 2566 | ValueError | ValueError |

Verdict: the row is correct for both metrics. Untested corner: a largest test time that is an event (the error message and bound are generic for test follow-up).

## Finding dispositions

| ID | Verdict |
|---|---|
| SA-006 | resolved |
| SA-001 to SA-005 | unchanged, resolved in the certified record |

No open finding remains.

## Not executed

Unchanged from the certified record: Fine-Gray, CIF Brier, randomForestSRC, landmarking, calibration curves, nested CV, boosting, survival SVM, Cox-Time (the Skill labels them not bundled or not executed). pycox and the scripts were not re-run (bytes unchanged).

## Evidence

Run root `F:\\OpenScience\\audits\\bio-machine-learning-survival-analysis\\reaudit-delta-20261003\\` (scripts/rd_times_range.py, rd_run_skill_snippets.py; logs/). Environment: survival-venv, scikit-survival 0.28.0, unchanged per TOOLS.md.
"""
for k, v in {"@IDENT@": IDENT, "@SUB@": str(sub), "@AVG@": str(avg), "@FIN@": f"{sw + dw:.1f}", "@SCORE@": str(score),
             "@AP@": f"{ap['passed']}/{ap['total']}", "@L1@": f"{l1:.1f}", "@L2@": f"{l2:.1f}"}.items():
    V = V.replace(k, v)
open(os.path.join(R, "viewer.md"), "w", encoding="utf-8").write(V)
