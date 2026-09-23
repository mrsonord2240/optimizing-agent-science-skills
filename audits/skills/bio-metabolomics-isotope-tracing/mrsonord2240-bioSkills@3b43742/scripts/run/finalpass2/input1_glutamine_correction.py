"""Final-pass Input 1 — prior canonical regression; synthetic areas."""
import numpy as np
import isocor

raw = [42000.0, 6100.0, 3200.0, 900.0, 1800.0, 15000.0]
corrector = isocor.mscorrectors.MetaboliteCorrectorFactory(
    "C5H10N2O3", tracer="13C", correct_NA_tracer=True,
    tracer_purity=[0.02, 0.98],
)
_, mid, residuum, enrichment = corrector.correct(raw)
assert len(mid) == 6
assert abs(float(np.sum(mid)) - 1.0) < 1e-6
assert 0.0 <= float(enrichment) <= 1.0
print("corrected_mid=", np.round(mid, 6).tolist())
print("residuum=", np.round(residuum, 6).tolist())
print("fractional_enrichment=", round(float(enrichment), 6))
print("assertions=mid_sums_to_one,length_is_six,enrichment_in_unit_interval")
