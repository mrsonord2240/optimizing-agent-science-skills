"""Delta qualification for the description-trim: revert edits.json on a scratch copy, check certified identity,
check that only the `description:` line differs, and parse the new frontmatter as YAML.
Usage: desc_qualify.py <skill-id> <certified-identity>"""
import difflib, hashlib, json, shutil, subprocess, sys
from pathlib import Path

sid, cert = sys.argv[1:3]
W = Path(r"F:\OpenScience\wt\normalize-dv-lane1\skills") / sid
RUN = Path(rf"F:\OpenScience\audits\{sid}\delta-desc-20261003")
REPO = Path(r"F:\optimizing-agent-science-skills")
edits = json.loads((RUN.parent / "fix-description-20261003" / "edits.json").read_text(encoding="utf-8"))
dst = RUN / "scratch" / sid
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(W, dst)
for e in edits:
    q = dst / e["file"]
    s = q.read_bytes().decode("utf-8")
    assert s.count(e["new"]) == 1, "new string not found exactly once"
    q.write_bytes(s.replace(e["new"], e["old"]).encode("utf-8"))
r = subprocess.run([sys.executable, "tools/skill_preflight.py", "--offline", "--json", str(dst)], cwd=REPO, capture_output=True, text=True)
pre = json.loads(r.stdout)[0]
print("reverted identity:", pre["identity"], "files", pre["files"], "bytes", pre["bytes"])
print("CERT MATCH" if pre["identity"] == cert else "CERT MISMATCH")
# file-level diff candidate vs reverted
changed = []
for p in sorted(W.rglob("*")):
    if p.is_file():
        rel = p.relative_to(W).as_posix()
        a = (dst / rel).read_bytes(); b = p.read_bytes()
        if a != b:
            changed.append(rel)
            ds = [l for l in difflib.unified_diff(a.decode().splitlines(), b.decode().splitlines(), "certified", "candidate", lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            print("CHANGED", rel, len(ds), "diff lines")
            for l in ds:
                print("   ", l[:120], "...")
            (RUN / "scripts" / "diff_SKILL.md.txt").write_text("\n".join(ds) + "\n", encoding="utf-8")
extra = {p.relative_to(dst).as_posix() for p in dst.rglob("*") if p.is_file()} ^ {p.relative_to(W).as_posix() for p in W.rglob("*") if p.is_file()}
print("file-set differences:", extra or "none")
# only the description: line differs
a = (dst / "SKILL.md").read_text(encoding="utf-8").splitlines(); b = (W / "SKILL.md").read_text(encoding="utf-8").splitlines()
d = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
print("same line count:", len(a) == len(b), "differing line numbers:", [i + 1 for i in d], [b[i][:12] for i in d])
# YAML parse
import yaml
txt = (W / "SKILL.md").read_text(encoding="utf-8")
fm = txt.split("---", 2)[1]
y = yaml.safe_load(fm)
print("yaml keys:", list(y), "| description type:", type(y["description"]).__name__)
print("description:", y["description"])
print("starts with 'Use when':", y["description"].startswith("Use when"), "| len", len(y["description"]), "| name==dir:", y["name"] == sid)
# compare with the certified record's recorded SKILL.md hash
