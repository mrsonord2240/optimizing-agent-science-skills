#!/usr/bin/env python
"""Pull fenced code blocks out of the shipped SKILL.md copy so audits run the text VERBATIM.
usage: extract_block.py <heading substring> <lang> <out file>   (first fenced block of that lang under the heading)"""
import re, sys
md = open('/mnt/openscience/audits/bio-alignment-sorting/run/skill/SKILL.md', encoding='utf-8').read()
head, lang, out = sys.argv[1:4]
i = md.index(head)
m = re.search(r"```%s\n(.*?)```" % lang, md[i:], re.S)
open(out, 'w', encoding='utf-8').write(m.group(1))
print(f"extracted {len(m.group(1).splitlines())} lines from '{head}' -> {out}")
