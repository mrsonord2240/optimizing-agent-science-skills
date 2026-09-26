"""Regression Input 3: execute the bundled mzML reader on precursor-less and unknown-window scans."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
module_path = root / "run" / "source_examples" / "inspect_mzml.py"
spec = importlib.util.spec_from_file_location("audited_inspect_mzml", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

result = module.inspect_mzml(root / "data" / "synthetic_mixed.mzML")
expected = {"ms1": 4, "ms2": 16, "ms2_without_precursor": 1, "offsets_unknown": 1}
assert result == expected, {"expected": expected, "observed": result}
print(json.dumps(result, indent=2))
