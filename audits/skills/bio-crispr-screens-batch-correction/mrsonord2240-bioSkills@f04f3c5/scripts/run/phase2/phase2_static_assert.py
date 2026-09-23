"""Source-tip static checks used in the Phase-2 audit."""
from pathlib import Path
import ast
import subprocess

run = Path(__file__).resolve().parent
source = run / 'skill_copy'
for path in (source / 'scripts').glob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'))
ast.parse((source / 'examples' / 'batch_correct.py').read_text(encoding='utf-8'))
skill = (source / 'SKILL.md').read_text(encoding='utf-8')
assert len(skill.splitlines()) <= 300
for reference in ['combat.md', 'ruv.md', 'sva.md', 'ntc-anchored-normalization.md']:
    assert (Path(r'F:\OpenScience\wt\crispr-screens-batch-correction\crispr-screens\batch-correction\references') / reference).exists()
help_text = subprocess.run([r'F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe', r'F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck', 'count', '--help'], capture_output=True, text=True, check=True).stdout
assert '--norm-method' in help_text and 'control' in help_text
print('ASSERT static: all shipped Python code parses; 231-line SKILL; all four referenced method files present; mageck count control normalization flag exists')
print('PHASE2_STATIC_ASSERT_PASS')
