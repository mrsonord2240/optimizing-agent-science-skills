"""Auditor static checks: parse every python block in SKILL.md; determinism re-run of in1/in2."""
import ast, re, subprocess, sys, hashlib
src = open('F:/OpenScience/external/GPTomics__bioSkills/proteomics/data-import/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', src, re.S)
for i, b in enumerate(blocks, 1):
    try:
        ast.parse(b); print(f'python block {i}: parses ({len(b.splitlines())} lines)')
    except SyntaxError as e:
        print(f'python block {i}: SYNTAX ERROR {e}')
print('other fenced blocks:', re.findall(r'```(\w+)', src))
for s in ['in1_maxquant_canonical.py', 'in2_diann_import.py']:
    hs = set()
    for _ in range(2):
        out = subprocess.run([sys.executable, s], capture_output=True, text=True).stdout
        hs.add(hashlib.sha1(out.encode()).hexdigest()[:10])
    print(f'{s}: two runs, distinct stdout hashes = {len(hs)} {hs}')
