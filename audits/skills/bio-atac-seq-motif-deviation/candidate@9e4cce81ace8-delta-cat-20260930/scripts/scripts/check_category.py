"""Validate the new frontmatter category/author with the marketplace tool's own parser (read-only).
Usage: python check_category.py <skill_id> <worktree_root containing skills/<id>>"""
import sys

sys.path.insert(0, "F:/optimizing-agent-science-skills/tools")
import marketplace_manifests as mm  # noqa: E402

sid, wt = sys.argv[1:3]
cat = mm.skill_category(sid, shelf=wt)
print(f"{sid}: category={cat!r} valid={cat in mm.VALID_CATEGORIES} allowed={sorted(mm.VALID_CATEGORIES)}")
text = open(f"{wt}/skills/{sid}/SKILL.md", encoding="utf-8").read()
fm = text[3:text.find("\n---", 3)]
try:
    import yaml
    d = yaml.safe_load(fm)
    print(f"yaml ok: name={d.get('name')!r} author={d.get('author')!r} category={d.get('category')!r} keys={list(d)}")
except ImportError:
    print("pyyaml unavailable; line check:", [l for l in fm.splitlines() if l.startswith(("author:", "category:"))])
