"""Final-pass Input 8 — fresh 15N correction path; synthetic glutamine areas."""
import numpy as np
import isocor

raw = [24000.0, 5600.0, 1900.0]
corrector = isocor.mscorrectors.MetaboliteCorrectorFactory(
    "C5H10N2O3", tracer="15N", correct_NA_tracer=True,
    tracer_purity=[0.01, 0.99],
)
_, mid, residuum, enrichment = corrector.correct(raw)
assert len(mid) == 3
assert abs(float(np.sum(mid)) - 1.0) < 1e-6
assert 0.0 <= float(enrichment) <= 1.0
print("corrected_15N_mid=", np.round(mid, 6).tolist())
print("residuum=", np.round(residuum, 6).tolist())
print("fractional_15N_enrichment=", round(float(enrichment), 6))
print("assertions=mid_sums_to_one,three_15N_states,enrichment_in_unit_interval")
