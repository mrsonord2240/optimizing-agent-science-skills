#!/usr/bin/env python3
"""Extract every fenced code block of the Skill's SKILL.md verbatim, named <section-slug>_<n>.<sh|R>, into out/blocks/ (so the audit runs the Skill's own text)."""
import re, os, sys
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_copy", "SKILL.md")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "blocks"); os.makedirs(out, exist_ok=True)
sec, n, inb, lang, buf = "top", {}, False, "", []
for ln in open(src, encoding="utf-8"):
    m = re.match(r"^(#{1,3}) (.*)", ln)
    if m and not inb:
        sec = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")[:40]; continue
    if ln.startswith("```"):
        if not inb:
            inb, lang, buf = True, ln[3:].strip(), []
        else:
            inb = False
            n[sec] = n.get(sec, 0) + 1
            ext = {"bash": "sh", "r": "R"}.get(lang, "txt")
            p = os.path.join(out, "%s_%d.%s" % (sec, n[sec], ext))
            open(p, "w", encoding="utf-8", newline="\n").write("".join(buf))
            print(p, lang, len(buf), "lines")
        continue
    if inb:
        buf.append(ln)
