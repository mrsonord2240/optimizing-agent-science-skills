"""Canonical Input 1 companion: prove the current source's missing-precursor error timing."""
from pathlib import Path
import importlib.util
import numpy as np
from matchms import Spectrum, calculate_scores

root = Path(__file__).resolve().parent
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
