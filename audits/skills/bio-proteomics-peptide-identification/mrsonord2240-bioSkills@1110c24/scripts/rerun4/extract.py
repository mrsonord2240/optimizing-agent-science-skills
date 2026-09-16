"""Extract fenced code blocks from a SKILL.md by the heading they sit under.

Used so every 'the Skill's own code' claim in this audit runs text taken
verbatim out of the fork's SKILL.md, not a re-typed copy.
"""
import re
import sys


def blocks(path, lang=None):
    text = open(path, encoding="utf-8").read()
    out = []
    heading = None
    for chunk in re.split(r"\n(?=#{2,4} )", text):
        m = re.match(r"(#{2,4} )(.*)", chunk)
        h = m.group(2).strip() if m else heading
        for fm in re.finditer(r"```(\w*)\n(.*?)```", chunk, re.S):
            if lang is None or fm.group(1) == lang:
                out.append((h, fm.group(1), fm.group(2)))
    return out


if __name__ == "__main__":
    for h, l, b in blocks(sys.argv[1]):
        print(f"--- [{l}] {h}  ({len(b.splitlines())} lines)")
