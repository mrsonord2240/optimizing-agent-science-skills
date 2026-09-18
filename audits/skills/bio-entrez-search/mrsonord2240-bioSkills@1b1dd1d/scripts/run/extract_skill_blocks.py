# Extract fenced python code blocks straight from the shipped SKILL.md, in order.
# Source: fix worktree db-esearch2 (fix commit 1b1dd1d), NOT the external clone.
import re, pathlib

skill_md = pathlib.Path(r"F:/OpenScience/wt/db-esearch2/database-access/entrez-search/SKILL.md").read_text(encoding='utf-8')
blocks = re.findall(r"```python\n(.*?)```", skill_md, re.DOTALL)
print(f"Found {len(blocks)} python code blocks in SKILL.md")
outdir = pathlib.Path(".")
for i, b in enumerate(blocks, 1):
    fn = outdir / f"skill_block_{i:02d}.py"
    fn.write_text(b, encoding='utf-8')
    first_line = b.strip().splitlines()[0] if b.strip() else ""
    print(f"  block {i:02d}: {first_line[:80]}")
