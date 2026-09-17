"""
Extract every fenced ```python code block from the SHIPPED SKILL.md, verbatim, in document
order. This is the "strong move" the brief calls out: test the document itself, not a
hand-transcribed approximation of it.

Source: F:\\OpenScience\\wt\\db-efetch\\database-access\\entrez-fetch\\SKILL.md
(fix worktree, branch fix/db-efetch, commit 3a095e5) -- read-only, never written to.
"""
import re
import pathlib

SKILL_MD = pathlib.Path(r"F:\OpenScience\wt\db-efetch\database-access\entrez-fetch\SKILL.md")
OUT_DIR = pathlib.Path(r"F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks")
OUT_DIR.mkdir(exist_ok=True)

text = SKILL_MD.read_text(encoding="utf-8")

# Match ```python ... ``` fenced blocks
pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
blocks = pattern.findall(text)

print(f"Found {len(blocks)} python fenced code blocks in shipped SKILL.md")

for i, block in enumerate(blocks, start=1):
    out_path = OUT_DIR / f"block_{i:02d}.py"
    out_path.write_text(block, encoding="utf-8")
    first_line = block.strip().splitlines()[0] if block.strip() else "(empty)"
    print(f"  block_{i:02d}.py  ({len(block.splitlines())} lines)  starts: {first_line}")

# Also concatenate all blocks into one importable module, in document order, since later
# blocks assume `Entrez`/`SeqIO` are already imported by the "Required Setup" block.
combined = "\n\n".join(blocks)
(OUT_DIR / "_combined.py").write_text(combined, encoding="utf-8")
print(f"\nWrote combined module: {OUT_DIR / '_combined.py'} ({len(combined.splitlines())} lines)")
