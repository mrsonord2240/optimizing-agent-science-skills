"""Extract every fenced code block of the Skill's SKILL.md (copy in run/skill) verbatim into run/blocks/.
Names: NN_<lang>.<ext> in document order, with the preceding heading in the index file."""
import os, re, io
here = os.path.dirname(os.path.abspath(__file__))
run = os.path.dirname(here)
src = os.path.join(run, "skill", "SKILL.md")
out = os.path.join(run, "blocks")
os.makedirs(out, exist_ok=True)
text = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
heading = ""
idx = []
n = 0
lines = text.split("\n")
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("#"):
        heading = ln.strip("# ").strip()
    m = re.match(r"^```(\w*)\s*$", ln)
    if m:
        lang = m.group(1) or "txt"
        body = []
        i += 1
        while not lines[i].startswith("```"):
            body.append(lines[i]); i += 1
        n += 1
        ext = {"r": "R", "bash": "sh"}.get(lang, lang)
        name = "%02d_%s.%s" % (n, lang, ext)
        with io.open(os.path.join(out, name), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(body) + "\n")
        idx.append("%s\t%s\t%d lines" % (name, heading, len(body)))
    i += 1
with io.open(os.path.join(out, "INDEX.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(idx) + "\n")
print("\n".join(idx))
