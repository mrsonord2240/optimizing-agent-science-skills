#!/usr/bin/env python3
"""Loadability of the fixed SKILL.md: YAML frontmatter parses, size/line/token estimate, every code fence balanced, every tool/file the text points at exists in the repo."""
import re, sys, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_copy", "SKILL.md")
t = open(p, encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
try:
    import yaml
    fm = yaml.safe_load(m.group(1)); print("YAML frontmatter parses; keys:", list(fm), " description chars:", len(fm["description"]))
except ImportError:
    print("pyyaml not available; frontmatter text length", len(m.group(1)))
print("bytes %d, lines %d, approx tokens (chars/4) %d" % (len(t.encode()), t.count("\n"), len(t) // 4))
print("code fences:", t.count("```"), "(even = balanced)" if t.count("```") % 2 == 0 else "UNBALANCED")
print("H2 sections:", len(re.findall(r"^## ", t, re.M)), " H3:", len(re.findall(r"^### ", t, re.M)))
root = next(r for r in ("/mnt/openscience/wt/as-longread", "/f/OpenScience/wt/as-longread", "F:/OpenScience/wt/as-longread") if os.path.exists(r))
for rel in re.findall(r"^- ((?:[a-z-]+/)?[a-z-]+) - ", t.split("## Related Skills")[1], re.M):
    cands = [os.path.join(root, rel), os.path.join(root, "alternative-splicing", rel)]
    print("related skill %-40s %s" % (rel, "exists" if any(os.path.isdir(c) for c in cands) else "MISSING"))
print("examples dir referenced in SKILL.md/usage-guide:", "examples/" in t, "| usage-guide.md exists:", os.path.exists(os.path.join(os.path.dirname(p), "usage-guide.md")))
