import json, os, sys, shutil, difflib, yaml
sys.path.insert(0, r"F:\optimizing-agent-science-skills\tools")
from skill_preflight import identity
A = r"F:\OpenScience\audits\bio-machine-learning-atlas-mapping"
TREE = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping"
CERT = "becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3"
RUN = os.path.join(A, "reaudit-delta3-20261003"); scratch = os.path.join(RUN, "scratch", "s")
if os.path.exists(os.path.join(RUN, "scratch")): shutil.rmtree(os.path.join(RUN, "scratch"))
shutil.copytree(TREE, scratch)
cur, _ = identity(TREE); r = {"current": cur}
for e in json.load(open(os.path.join(A, "fix-description2-20261003", "edits.json"), encoding="utf-8")):
    p = os.path.join(scratch, e["file"]); t = open(p, "rb").read().decode("utf-8")
    assert t.count(e["new"]) == 1; open(p, "wb").write(t.replace(e["new"], e["old"]).encode("utf-8"))
id1, rows = identity(scratch)
r["after_revert"] = id1; r["reproduces_certified"] = id1 == CERT
cand = {}
for dp, dn, fn in os.walk(TREE):
    for f in fn:
        p = os.path.join(dp, f); cand[os.path.relpath(p, TREE).replace("\\", "/")] = open(p, "rb").read()
scr = dict(rows); assert set(cand) == set(scr)
r["files_differing"] = [k for k in cand if cand[k] != scr[k]]
d = [l for l in difflib.unified_diff(scr["SKILL.md"].decode().split("\n"), cand["SKILL.md"].decode().split("\n"), lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
r["skillmd_line_diff"] = [x[:70] for x in d]
r["one_description_line"] = len(d) == 2 and d[0].startswith("-description:") and d[1].startswith("+description:")
t = cand["SKILL.md"].decode(); fm = yaml.safe_load(t[4:t.find("\n---", 3)])
r.update(yaml_keys=list(fm), yaml_description=fm["description"], yaml_type=type(fm["description"]).__name__, yaml_name=fm["name"], new_len=len(fm["description"]))
r["description_sentences_use_when"] = fm["description"].startswith("Use when ") and fm["description"].count(". ") == 0 and fm["description"].endswith(".")
json.dump(r, open(os.path.join(RUN, "logs", "qualify.json"), "w"), indent=1)
shutil.rmtree(os.path.join(RUN, "scratch")); print(json.dumps(r, indent=1))
