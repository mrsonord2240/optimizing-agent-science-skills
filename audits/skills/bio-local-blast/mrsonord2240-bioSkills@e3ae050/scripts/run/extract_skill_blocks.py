"""Extract fenced code blocks from the fixed SKILL.md programmatically, so we test
the shipped document rather than a hand transcription of it."""
import re, sys, json

SKILL_MD = r"F:\OpenScience\wt\db-blast\database-access\local-blast\SKILL.md"

with open(SKILL_MD, encoding='utf-8') as f:
    text = f.read()

# Match fenced code blocks: ```lang\n...\n```
pattern = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
blocks = []
for i, m in enumerate(pattern.finditer(text)):
    lang = m.group(1) or "(none)"
    code = m.group(2)
    # capture preceding heading for context
    preceding = text[:m.start()]
    headings = re.findall(r"^#{1,4}\s+(.*)$", preceding, re.MULTILINE)
    heading = headings[-1] if headings else "(no heading)"
    blocks.append({"index": i, "lang": lang, "heading": heading, "code": code})

for b in blocks:
    print(f"--- Block {b['index']} | lang={b['lang']} | heading={b['heading']!r} ---")
    print(b['code'])
    print()

with open(r"F:\OpenScience\audits\bio-local-blast\run\skill_blocks.json", "w", encoding='utf-8') as f:
    json.dump(blocks, f, indent=2)
print(f"\nTotal blocks: {len(blocks)}", file=sys.stderr)
