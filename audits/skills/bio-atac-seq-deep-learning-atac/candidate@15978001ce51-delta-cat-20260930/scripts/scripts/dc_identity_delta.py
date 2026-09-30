"""Delta re-audit: identity, delta vs shelf copy, line endings, frontmatter and marketplace category.

usage: python dc_identity_delta.py <skill_id> <candidate_dir> <expected_identity>
Read-only on the candidate, the shelf and the manifest tool.
"""
import difflib, hashlib, json, os, sys

sys.dont_write_bytecode = True
SHELF = "F:/optimized-scientific-skills"
TOOLS = "F:/optimizing-agent-science-skills/tools"


def manifest(root):
    rows = []
    for dp, dns, fs in os.walk(root):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fs:
            p = os.path.join(dp, f)
            b = open(p, "rb").read()
            rows.append((os.path.relpath(p, root).replace(os.sep, "/"), len(b), hashlib.sha256(b).hexdigest(), b))
    rows.sort(key=lambda r: r[0].encode("utf-8"))
    text = "\n".join(f"{r}\t{n}\t{h}" for r, n, h, _ in rows)
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), rows


sid, cand, expected = sys.argv[1:4]
old_dir = os.path.join(SHELF, "skills", sid)
new_id, new = manifest(cand)
old_id, old = manifest(old_dir)
print(f"candidate identity {new_id} files={len(new)} bytes={sum(r[1] for r in new)}")
print(f"expected           {expected} -> {'MATCH' if new_id == expected else 'MISMATCH'}")
print(f"shelf identity     {old_id} files={len(old)} bytes={sum(r[1] for r in old)}")

o = {r[0]: r for r in old}; n = {r[0]: r for r in new}
print("added:", sorted(set(n) - set(o)) or "none", "| removed:", sorted(set(o) - set(n)) or "none")
for path in sorted(set(o) & set(n), key=lambda s: s.encode()):
    if o[path][2] == n[path][2]:
        continue
    a = o[path][3].decode("utf-8").splitlines(); b = n[path][3].decode("utf-8").splitlines()
    print(f"== changed {path} ({o[path][1]} -> {n[path][1]} bytes)")
    for line in difflib.unified_diff(a, b, lineterm="", n=0):
        if not line.startswith(("---", "+++")):
            print("  " + line)
for path, (_, _, _, b) in sorted(n.items()):
    if b.count(b"\r\n"):
        print(f"CRLF in {path}: {b.count(b'\r\n')}")
print("CRLF scan done (no line above = all LF)")

# frontmatter parse (PyYAML if present, else line split) and keys
text = n["SKILL.md"][3].decode("utf-8")
end = text.find("\n---", 3); fm = text[3:end]
try:
    import yaml
    meta = yaml.safe_load(fm); print("frontmatter parses as YAML; keys:", list(meta))
except ImportError:
    meta = dict(l.split(":", 1) for l in fm.strip().splitlines()); print("keys (no PyYAML):", list(meta))
print("category:", repr(str(meta.get("category")).strip()), "| author:", repr(str(meta.get("author")).strip()))

# the manifest tool's own reader, pointed at the candidate's worktree as the shelf
sys.path.insert(0, TOOLS)
import marketplace_manifests as mm
wt = os.path.dirname(os.path.dirname(os.path.normpath(cand)))
print("VALID_CATEGORIES:", sorted(mm.VALID_CATEGORIES))
print("skill_category(candidate) ->", repr(mm.skill_category(sid, shelf=wt)), "(accepted)")
sys.exit(0 if new_id == expected else 1)
