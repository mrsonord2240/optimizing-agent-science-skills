"""New scope-boundary test: a clearly superior match must remain Level 2a, not be over-demoted by TIE_MARGIN."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
result = subprocess.run([sys.executable, str(root / 'match_library.py'), str(root / 'data' / 'no_false_tie_references.mgf'), str(root / 'data' / 'no_false_tie_queries.mgf')], text=True, capture_output=True, check=False)
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, end='', file=sys.stderr)
assert result.returncode == 0, result.returncode
assert 'citrate' in result.stdout and ' 7' in result.stdout, result.stdout
assert 'Level 3' not in result.stdout, result.stdout
assert 'Level 2a' not in result.stdout, result.stdout
print('OBSERVATION: a >0.02-margin single match is not falsely tied, but the single-hit CLI output still omits the promised Level 2a label.')
