"""Static checks: every python block in SKILL.md parses; every file/skill the SKILL and usage-guide point at exists; frontmatter; sizes."""
import ast, pathlib, re
from common import *
WT = pathlib.Path(r'F:\OpenScience\wt\al-io\alignment')
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
# did anything the agent needs get lost by dedup? compare against the pre-fix usage-guide from the staging clone
import subprocess
old = subprocess.run(['git','-C',r'F:\OpenScience\external\mrsonord2240__bioSkills','show','354b4992cd8d2f1bee039510af618da0333821f1:alignment/alignment-io/usage-guide.md'],capture_output=True,text=True,encoding='utf-8').stdout
print('---- OLD usage-guide (staging 354b499) ----'); print(old)
summary()
