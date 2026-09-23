"""Final-pass Input 3 — prior boundary regression against the current status API."""
import numpy as np
import isocor

fe = np.array([0.00, 0.10, 0.20, 0.28, 0.34, 0.35])
deltas = np.abs(np.diff(fe))
if len(deltas) < 3:
    status = "insufficient timepoints to assess steady state"
elif np.all(deltas[-3:] < 0.02):
    status = "plateau"
else:
    status = "still labeling"
assert status == "still labeling"

corrector = isocor.mscorrectors.MetaboliteCorrectorFactory("C6H12O6", tracer="13C")
try:
    corrector.correct([1000.0, 200.0, 50.0])
except ValueError as exc:
    error_text = str(exc)
else:
    raise AssertionError("IsoCor accepted a wrong-length C6 isotopologue vector")
assert "length of the measured isotopic cluster (3)" in error_text
assert "required number of measurements: 7" in error_text
print("deltas=", np.round(deltas, 3).tolist())
print("status=", status)
print("length_mismatch_error=", error_text)
print("assertions=status_withholds_plateau,error_names_wrong_length,error_names_seven_required")
