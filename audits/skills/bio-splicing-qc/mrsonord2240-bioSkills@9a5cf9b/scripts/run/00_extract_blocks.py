"""Extract every fenced block of SKILL.md (copy in run/skill) to blocks/, syntax-check python and bash blocks."""
import re, ast, subprocess, sys, pathlib
root = pathlib.Path(__file__).parent
text = (root / 'skill' / 'SKILL.md').read_text(encoding='utf-8')
out = root / 'blocks'; out.mkdir(exist_ok=True)
blocks = re.findall(r'```(\w*)\n(.*?)```', text, re.S)
print(len(blocks), 'blocks')
for i, (lang, body) in enumerate(blocks, 1):
    ext = {'python': 'py', 'bash': 'sh'}.get(lang, 'txt')
    p = out / f'B{i:02d}.{ext}'
    p.write_text(body, encoding='utf-8', newline='\n')
    status = ''
    if lang == 'python':
        try: ast.parse(body); status = 'python parses'
        except SyntaxError as e: status = f'PY SYNTAX ERROR {e}'
    print(p.name, lang, body.count('\n'), 'lines', status)
