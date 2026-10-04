import json, os, shutil, sys
sys.path.insert(0, r"F:\optimizing-agent-science-skills\tools")
from skill_preflight import identity
A = r"F:\OpenScience\audits"; REC = r"F:\optimizing-agent-science-skills\audits\skills"
RUN = "reaudit-delta2-20261003"
WHO = "Claude (Anthropic) delta re-audit worker E2"
CERTREC = {
 "bio-splicing-quantification": "candidate@247bcf26db18-run-reaudit-2",
 "bio-machine-learning-survival-analysis": "candidate@eac9a589b7bd-reaudit-delta-20261003",
 "bio-machine-learning-atlas-mapping": "candidate@8b4d96ad2465-final-reaudit-lane3b-20261003",
}
TREE = {
 "bio-splicing-quantification": r"F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification",
 "bio-machine-learning-survival-analysis": r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis",
 "bio-machine-learning-atlas-mapping": r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping",
}
import yaml
res = {}
for sid, rec in CERTREC.items():
    run = os.path.join(A, sid, RUN)
    cert = os.path.join(REC, sid, rec)
    ident, rows = identity(TREE[sid])
    q = json.load(open(os.path.join(run, "logs", "qualify.json")))
    assert q["current"] == ident and q["reproduces_certified"] and q["skillmd_diff_is_one_description_line"]
    files = [{"path": r, "bytes": len(d), "sha256": __import__("hashlib").sha256(d).hexdigest()} for r, d in rows]
    nbytes = sum(f["bytes"] for f in files)
    sidj = json.load(open(os.path.join(cert, "source-identity.json"), encoding="utf-8"))
    prior = json.load(open(os.path.join(cert, "report.json"), encoding="utf-8"))
    rep = json.load(open(os.path.join(cert, "report.json"), encoding="utf-8"))
    certid = sidj["candidate"]["content_sha256"]
    sidj["candidate"]["content_sha256"] = ident
    cm = sidj["candidate"].get("content_manifest", {})
    sidj["candidate"]["content_manifest"] = {"file_count": len(files), "bytes": nbytes, "recipe": cm.get("recipe", "relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; records sorted by path and separated by LF; no trailing LF")}
    sidj["candidate"]["status_after_execution"] = "candidate files unchanged (identity re-verified with skill_preflight --offline before and after)"
    sidj["files"] = files
    sidj["prior_audit"] = {"identity": certid, "run": rec, "path": cert, "score": prior["final"]["score"], "grade": prior["final"]["grade"]}
    chain = q.get("chain_reproduces")
    qual = (f"Only SKILL.md differs from the certified identity {certid[:12]}; the other files are byte-identical. SKILL.md differs by exactly one line, the frontmatter description (old 694/577/n.a. chars to new {q['new_description_len']} chars). "
            f"Reverting edits.json (fix-description-20261003) on a scratch copy reproduces {q['after_desc_revert']} exactly.")
    if chain:
        qual += (" Reverting the SA-006 edit (fix-textbatch-20261003) after that reproduces "
                 f"{q['chain_fix-textbatch-20261003']}: the chain back to c60f873f52f6 is fully reproduced.")
    qual += " Frontmatter parsed with PyYAML safe_load: single string, name and all other keys intact."
    sidj["delta"] = {"mode": "text-only delta re-audit (description trim)", "qualification": qual,
                     "fix_log": os.path.join(A, sid, "fix-description-20261003", "fix-log.md")}
    rep["meta"]["performed_by"] = WHO
    rep["meta"]["description"] = q["yaml_description"]
    rep["meta"]["evaluated_on"] = "2026-10-03"
    ag = rep["static_score"]["categories"]["agent_specific"]
    if sid == "bio-splicing-quantification":
        ag["note"] = ("Trigger is now the Use-when clause only (tool list, taxonomy prose removed at Sam's request); 'short-read' and 'measuring PSI' still separate it from bio-long-read-splicing and bio-differential-splicing, and Related Skills in the body carry the routing; progressive disclosure works; restricted and heavy surfaces are labelled not executed")
    elif sid == "bio-machine-learning-survival-analysis":
        ag["note"] = ("Trigger is now the Use-when clause only; 'individualized risk predictor ... beyond the C-index' keeps the prediction regime distinct from inference, and the body retains the hand-off to clinical-biostatistics/survival-analysis; progressive disclosure, seeded scripts, and prose-only or R-only methods labelled not executed")
    else:
        ag["score"] = 16
        ag["note"] = ("Trigger is now the Use-when clause only; the description no longer separates this Skill from bio-single-cell-cell-annotation (shelf), whose trigger also covers annotating from a reference atlas and transferring labels, and the body names no hand-off to it (AM-009); progressive disclosure works; bundled curated markers cover PBMC and a 1604-gene set only")
        rep["recommendations"].append({
            "priority": "P2",
            "title": "AM-009 Description no longer separates it from cell-annotation",
            "observed_in": [],
            "problem": "The trimmed description (annotate against a pre-trained reference atlas, pick a mapping method, judge transferred labels) matches bio-single-cell-cell-annotation, which on the shelf says annotate from a reference atlas or pretrained model, transfer labels onto a query, assess confidence and rejection. The old tool list and the cell-annotation pointer were the separators, and the body has no hand-off to cell-annotation either.",
            "root_cause": "Description reduced to a generic clause that omits the Skill-specific mechanism (projection into a fixed reference latent space with out-of-distribution gating).",
            "fix": "Add one clause to the description, e.g. 'projecting a query into a fixed reference latent space (scArches, Symphony) and gating labels on out-of-distribution distance', and add a Related Skills hand-off to cell-annotation for classifier-only annotation. Text only."})
        rep["recommendations"].sort(key=lambda r: r["priority"])
    # scores recomputed per schema
    ins = rep["dynamic_score"]["inputs"]
    avg = round(sum(i["basic"] + i["specialized"] for i in ins) / len(ins), 1)
    assert avg == rep["dynamic_score"]["execution_avg"], (avg, rep["dynamic_score"]["execution_avg"])
    sub = sum(c["score"] for c in rep["static_score"]["categories"].values())
    rep["static_score"]["subtotal"] = sub
    sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = round(sw + dw)
    rep["final"].update({"static_weighted": sw, "dynamic_weighted": dw, "score": score})
    ap = rep["dynamic_score"]["assertion_pass_rate"]
    l1 = sum(i["basic"] for i in ins) / len(ins); l2 = sum(i["specialized"] for i in ins) / len(ins)
    assert sub >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and score >= 85 and ap["passed"] / ap["total"] >= .9
    json.dump(sidj, open(os.path.join(run, "source-identity.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(rep, open(os.path.join(run, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    res[sid] = dict(ident=ident, certid=certid, sub=sub, avg=avg, sw=sw, dw=dw, score=score, ap=ap, l1=round(l1, 1), l2=round(l2, 1),
                    prior_sub=prior["static_score"]["subtotal"], prior_score=prior["final"]["score"], q=q, nbytes=nbytes, nfiles=len(files),
                    recs=[(r["priority"], r["title"]) for r in rep["recommendations"]])
json.dump(res, open(os.path.join(A, "delta2_results.json"), "w"), indent=1)
print(json.dumps({k: {x: v for x, v in d.items() if x != "q"} for k, d in res.items()}, indent=1))
