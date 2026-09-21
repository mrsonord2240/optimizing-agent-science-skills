import re, pathlib
src = pathlib.Path(r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\run\skill\SKILL.md").read_text(encoding="utf-8")
out = pathlib.Path(r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\run\blocks")
n = 0
for m in re.finditer(r"```(\w+)\n(.*?)```", src, re.S):
    lang, body = m.group(1), m.group(2)
    n += 1
    ext = {"r": "R", "python": "py", "bash": "sh"}.get(lang, lang)
    p = out / f"skill_block{n:02d}.{ext}"
    p.write_text(body, encoding="utf-8", newline="\n")
    print(p.name, lang, len(body.splitlines()), "lines:", body.splitlines()[0][:70])
