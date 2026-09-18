"""Programmatically extract fenced code blocks from the shipped SKILL.md,
so the audit runs the document itself, not a hand transcription of it."""
import re
import sys

skill_md = open(r"F:\OpenScience\audits\bio-biomart-queries\run\skill_copy\SKILL.md",
                 encoding="utf-8").read()

# Match ```lang\n...\n``` blocks, capturing the preceding heading as a label.
pattern = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
blocks = pattern.findall(skill_md)

for i, (lang, code) in enumerate(blocks):
    print(f"--- Block {i} (lang={lang!r}) ---")
    print(code[:200].rstrip())
    print("...")
