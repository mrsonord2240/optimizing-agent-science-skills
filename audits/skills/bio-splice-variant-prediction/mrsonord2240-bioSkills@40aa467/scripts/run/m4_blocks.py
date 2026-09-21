"""M4: extract every fenced block from the fixed SKILL.md, syntax-check python (ast) and bash (bash -n); list files referenced
by SKILL.md/usage-guide.md and check they exist (gate 8)."""
import re, ast, subprocess, os, sys, glob
txt = open('skill/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```(\w*)\n(.*?)```', txt, re.S)
os.makedirs('blocks', exist_ok=True)
print('fenced blocks:', len(blocks), [b[0] or '(none)' for b in blocks])
for i, (lang, body) in enumerate(blocks, 1):
    p = f'blocks/B{i:02d}.{ {"python": "py", "bash": "sh"}.get(lang, "txt")}'
    open(p, 'w', encoding='utf-8', newline='\n').write(body)
    if lang == 'python':
        try:
            ast.parse(body); print(f'B{i:02d} python parses')
        except SyntaxError as e:
            print(f'B{i:02d} python SYNTAX ERROR', e)
    elif lang == 'bash':
        r = subprocess.run(['bash', '-n', p], capture_output=True, text=True)
        print(f'B{i:02d} bash -n rc={r.returncode}', r.stderr.strip()[:200])
# shipped means present
for doc in ['skill/SKILL.md', 'skill/usage-guide.md']:
    t = open(doc, encoding='utf-8').read()
    refs = set(re.findall(r'`((?:examples|references|scripts|assets|templates)/[^`\s]+)`', t)) | set(re.findall(r'\b((?:examples)/[\w./-]+\.\w+)', t))
    for r in sorted(refs):
        print(doc, '->', r, 'EXISTS' if os.path.exists('skill/' + r) else 'MISSING')
for f in glob.glob('skill/examples/*.py'):
    ast.parse(open(f, encoding='utf-8').read()); print('parses:', f)
