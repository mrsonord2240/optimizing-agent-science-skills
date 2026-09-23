"""Fresh stress regression: the shipped CLI must retain a genuine isomer tie as Level 3."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
result = subprocess.run([sys.executable, str(root / 'match_library.py'), str(root / 'data' / 'tie_references.mgf'), str(root / 'data' / 'tie_queries.mgf')], text=True, capture_output=True, check=False)
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, end='', file=sys.stderr)
assert result.returncode == 0, result.returncode
assert 'citrate' in result.stdout and 'isocitrate' in result.stdout and 'Level 3' in result.stdout, result.stdout
print('ASSERTIONS: equal isomer spectra remain a candidate set at Level 3, not an arbitrary Level 2a name.')
