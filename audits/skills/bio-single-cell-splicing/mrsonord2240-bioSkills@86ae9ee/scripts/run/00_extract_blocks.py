"""Extract every fenced code block from run/skill/SKILL.md (and usage-guide.md) to blocks/NN_<lang>.<ext>; print an index with line numbers."""
import re, os, sys
os.makedirs('blocks', exist_ok=True)
ext = {'bash': 'sh', 'r': 'R', 'python': 'py', '': 'txt'}
for src in ['skill/SKILL.md', 'skill/usage-guide.md']:
    txt = open(src, encoding='utf-8').read().split('\n')
    n = 0; i = 0
    while i < len(txt):
        m = re.match(r'^```(\w*)\s*$', txt[i])
        if m:
            lang = m.group(1); start = i + 1; j = start
            while not txt[j].startswith('```'): j += 1
            n += 1
            tag = 'S' if 'SKILL' in src else 'U'
            fn = f'blocks/{tag}{n:02d}_{lang or "txt"}.{ext.get(lang, "txt")}'
            open(fn, 'w', encoding='utf-8', newline='\n').write('\n'.join(txt[start:j]) + '\n')
            print(fn, 'lines', start + 1, '-', j, ':', txt[start][:70])
            i = j
        i += 1
