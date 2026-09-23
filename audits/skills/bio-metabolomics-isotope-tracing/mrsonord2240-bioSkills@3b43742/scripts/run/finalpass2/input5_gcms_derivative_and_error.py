"""Final-pass Input 5 — prior GC-MS derivative and error-text regression; synthetic areas."""
import numpy as np
import isocor

raw = [8000.0, 1400.0, 22000.0, 3100.0]
with_derivative = isocor.mscorrectors.MetaboliteCorrectorFactory(
    "C3H7NO2", tracer="13C", derivative_formula="C6H15Si",
    correct_NA_tracer=True, tracer_purity=[0.02, 0.98],
)
without_derivative = isocor.mscorrectors.MetaboliteCorrectorFactory(
    "C3H7NO2", tracer="13C", correct_NA_tracer=True,
    tracer_purity=[0.02, 0.98],
)
_, mid_derivative, _, _ = with_derivative.correct(raw)
_, mid_no_derivative, _, _ = without_derivative.correct(raw)
delta = float(np.max(np.abs(np.asarray(mid_derivative) - np.asarray(mid_no_derivative))))
assert abs(float(np.sum(mid_derivative)) - 1.0) < 1e-6
assert delta > 0.01
try:
    isocor.mscorrectors.MetaboliteCorrectorFactory(
        "C6H12O6", tracer="13C", mz_of_resolution=400
    )
except ValueError as exc:
    message = str(exc)
else:
    raise AssertionError("half-defined high-resolution parameters unexpectedly succeeded")
documented = "MetaboliteCorrectorFactory was unable to select a correction strategy. Please check your inputs."
assert message == documented
print("mid_with_derivative=", np.round(mid_derivative, 6).tolist())
print("max_abs_mid_difference_without_derivative=", round(delta, 6))
print("half_defined_resolution_error_exact_match=", message == documented)
