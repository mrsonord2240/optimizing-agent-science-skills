"""Extract every fenced code block of the Skill's SKILL.md into a directory so each can be run literally."""
import re, pathlib, sys
skill = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
sect = ''
n = 0
pat = re.compile(r'^(#{1,3} [^\n]*)$|^```(\w*)\n(.*?)^```', re.M | re.S)
for m in pat.finditer(skill):
    if m.group(1):
        sect = re.sub(r'\W+', '_', m.group(1).strip('# '))[:30]
        continue
    n += 1
    lang = m.group(2) or 'txt'
    ext = {'python': 'py', 'bash': 'sh', 'ini': 'ini'}.get(lang, lang)
    p = out / f'{n:02d}_{sect}.{ext}'
    p.write_text(m.group(3), encoding='utf-8', newline='\n')
    print(p.name, len(m.group(3).splitlines()), 'lines')
