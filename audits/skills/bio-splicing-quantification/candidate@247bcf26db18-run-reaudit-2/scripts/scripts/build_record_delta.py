import json, hashlib, os
R = r"F:\OpenScience\audits\bio-splicing-quantification\run-reaudit-2"
SK = r"F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification"
IDENT = "247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc"
CERT = r"F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@0c0354add99b-run-reaudit-1"
files = []
for dp, dn, fn in os.walk(SK):
    for f in fn:
        p = os.path.join(dp, f)
        b = open(p, "rb").read()
        files.append({"path": os.path.relpath(p, SK).replace("\\", "/"), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x["path"])
assert len(files) == 5 and sum(f["bytes"] for f in files) == 42306
sid = json.load(open(os.path.join(CERT, "source-identity.json"), encoding="utf-8"))
sid["candidate"]["content_sha256"] = IDENT
sid["candidate"]["content_manifest"] = {"file_count": 5, "bytes": 42306, "recipe": sid["candidate"]["content_manifest"]["recipe"]}
sid["candidate"]["status_after_execution"] = "untracked Skill subtree only; candidate files unchanged (identity re-verified with skill_preflight --offline before and after)"
sid["files"] = files
sid["prior_audit"] = {"identity": "0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf", "run": "run-reaudit-1", "path": CERT, "score": 85, "grade": "Production Ready"}
sid["delta"] = {
    "mode": "text-only delta re-audit",
    "qualification": "Only SKILL.md differs from the certified per-file sha256 values (4 other files byte-identical, including scripts/quantify_splicing.py). Reversing the one SQ-13 sentence on a scratch copy reproduces SKILL.md sha256 899e98ff33a29a8749b04c17da24116d80a409b0b6870e8f6dd474af444b622f exactly (certified size 23344 bytes).",
    "fix_log": r"F:\OpenScience\audits\bio-splicing-quantification\fix-textbatch-20261003\fix-log.md",
}
json.dump(sid, open(os.path.join(R, "source-identity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

rep = json.load(open(os.path.join(CERT, "report.json"), encoding="utf-8"))
rep["meta"]["performed_by"] = "Claude (Anthropic) delta re-audit worker D2"
ins = rep["dynamic_score"]["inputs"]
inp = ins[1]
inp["note"] += "; delta re-check of the reworded SQ-13 sentence on the same real rMATS output: 719 of 958 SE rows 148/74, max 148/74, formula still reproduces IncLevel (maxabs 0.0005)"
inp["assertions"][4] = {
    "text": "SKILL.md states JC IncFormLen/SkipFormLen as maxima and tells the reader to use the per-event values (SQ-13)",
    "result": "PASS",
    "note": "text now says maxima 2*(readLength-1) and readLength-1, 719 of 958 chrX SE rows 148/74, use per-row lengths; counts reproduced from the real JC file (max 148/74, 58 distinct pairs)"}
inp["assertions"].append({
    "text": "The condition given for reaching the maxima is exact",
    "result": "FAIL",
    "note": "text says maxima are 'reached only for exons at least read-length long; short exons shorten them'; on the real file SkipFormLen is 74 in all 958 rows including a 1 nt exon, and a 74 nt exon (below read length 75) already gives 148 (SQ-14)"})
inp["specialized"] = 53
inp["assertions_passed"] = 5
inp["assertions_total"] = 6
for i in ins:
    i["total"] = i["basic"] + i["specialized"]
avg = round(sum(i["total"] for i in ins) / len(ins), 1)
ap = {"passed": sum(i["assertions_passed"] for i in ins), "total": sum(i["assertions_total"] for i in ins)}
rep["dynamic_score"]["execution_avg"] = avg
rep["dynamic_score"]["assertion_pass_rate"] = ap
sub = rep["static_score"]["subtotal"]
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
rep["final"].update({"static_weighted": sw, "dynamic_weighted": dw, "score": score})
fs = rep["static_score"]["categories"]["functional_suitability"]
fs["note"] = fs["note"].replace("JC length statement is exact only for typical events (SQ-13)", "JC length statement now states maxima and per-event use (SQ-13 resolved), with one imprecise condition clause (SQ-14)")
rep["recommendations"] = [r for r in rep["recommendations"] if "(SQ-13)" not in r["fix"]]
rep["recommendations"].append({
    "priority": "P2",
    "title": "SQ-13 rewording gives an inexact condition for the maxima",
    "observed_in": [2],
    "problem": "SKILL.md says IncFormLen/SkipFormLen maxima are 'reached only for exons at least read-length long; short exons shorten them'. On the real chrX JC file SkipFormLen is 74 in all 958 rows (a 1 nt exon included), and exons of 74 nt (readLength - 1) already reach 148.",
    "root_cause": "The exon-length condition belongs to IncFormLen alone and its threshold is readLength - 1, not readLength.",
    "fix": "Say 'IncFormLen reaches 2*(readLength - 1) for exons of at least readLength - 1 nt; SkipFormLen was readLength - 1 in every SE row here'. Text only. The operative advice (use the per-row lengths) is correct. (SQ-14)"})
json.dump(rep, open(os.path.join(R, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
l1 = sum(i["basic"] for i in ins) / 7
l2 = sum(i["specialized"] for i in ins) / 7
print(sub, avg, l1, l2, sw, dw, score, ap)
assert sub >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and score >= 85 and ap["passed"] / ap["total"] >= .9

V = """# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes), lane D2
Exact candidate content SHA-256: `@IDENT@` (5 files, 42306 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `0c0354add99b` (85, Production Ready), record `candidate@0c0354add99b-run-reaudit-1`
Scores carry forward from the certified report; only the dimension and assertions touched by the change were re-scored.

## Result

**Static @SUB@/100; Execution average @AVG@/100; Final @FIN@ (@SCORE@); assertion pass rate @AP@; Layer 1 @L1@/40; Layer 2 @L2@/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `247bcf26db18`. The margin over the 85 gate remains narrow.

## Delta qualification

- Per-file sha256 against the certified source-identity: `references/failure-modes-and-errors.md`, `references/intron-retention-and-microexons.md`, `scripts/quantify_splicing.py` and `usage-guide.md` are byte-identical; only `SKILL.md` differs (23344 to 23571 bytes). No script or executable statement changed.
- Reversing the single SQ-13 sentence on a scratch copy reproduces SKILL.md sha256 `899e98ff...b622f` exactly, so the whole diff is that one sentence.
- The SKILL.md python block was re-run verbatim on the real rMATS JC output: 958 SE events, 20 reliable, rc 0 (scripts/rd_snippet_and_forms.py).

## Changed claim versus measured values

| Claim in new text | Measured (real chrX JC SE, rMATS 4.4.0, readLength 75; planted readLength 50) | Verdict |
|---|---|---|
| maxima 2*(readLength-1) and readLength-1; 98/49 at 50, 148/74 at 75 | planted 98/49; real max IncFormLen 148, max SkipFormLen 74 | correct |
| 719 of 958 chrX SE rows are 148/74 | 719 of 958 (58 distinct pairs) | correct |
| use the per-event lengths in each row | formula with row lengths reproduces IncLevel, maxabs 0.0005 over 1465 values (JC), 1549 (JCEC) | correct |
| JCEC adds exon-body positions (149 for the 100 nt planted exon) | planted JCEC 149/49 | correct, unchanged |
| PSI = (IJC/IncFormLen)/(IJC/IncFormLen + SJC/SkipFormLen) | same reproduction | still correct |
| maxima "reached only for exons at least read-length long; short exons shorten them" | SkipFormLen 74 in 958/958 rows incl. a 1 nt exon; a 74 nt exon gives 148; 710 exons of at least 75 nt all give 148 | inexact (SQ-14) |

## Finding dispositions

| ID | Verdict |
|---|---|
| SQ-13 | resolved: constants claim replaced by maxima plus per-event guidance |
| SQ-14 (P2, new, text only) | open: condition clause is inexact for SkipFormLen and off by one for IncFormLen |
| SQ-12 (P2) | open, untouched: header-only rMATS file raises KeyError in parse_rmats_output (script unchanged) |

All other certified dispositions (SQ-01 to SQ-11) are unchanged; no other part of SKILL.md changed.

## Not executed

Unchanged from the certified record: MAJIQ V3/VOILA, VAST-TOOLS, Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0; the Skill labels each as not executed. The IRFinder smoke was not run (not needed for a prose change).

## Evidence

Run root `F:\\OpenScience\\audits\\bio-splicing-quantification\\run-reaudit-2\\` (scripts/rd_snippet_and_forms.py, logs/rd_snippet_and_forms.log). The rMATS outputs of `run-reaudit-1\\out` were reused as inputs (Skill scripts and rMATS version unchanged).
"""
for k, v in {"@IDENT@": IDENT, "@SUB@": str(sub), "@AVG@": str(avg), "@FIN@": f"{sw + dw:.1f}", "@SCORE@": str(score),
             "@AP@": f"{ap['passed']}/{ap['total']}", "@L1@": f"{l1:.1f}", "@L2@": f"{l2:.1f}"}.items():
    V = V.replace(k, v)
open(os.path.join(R, "viewer.md"), "w", encoding="utf-8").write(V)
