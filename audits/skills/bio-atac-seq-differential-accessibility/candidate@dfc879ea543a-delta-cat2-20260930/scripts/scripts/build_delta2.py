"""Build delta-cat2-20260930 report.json and source-identity.json from the delta-cat-20260930 run.
Usage: python build_delta2.py <skill_id>
Same schema as the prior certified report; only touched scores, notes and recommendations change.
Final = 0.4 x static + 0.6 x execution average (skill-auditor@1.0), same gates and floors."""
import copy
import json
import sys

SID = sys.argv[1]
PREV = f"F:/OpenScience/audits/{SID}/delta-cat-20260930"
RUN = f"F:/OpenScience/audits/{SID}/delta-cat2-20260930"
EXPECTED = {"bio-atac-seq-differential-accessibility": "dfc879ea543a99d857d53f2556d8b09660006d27a8dda23ede8b03b4ff5b9b1b",
            "bio-atac-seq-nucleosome-positioning": "2aa4d73b30023a6d14d690fa0e02f3a8b32a563d15bd445c24e257cb0e0ad18b"}[SID]
prev = json.load(open(f"{PREV}/report.json", encoding="utf-8"))
psrc = json.load(open(f"{PREV}/source-identity.json", encoding="utf-8"))
ident = json.load(open(f"{RUN}/logs/identity.json", encoding="utf-8"))
assert ident["candidate_identity"] == EXPECTED and len(ident["changed_vs_previous"]) == 1
rep = copy.deepcopy(prev)
cats = rep["static_score"]["categories"]
inputs = {i["index"]: i for i in rep["dynamic_score"]["inputs"]}


def rec(prefix):
    return next(r for r in rep["recommendations"] if r["title"].startswith(prefix))


if SID == "bio-atac-seq-differential-accessibility":
    cats["agent_usability"].update(score=16, note=(
        "Clear workflow and CLI header; SKILL.md step 5 and method-reference now agree that --sva fits "
        "DESeq2 directly on the DiffBind counts"))
    r = rec("method-reference contradicts")
    r["title"] = "--method silently ignored with --sva"
    r["problem"] = ("SKILL.md step 5 and method-reference now document that --sva ignores --method, but the run "
                    "prints nothing when --method is passed with --sva (--design does print a message).")
    r["root_cause"] = "fit_sva never reads method and main() emits no warning for the combination."
    r["fix"] = "Warn at runtime when --method is passed together with --sva."
else:
    cats["reliability"].update(score=11, note=(
        "Failure guards present and exercised; NRL plateau ambiguity remains; export/summary count "
        "difference now explained correctly in a script comment"))
    a = inputs[3]["assertions"][5]
    a["note"] = ("Runtime unchanged. NFR BAM 141,651 pairs vs nfr_count 130,774; mono 64,579 vs 67,604. The "
                 "script comment now states the cause (unshifted counts vs 9 bp-shorter Tn5-shifted exports), "
                 "which the delta-cat recount reproduces exactly; the assertion is behavioural and still fails")
    rep["recommendations"].remove(rec("R exports and summary CSV"))
    rep["key_strengths"].append(
        "The export-versus-summary count difference is now explained in the script, and the stated cause "
        "(9 bp Tn5 shift) reproduces both export counts exactly")

st = sum(c["score"] for c in cats.values())
rep["static_score"]["subtotal"] = st
ins = rep["dynamic_score"]["inputs"]
ex = round(sum(i["total"] for i in ins) / len(ins), 1)
passed = sum(i["assertions_passed"] for i in ins)
total = sum(i["assertions_total"] for i in ins)
rep["dynamic_score"].update(execution_avg=ex, assertion_pass_rate={"passed": passed, "total": total})
score = round(0.4 * st + 0.6 * ex)
grade, sym = (("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75
              else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌"))
l1 = sum(i["basic"] for i in ins) / len(ins)
l2 = sum(i["specialized"] for i in ins) / len(ins)
floors = {"static>=80": st >= 80, "exec>=85": ex >= 85, "L1>=32": l1 >= 32, "L2>=48": l2 >= 48,
          "assert>=90%": passed / total >= 0.9}
assert all(floors.values()), floors
assert all(r["priority"] in ("P0", "P1", "P2") for r in rep["recommendations"])
rep["final"].update(static_weighted=round(0.4 * st, 1), dynamic_weighted=round(0.6 * ex, 1), score=score,
                    grade=grade, grade_symbol=sym, deployable=True, veto_override=False)
assert set(rep) == set(prev) and set(rep["final"]) == set(prev["final"])
json.dump(rep, open(f"{RUN}/report.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
print(f"{SID}: static {st} exec {ex} assertions {passed}/{total} final {score} {grade}; floors ok; "
      f"recs {[(r['priority'], r['title']) for r in rep['recommendations']]}")

src = copy.deepcopy(psrc)
files = ident["candidate_files"]
c = src["candidate"]
if "content_sha256" in c:
    c["content_sha256"] = EXPECTED
    c["content_manifest"].update(file_count=len(files), bytes=sum(f["bytes"] for f in files))
    c["files"] = [{"path": f["path"], "bytes": f["bytes"], "sha256": f["sha256"]} for f in files]
    src["prior_audit"] = {"path": PREV.replace("/", "\\") + "\\report.json",
                          "content_sha256": psrc["candidate"]["content_sha256"], "score": prev["final"]["score"]}
else:
    import os
    import subprocess
    c["manifest_sha256"] = EXPECTED
    c.update(file_count=len(files), byte_total=sum(f["bytes"] for f in files))
    src["files"] = [{"path": f["path"],
                     "git_blob": subprocess.check_output(["git", "hash-object", os.path.join(c["path"], f["path"])],
                                                         text=True).strip(),
                     "sha256": f["sha256"], "bytes": f["bytes"]} for f in files]
    src["prior_audit"] = {"path": PREV, "identity": psrc["candidate"]["manifest_sha256"],
                          "score": prev["final"]["score"]}
src["phase"] = "delta re-audit (delta-cat2-20260930: follow-up documentation fix)"
src["delta"] = {"previous_run": PREV, "previous_identity": ident["previous_identity"],
                "shelf_commit": "ea3b976", "shelf_identity": ident["shelf_identity"],
                "changed_vs_previous": ident["changed_vs_previous"]}
json.dump(src, open(f"{RUN}/source-identity.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
print("source-identity written")
