import json, os, sys, shutil, hashlib, subprocess, yaml
sys.path.insert(0, r"F:\optimizing-agent-science-skills\tools")
from skill_preflight import identity
A = r"F:\OpenScience\audits"
REC = r"F:\optimizing-agent-science-skills\audits\skills"
CFG = {
 "bio-splicing-quantification": dict(tree=r"F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification",
   cert="247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc", chain=[]),
 "bio-machine-learning-survival-analysis": dict(tree=r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis",
   cert="eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb",
   chain=[("fix-textbatch-20261003","c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39")]),
 "bio-machine-learning-atlas-mapping": dict(tree=r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping",
   cert="8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04", chain=[]),
}
RUN = "reaudit-delta2-20261003"
out = {}
for sid, c in CFG.items():
    run = os.path.join(A, sid, RUN)
    scratch = os.path.join(run, "scratch", sid)
    if os.path.exists(os.path.join(run, "scratch")): shutil.rmtree(os.path.join(run, "scratch"))
    shutil.copytree(c["tree"], scratch)
    cur, _ = identity(c["tree"])
    r = {"current": cur}
    def revert(editsfile):
        ed = json.load(open(editsfile, encoding="utf-8"))
        for e in ed:
            p = os.path.join(scratch, e["file"])
            t = open(p, "rb").read().decode("utf-8")
            assert t.count(e["new"]) == 1, (editsfile, t.count(e["new"]))
            open(p, "wb").write(t.replace(e["new"], e["old"]).encode("utf-8"))
    revert(os.path.join(A, sid, "fix-description-20261003", "edits.json"))
    id1, rows = identity(scratch)
    r["after_desc_revert"] = id1
    r["reproduces_certified"] = id1 == c["cert"]
    # per-file diff vs candidate
    diffs = []
    cand = {}
    for dp, dn, fn in os.walk(c["tree"]):
        for f in fn:
            p = os.path.join(dp, f); cand[os.path.relpath(p, c["tree"]).replace("\\","/")] = open(p,"rb").read()
    scr = {rel: d for rel, d in rows}
    assert set(cand) == set(scr)
    diffs = [k for k in cand if cand[k] != scr[k]]
    r["files_differing"] = diffs
    # line diff of SKILL.md
    a = cand["SKILL.md"].decode("utf-8").split("\n"); b = scr["SKILL.md"].decode("utf-8").split("\n")
    import difflib
    d = [l for l in difflib.unified_diff(b, a, lineterm="", n=0) if not l.startswith(("---","+++","@@"))]
    r["skillmd_line_diff"] = [x[:60] for x in d]
    r["skillmd_diff_is_one_description_line"] = len(d) == 2 and d[0].startswith("-description:") and d[1].startswith("+description:")
    for fix, want in c["chain"]:
        revert(os.path.join(A, sid, fix, "edits.json"))
        idc, _ = identity(scratch)
        r["chain_" + fix] = idc; r["chain_reproduces"] = idc == want
    # YAML parse of current frontmatter
    t = cand["SKILL.md"].decode("utf-8")
    end = t.find("\n---", 3)
    fm = yaml.safe_load(t[4:end])
    r["yaml_keys"] = list(fm)
    r["yaml_description"] = fm["description"]; r["yaml_description_type"] = type(fm["description"]).__name__
    r["yaml_name"] = fm["name"]
    fm0 = yaml.safe_load(open(os.path.join(scratch,"SKILL.md"),encoding="utf-8").read().split("\n---",1)[0][4:]) if not c["chain"] else None
    r["old_description_len"] = len(fm0["description"]) if fm0 else None
    r["new_description_len"] = len(fm["description"])
    # other frontmatter fields unchanged vs scratch (desc-reverted only for splicing/atlas)
    out[sid] = r
    json.dump(r, open(os.path.join(run, "logs", "qualify.json"), "w"), indent=1)
    shutil.rmtree(os.path.join(run, "scratch"))
print(json.dumps(out, indent=1))
