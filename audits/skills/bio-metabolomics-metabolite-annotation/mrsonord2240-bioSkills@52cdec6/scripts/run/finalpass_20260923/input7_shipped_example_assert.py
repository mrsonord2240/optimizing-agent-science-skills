"""New source-integrity test: run the shipped example byte-for-byte and inspect its regression assertions/output."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
source = Path(r'F:\OpenScience\wt\metabolomics-metabolite-annotation\metabolomics\metabolite-annotation\examples\annotate_features.py')
assert (root / 'input7_shipped_example.py').read_bytes() == source.read_bytes(), 'audit copy differs from the exact-tip shipped example'
result = subprocess.run([sys.executable, str(root / 'input7_shipped_example.py')], text=True, capture_output=True, check=False)
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, end='', file=sys.stderr)
assert result.returncode == 0, result.returncode
assert 'query_strong' in result.stdout and 'level=2a' in result.stdout, result.stdout
assert 'query_promiscuous' in result.stdout and 'matches=2' in result.stdout and 'level=3' in result.stdout, result.stdout
print('ASSERTIONS: audit copy is byte-identical to the exact-tip shipped example; self-checks passed; high score/few peaks remains Level 3.')
