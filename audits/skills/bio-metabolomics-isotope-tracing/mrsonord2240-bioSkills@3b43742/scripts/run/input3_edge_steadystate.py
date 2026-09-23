"""
Input 3 (Edge / boundary, REGRESSION of pre-fix Input 3, re-scored against the FIXED
steady-state snippet) -- synthetic time course + documented error-message verification.
User request: "I sampled fractional enrichment for citrate at 0, 5, 15, 30, 60, 90 min and
got 0.00, 0.10, 0.20, 0.28, 0.34, 0.35. Is this at isotopic steady state? Also: I passed a
3-element vector to IsoCor's correct() for a 6-carbon metabolite by mistake -- what happens?"

Part A now follows the FIXED SKILL.md snippet:
  deltas = np.abs(np.diff(fe))
  reached_plateau = len(deltas) >= 3 and np.all(deltas[-3:] < 0.02)
This is the exact regression test the P1 fix was supposed to resolve: pre-fix, the
last-pair-only check returned reached_plateau=True on this still-decelerating series
(last_diff=0.01<0.02); the fix log claims it now returns False.

Part B verifies the "Common Errors" table entry for a length-mismatch vector against the
real isocor error text (unchanged by the fix, re-run as regression).
"""
import numpy as np
import isocor

# --- Part A: steady-state check, FIXED multi-interval rule ---
t = np.array([0, 5, 15, 30, 60, 90])
fe = np.array([0.00, 0.10, 0.20, 0.28, 0.34, 0.35])
deltas = np.abs(np.diff(fe))
reached_plateau = len(deltas) >= 3 and np.all(deltas[-3:] < 0.02)
print("Part A -- steady-state check (FIXED multi-interval rule)")
print("  timepoints (min):", t.tolist())
print("  fractional enrichment:", fe.tolist())
print("  all consecutive deltas:", np.round(deltas, 4).tolist())
print("  last 3 deltas:", np.round(deltas[-3:], 4).tolist())
print("  reached_plateau  :", reached_plateau)
print("  -> PRE-FIX this series was flagged reached_plateau=True (last-pair-only, 0.01<0.02).")
print("     POST-FIX it correctly requires the last 3 deltas [0.08,0.06,0.01] all <0.02;")
print("     0.08 fails, so reached_plateau=False -- the P1 is resolved for this exact series.")

# --- Part B: documented length-mismatch error (Common Errors table), unchanged ---
print("\nPart B -- length-mismatch error text (6-carbon formula, wrong 3-element input)")
corrector = isocor.mscorrectors.MetaboliteCorrectorFactory('C6H12O6', tracer='13C')
try:
    corrector.correct([1000.0, 200.0, 50.0])
    print("  no error raised (UNEXPECTED)")
except Exception as e:
    print(f"  {type(e).__name__}: {e}")
