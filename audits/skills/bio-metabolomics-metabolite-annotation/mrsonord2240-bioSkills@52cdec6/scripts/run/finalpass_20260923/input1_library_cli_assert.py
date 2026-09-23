"""Fresh canonical regression: invoke the shipped library-matching script on synthetic MGF files."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
cmd = [sys.executable, str(root / "match_library.py"), str(root / "data" / "single_references.mgf"), str(root / "data" / "single_queries.mgf")]
result = subprocess.run(cmd, text=True, capture_output=True, check=False)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="", file=sys.stderr)
assert result.returncode == 0, result.returncode
assert "citrate" in result.stdout and " 7" in result.stdout, result.stdout
assert "query_no_overlap" in result.stdout and "Level 5" in result.stdout, result.stdout
assert "Level 2a" not in result.stdout, result.stdout
print("OBSERVATION: single confident hit has score=0.9996 and matches=7 but omits the documented Level 2a label; zero-overlap query correctly prints Level 5.")

# Re-run the current P2 wording correction: add_precursor_mz warns, while scoring raises.
import importlib.util
import numpy as np
from matchms import Spectrum, calculate_scores

spec = importlib.util.spec_from_file_location('audited_match_library', root / 'match_library.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
reference = module.prepare(Spectrum(mz=np.array([59.01, 87.01]), intensities=np.array([1.0, 0.5]), metadata={'compound_name': 'reference', 'precursor_mz': 191.0197}))
missing = module.prepare(Spectrum(mz=np.array([59.01, 87.01]), intensities=np.array([1.0, 0.5]), metadata={'compound_name': 'missing_precursor'}))
try:
    calculate_scores([reference], [missing], module.ModifiedCosine(tolerance=0.005))
except AssertionError as error:
    assert 'Precursor_mz missing' in str(error), error
    print('ASSERTIONS: add_precursor_mz returned with a warning; ModifiedCosine scoring then raised the documented Precursor_mz missing AssertionError.')
else:
    raise AssertionError('Expected ModifiedCosine scoring to reject a missing precursor_mz')
