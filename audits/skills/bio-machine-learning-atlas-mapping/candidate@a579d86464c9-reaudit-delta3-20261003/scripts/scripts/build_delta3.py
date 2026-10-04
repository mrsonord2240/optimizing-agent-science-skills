import json, os, sys, hashlib
sys.path.insert(0, r"F:\optimizing-agent-science-skills\tools")
from skill_preflight import identity
A = r"F:\OpenScience\audits\bio-machine-learning-atlas-mapping"; RUN = os.path.join(A, "reaudit-delta3-20261003")
CERT = r"F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-atlas-mapping\candidate@becbe61423e7-reaudit-delta2-20261003"
TREE = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping"
ident, rows = identity(TREE); q = json.load(open(os.path.join(RUN, "logs", "qualify.json")))
assert q["current"] == ident and q["reproduces_certified"] and q["one_description_line"]
files = [{"path": p, "bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()} for p, d in rows]
sj = json.load(open(os.path.join(CERT, "source-identity.json"), encoding="utf-8")); rep = json.load(open(os.path.join(CERT, "report.json"), encoding="utf-8"))
prior = {"identity": sj["candidate"]["content_sha256"], "run": os.path.basename(CERT), "path": CERT, "score": rep["final"]["score"], "grade": rep["final"]["grade"], "static": rep["static_score"]["subtotal"]}
sj["candidate"]["content_sha256"] = ident
sj["candidate"]["content_manifest"].update(file_count=len(files), bytes=sum(f["bytes"] for f in files))
sj["files"] = files; sj["prior_audit"] = prior
sj["delta"] = {"mode": "text-only delta re-audit (description reword, AM-009 fix)",
  "qualification": f"Only SKILL.md differs from certified identity {prior['identity'][:12]}; the other 6 files are byte-identical. SKILL.md differs by exactly one line, the frontmatter description (old 174 to new {q['new_len']} chars). Reverting fix-description2-20261003/edits.json on a scratch copy reproduces {q['after_revert']} exactly. Frontmatter parsed with PyYAML safe_load: one string, name and all other keys intact. Body byte-identical, so the certified execution evidence applies; one extra independent check (scripts/frozen_ref_check.py) was run on the accuracy of 'without retraining the reference'.",
  "fix_log": os.path.join(A, "fix-description2-20261003", "fix-log.md")}
sj["tooling"]["frozen_ref_check"] = "scripts/frozen_ref_check.py, logs/frozen_ref.log (scvi-tools 1.5.1, single-cell venv, no Skill bytes touched)"
rep["meta"]["performed_by"] = "Claude (Anthropic) delta re-audit worker E4"
rep["meta"]["description"] = q["yaml_description"]; rep["meta"]["evaluated_on"] = "2026-10-03"
ag = rep["static_score"]["categories"]["agent_specific"]; ag["score"] = 17
ag["note"] = ("Trigger now states the separating task (projecting a query into an existing reference atlas embedding without retraining the reference), which bio-single-cell-cell-annotation (shelf: CellTypist/SingleR/Azimuth/scmap annotation) does not claim; rubric 8.1 = 3, mostly precise: the third clause (judging transferred labels) still overlaps cell-annotation's confidence/rejection trigger and the body has no Related Skills hand-off to cell-annotation; progressive disclosure works; bundled curated markers cover PBMC and a 1604-gene set only")
rep["recommendations"] = [r for r in rep["recommendations"] if not r["title"].startswith("AM-009")]
ins = rep["dynamic_score"]["inputs"]; avg = round(sum(i["basic"] + i["specialized"] for i in ins) / len(ins), 1)
assert avg == rep["dynamic_score"]["execution_avg"]
sub = sum(c["score"] for c in rep["static_score"]["categories"].values()); rep["static_score"]["subtotal"] = sub
sw = round(sub * .4, 1); dw = round(avg * .6, 1); score = round(sub * .4 + avg * .6)
rep["final"].update(static_weighted=sw, dynamic_weighted=dw, score=score)
ap = rep["dynamic_score"]["assertion_pass_rate"]; l1 = sum(i["basic"] for i in ins) / len(ins); l2 = sum(i["specialized"] for i in ins) / len(ins)
assert sub >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and score >= 85 and ap["passed"] / ap["total"] >= .9
json.dump(sj, open(os.path.join(RUN, "source-identity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
json.dump(rep, open(os.path.join(RUN, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
res = dict(ident=ident, prior=prior, sub=sub, avg=avg, sw=sw, dw=dw, exact=round(sub*.4+avg*.6, 2), score=score, ap=ap, l1=round(l1, 1), l2=round(l2, 1), nfiles=len(files), nbytes=sum(f["bytes"] for f in files), recs=[(r["priority"], r["title"]) for r in rep["recommendations"]], q=q)
json.dump(res, open(os.path.join(RUN, "logs", "results.json"), "w"), indent=1); print(json.dumps({k: v for k, v in res.items() if k != "q"}, indent=1))
