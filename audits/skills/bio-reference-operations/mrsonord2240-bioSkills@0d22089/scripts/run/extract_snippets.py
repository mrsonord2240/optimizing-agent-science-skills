#!/usr/bin/env python
"""Extract every fenced code block of the shipped SKILL.md / usage-guide.md verbatim into snippets/<doc>_<NN>_<lang>.txt so that what is executed is exactly what ships."""
import os, re, sys
ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
for doc, tag in (('SKILL.md', 'skill'), ('usage-guide.md', 'ug')):
    txt = open(os.path.join(ROOT, doc), encoding='utf-8').read()
    for n, m in enumerate(re.finditer(r'```(\w*)\n(.*?)```', txt, re.S), 1):
        lang, body = m.group(1) or 'txt', m.group(2)
        fn = f'{tag}_{n:02d}_{lang}.txt'
        open(os.path.join(OUT, fn), 'w', encoding='utf-8', newline='\n').write(body)
        print(fn, '|', (body.strip().splitlines() or [''])[0][:80])
