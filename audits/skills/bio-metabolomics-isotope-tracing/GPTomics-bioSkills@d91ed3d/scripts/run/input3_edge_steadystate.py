"""
Input 3 (Edge / boundary) — synthetic time course + documented error-message verification.
User request: "I sampled fractional enrichment for citrate at 0, 5, 15, 30, 60, 90 min and
got 0.00, 0.10, 0.20, 0.28, 0.34, 0.35. Is this at isotopic steady state? Also: I passed a
3-element vector to IsoCor's correct() for a 6-carbon metabolite by mistake -- what happens?"

Part A tests the SKILL.md steady-state snippet's <2% threshold exactly at a boundary value.
Part B verifies the "Common Errors" table entry for a length-mismatch vector against the
real isocor error text (synthetic data throughout).
"""
import numpy as np
import isocor

# --- Part A: steady-state boundary check (SKILL.md pattern) ---
t = np.array([0, 5, 15, 30, 60, 90])
fe = np.array([0.00, 0.10, 0.20, 0.28, 0.34, 0.35])
last_diff = abs(fe[-1] - fe[-2])
reached_plateau = last_diff < 0.02
print("Part A -- steady-state check")
print("  timepoints (min):", t.tolist())
print("  fractional enrichment:", fe.tolist())
print(f"  last-step change: {last_diff:.4f} (threshold <0.02)")
print("  reached_plateau  :", reached_plateau)
print("  -> boundary case: 0.01 < 0.02, so classical MFA would be licensed by this rule,")
print("     but the trend (0.28->0.34->0.35) is still decelerating, not flat; a single")
print("     threshold check on the LAST pair only, with no earlier-pair comparison, would")
print("     pass this borderline series even though full convergence is not yet visually clear.")

# --- Part B: documented length-mismatch error (Common Errors table) ---
print("\nPart B -- length-mismatch error text (6-carbon formula, wrong 3-element input)")
corrector = isocor.mscorrectors.MetaboliteCorrectorFactory('C6H12O6', tracer='13C')
try:
    corrector.correct([1000.0, 200.0, 50.0])
    print("  no error raised (UNEXPECTED)")
except Exception as e:
    print(f"  {type(e).__name__}: {e}")
