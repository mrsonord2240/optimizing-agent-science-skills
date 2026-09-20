"""Print the Nth fenced code block that follows a heading line in a markdown file, verbatim.
usage: blocks.py FILE "HEADING TEXT (exact line)" [N=1]
Used so the audit runs the Skill's own text, not a retyped copy."""
import sys, io
path, heading = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
lines = io.open(path, encoding="utf-8").read().split("\n")
try:
    start = next(i for i, l in enumerate(lines) if l.strip() == heading.strip())
except StopIteration:
    sys.stderr.write("heading not found: %s\n" % heading); sys.exit(4)
count, inblk, out = 0, False, []
for l in lines[start + 1:]:
    if l.startswith("```"):
        if inblk:
            count += 1
            if count == n:
                break
            out = []
            inblk = False
        else:
            inblk = True
        continue
    if inblk:
        out.append(l)
    elif l.startswith("## ") or (l.startswith("### ") and False):
        break
sys.stdout.write("\n".join(out) + "\n")
