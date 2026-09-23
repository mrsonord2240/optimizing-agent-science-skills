"""Phase 2 static and source-integrity checks for this copied skill snapshot."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / 'skill'
files = sorted(p for p in SKILL.rglob('*') if p.is_file())
pyfiles = [p for p in files if p.suffix == '.py']
for path in pyfiles:
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
skill_text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
assert skill_text.startswith('---\n') and '\nname: bio-crispr-screens-prime-editing-screens\n' in skill_text
assert all('../' not in str(p.relative_to(SKILL)) for p in files)
assert not any(token in '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in pyfiles) for token in ('eval(', 'exec('))
result = {
    'copied_skill_md_sha256': hashlib.sha256((SKILL / 'SKILL.md').read_bytes()).hexdigest(),
    'shipped_files': [str(p.relative_to(SKILL)) for p in files],
    'python_files_ast_parsed': [str(p.relative_to(SKILL)) for p in pyfiles],
    'frontmatter_name_ok': True,
    'raw_eval_or_exec_found': False,
}
(ROOT / 'static_checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
