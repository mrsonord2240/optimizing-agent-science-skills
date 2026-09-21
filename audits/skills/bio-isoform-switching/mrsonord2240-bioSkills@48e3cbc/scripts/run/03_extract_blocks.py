# Extract the fenced code blocks of the Skill's SKILL.md into run/blocks/ so every test executes the Skill's text verbatim.
import re, os, io
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill", "SKILL.md")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocks")
os.makedirs(out, exist_ok=True)
txt = io.open(src, encoding="utf-8").read()
blocks = re.findall(r"```(\w+)\n(.*?)```", txt, flags=re.S)
names = {}
n = {"r": 0, "bash": 0}
for lang, body in blocks:
    i = n.get(lang, 0); n[lang] = i + 1
    fn = "%s_%02d.%s" % (lang, i, "R" if lang == "r" else "sh")
    with io.open(os.path.join(out, fn), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print(fn, len(body.splitlines()), "lines |", body.strip().splitlines()[0][:80])
