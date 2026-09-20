"""Extract every fenced code block from SKILL.md / usage-guide.md verbatim into run/snip/<file>_<n>_<lang>.txt and print an index."""
import os, re, sys
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(RUN, "snip"); os.makedirs(out, exist_ok=True)
for fn in ("SKILL.md", "usage-guide.md"):
    txt = open(os.path.join(RUN, "skill", fn), encoding="utf-8").read()
    head = ""; n = 0
    lines = txt.split("\n"); i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("#"): head = l.strip("# ").strip()
        m = re.match(r"^```(\w*)", l)
        if m:
            lang = m.group(1) or "txt"; body = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            n += 1
            name = f"{fn.split('.')[0]}_{n:02d}_{lang}.txt"
            open(os.path.join(out, name), "w", encoding="utf-8", newline="\n").write("\n".join(body) + "\n")
            print(f"{name:28s} [{head[:50]}] {body[0][:70] if body else ''}")
        i += 1
