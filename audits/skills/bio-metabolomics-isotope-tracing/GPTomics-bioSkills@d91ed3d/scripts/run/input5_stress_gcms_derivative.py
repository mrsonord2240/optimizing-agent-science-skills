"""
Input 5 (Stress / multi-part) — synthetic data.
User request: "My alanine is TBDMS-derivatized for GC-MS (derivative adds C6H15Si to the
C3H7NO2 backbone). I have M+0..M+3 raw areas from a U-13C3-alanine tracer at 98% purity.
Correct for natural abundance including the derivative formula, AND separately: I tried to
set a high-resolution correction by only giving mz_of_resolution without resolution -- what
error do I get?"

Part A: derivative_formula correction pattern from SKILL.md ("GC-MS MID still wrong after
correction" failure mode / derivative formula requirement).
Part B: documented "ValueError half-defined resolution" Common Errors entry.
"""
import numpy as np
import isocor

print("Part A -- TBDMS-derivatized alanine correction (synthetic GC-MS areas)")
raw = [8000.0, 1400.0, 22000.0, 3100.0]  # synthetic M+0..M+3 for 3-carbon alanine backbone
corrector = isocor.mscorrectors.MetaboliteCorrectorFactory(
    'C3H7NO2', tracer='13C', derivative_formula='C6H15Si',
    correct_NA_tracer=True, tracer_purity=[0.02, 0.98])
corrected_area, iso_fraction, residuum, mean_enrichment = corrector.correct(raw)
print("  raw areas (M+0..M+3)      :", raw)
print("  corrected MID              :", np.round(iso_fraction, 4).tolist())
print("  fractional enrichment      :", round(mean_enrichment, 4))
print("  MID sums to 1              :", abs(sum(iso_fraction) - 1.0) < 1e-6)

print("\nPart A2 -- same raw areas WITHOUT derivative formula (shows why it matters)")
corrector_noderiv = isocor.mscorrectors.MetaboliteCorrectorFactory(
    'C3H7NO2', tracer='13C', correct_NA_tracer=True, tracer_purity=[0.02, 0.98])
_, iso_fraction_noderiv, _, mean_enr_noderiv = corrector_noderiv.correct(raw)
print("  corrected MID (no derivative, WRONG for this GC-MS case):",
      np.round(iso_fraction_noderiv, 4).tolist())
print("  fractional enrichment (no derivative)                    :", round(mean_enr_noderiv, 4))
print("  MID differs from Part A by (max abs):",
      round(float(np.max(np.abs(np.array(iso_fraction) - np.array(iso_fraction_noderiv)))), 4))

print("\nPart B -- half-defined resolution error (mz_of_resolution without resolution)")
try:
    isocor.mscorrectors.MetaboliteCorrectorFactory(
        'C6H12O6', tracer='13C', mz_of_resolution=400)
    print("  no error raised (UNEXPECTED)")
except Exception as e:
    print(f"  {type(e).__name__}: {e}")
