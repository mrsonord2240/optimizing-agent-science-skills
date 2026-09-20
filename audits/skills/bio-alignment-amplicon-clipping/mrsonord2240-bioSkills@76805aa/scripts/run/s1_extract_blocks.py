"""Extract fenced ```bash blocks from the fixed SKILL.md (verbatim, no edits) so the audit runs the Skill's own commands.
Writes <outdir>/<nearest-heading-slug>_<k>.sh. Usage: s1_extract_blocks.py SKILL.md outdir"""
import re, os, sys
skill = sys.argv[1]; outdir = sys.argv[2]
os.makedirs(outdir, exist_ok=True)
txt = open(skill, encoding="utf-8").read()
head = ""; found = {}
pat = re.compile(r"^(#+ [^\n]*)$|^```bash\n((?:.|\n)*?)^```", re.M)
for m in pat.finditer(txt):
    if m.group(1):
        head = m.group(1)
    else:
        key = re.sub(r"[^a-z0-9]+", "_", head.lower()).strip("_")
        found[key] = found.get(key, 0) + 1
        name = f"{key}_{found[key]}.sh"
        with open(os.path.join(outdir, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(m.group(2))
        print(name, len(m.group(2).splitlines()), "lines")
