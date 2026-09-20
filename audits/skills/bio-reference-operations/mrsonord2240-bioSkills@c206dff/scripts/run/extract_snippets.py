#!/usr/bin/env python
"""Extract every fenced code block from the Skill's SKILL.md and usage-guide.md verbatim (no retyping)
into snippets/<doc>_<NN>_<lang>.txt and print an index. Used so that what gets executed is exactly what ships."""
import os, re, sys
ROOT = sys.argv[1]      # skill dir copy
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
idx = []
for doc, tag in (('SKILL.md', 'skill'), ('usage-guide.md', 'ug')):
    txt = open(os.path.join(ROOT, doc), encoding='utf-8').read()
    for n, m in enumerate(re.finditer(r'```(\w*)\n(.*?)```', txt, re.S), 1):
        lang, body = m.group(1) or 'txt', m.group(2)
        fn = f'{tag}_{n:02d}_{lang}.txt'
        open(os.path.join(OUT, fn), 'w', encoding='utf-8', newline='\n').write(body)
        idx.append((fn, lang, body.strip().splitlines()[0][:70] if body.strip() else ''))
for i in idx:
    print(*i, sep=' | ')
print(len(idx), 'blocks')
