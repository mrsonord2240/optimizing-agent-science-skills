"""
Input 1 (Canonical) — synthetic data.
User request: "I have M+0..M+5 areas for glutamine (C5H10N2O3) from a U-13C5-glutamine
tracing experiment on a triple-quad (low-res). Apply natural-abundance correction with
98% tracer purity and give me the corrected MID and fractional enrichment."

Follows the SKILL.md pattern exactly (MetaboliteCorrectorFactory().correct()), applied to
a metabolite/tracer combination NOT shown in the Skill's own example (glucose), to test
generality of the documented pattern.
"""
import numpy as np
import isocor

# Synthetic raw isotopologue areas M+0..M+5 for glutamine (5 carbons -> 6 isotopologues).
# Constructed to represent partial ~13C5-glutamine labeling with a visible natural-abundance
# shoulder on M+1/M+2, SYNTHETIC (not real instrument data).
raw = [42000.0, 6100.0, 3200.0, 900.0, 1800.0, 15000.0]

corrector = isocor.mscorrectors.MetaboliteCorrectorFactory(
    'C5H10N2O3', tracer='13C',
    correct_NA_tracer=True,
    tracer_purity=[0.02, 0.98])  # [unlabeled, labeled] per-position purity, 98% U-13C5

corrected_area, iso_fraction, residuum, mean_enrichment = corrector.correct(raw)

print("raw areas (M+0..M+5):", raw)
print("corrected areas      :", np.round(corrected_area, 2).tolist())
print("corrected MID         :", np.round(iso_fraction, 4).tolist())
print("residuum               :", np.round(residuum, 6).tolist())
print("fractional enrichment  :", round(mean_enrichment, 4))
print("MID sums to 1          :", abs(sum(iso_fraction) - 1.0) < 1e-6)
