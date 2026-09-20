#!/usr/bin/env python3
"""Dump every fenced code block of the fixed SKILL.md verbatim to blocks/NNN_<lang>.<ext>, plus an index with the nearest heading."""
import re, os, sys
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
head = ''; i = 0; n = 0; idx = []
while i < len(src):
    l = src[i]
    if l.startswith('#') and not l.startswith('```'):
        head = l.strip('# ').strip()
    m = re.match(r'^(\s*)```(\w*)', l)
    if m:
        lang = m.group(2) or 'txt'; j = i + 1; body = []
        while j < len(src) and not src[j].strip().startswith('```'):
            body.append(src[j]); j += 1
        n += 1
        ext = {'bash': 'sh', 'python': 'py'}.get(lang, 'txt')
        fn = f'{n:03d}_{lang}.{ext}'
        open(os.path.join(out, fn), 'w', encoding='utf-8', newline='\n').write('\n'.join(body) + '\n')
        idx.append(f'{fn}\tline {i+1}\t{head}')
        i = j
    i += 1
open(os.path.join(out, 'INDEX.tsv'), 'w', encoding='utf-8').write('\n'.join(idx) + '\n')
print('\n'.join(idx))
