"""Static checks: every python block in SKILL.md parses; every file/skill the SKILL and usage-guide point at exists; frontmatter; sizes."""
import ast, pathlib, re
from common import *
WT = pathlib.Path(r'F:\OpenScience\wt\al-io2\alignment')
blocks = py_blocks()
print(len(blocks), 'python blocks')
for h, c in blocks:
    try: ast.parse(c); ok(True, f'parses: [{h}]')
    except SyntaxError as e: ok(False, f'syntax error in [{h}]: {e}')
txt = (SKILL/'SKILL.md').read_text(encoding='utf-8'); ug = (SKILL/'usage-guide.md').read_text(encoding='utf-8')
fm = re.match(r'---\n(.*?)\n---', txt, re.S).group(1); print(fm)
ok('name: bio-alignment-io' in fm and 'description:' in fm, 'frontmatter has name+description')
print('SKILL.md lines', len(txt.splitlines()), 'usage-guide lines', len(ug.splitlines()))
ok((WT/'msa-parsing'/'examples'/'neff.py').exists(), 'msa-parsing/examples/neff.py (cross-ref) exists in worktree')
for rel in ['multiple-alignment','pairwise-alignment','msa-parsing','msa-statistics','structural-alignment','alignment-trimming']:
    ok((WT/rel/'SKILL.md').exists(), f'Related skill alignment/{rel} exists')
ok((WT.parent/'sequence-io'/'format-conversion'/'SKILL.md').exists(), 'Related skill sequence-io/format-conversion exists')
for f in ['batch_convert.py','convert_formats.py','read_alignment.py','slice_alignment.py','sample_alignment.aln']:
    ok((SKILL/'examples'/f).exists(), f'examples/{f} shipped')
# things usage-guide points to
for m in re.findall(r'`([^`]+)`', ug): pass
print('usage-guide points at SKILL.md sections:', re.findall(r'"([^"]+)"', ug.split('## Notes')[1]))
for sec in ['Version Compatibility','Format Selection for Downstream Tools','Format-Specific Notes']:
    ok(('## '+sec) in txt, f'SKILL.md has section "{sec}" that usage-guide points to')
# usage-guide: round 2 did not touch it (git diff 818f049..00ddbb3 lists only SKILL.md, convert_formats.py, read_alignment.py)
import subprocess
d = subprocess.run(['git','-C','F:/OpenScience/wt/al-io2','diff','--stat','818f049','00ddbb34e81668b221fb96daa59530e7432495fa'],capture_output=True,text=True,encoding='utf-8').stdout
print(d)
ok('SKILL.md' in d and 'convert_formats.py' in d and 'usage-guide' not in d, 'round 2 diff (non-empty) touches SKILL.md/convert_formats.py/read_alignment.py, not usage-guide.md')
# every python block parse + examples py_compile from copy (no __pycache__: compile() only)
for f in ['batch_convert.py','convert_formats.py','read_alignment.py','slice_alignment.py']:
    try: compile((SKILL/'examples'/f).read_text(encoding='utf-8'), f, 'exec'); ok(True, f'{f} compiles')
    except SyntaxError as e: ok(False, f'{f}: {e}')
summary()
