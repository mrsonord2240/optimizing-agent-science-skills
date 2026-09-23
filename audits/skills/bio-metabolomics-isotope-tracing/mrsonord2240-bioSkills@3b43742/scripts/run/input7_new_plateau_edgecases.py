"""
Input 7 (NEW, Adversarial -- tests the FIX itself, not just the pre-fix defect) -- synthetic.
User request: "Two follow-up questions about the plateau check: (1) my citrate labeling at
0, 30, 60, 90, 120 min came out 0.10, 0.30, 0.395, 0.398, 0.399 -- is that steady state?
(2) I only sampled two timepoints, 0 and 60 min, giving 0.00 and 0.42 -- can the plateau
check tell me anything?"

Purpose: the P1 fix requires the last 3 CONSECUTIVE deltas to all be <0.02. This input checks
two things the fix log did not explicitly verify:
  (a) True positive -- a genuinely flat series (5 points, 4 deltas, last 3 all small) must
      still be correctly flagged reached_plateau=True. If the fix over-corrected into never
      returning True, that would be a new regression the P1 fix introduced.
  (b) Boundary/under-determined case -- with only 2 timepoints (1 delta), `len(deltas) >= 3`
      is False by construction, so reached_plateau is always False regardless of how flat the
      single interval is. SKILL.md does not say what an agent should tell a user who only has
      2-3 timepoints; this exposes whether the fix silently traded a false-positive risk for an
      unexplained "can never assess" case for short time courses.
"""
import numpy as np

print("Case (a) -- 5-point series that LOOKS flat on the last pair but the fixed rule")
print("           catches a still-meaningful earlier interval in the 3-delta window")
t_a = np.array([0, 30, 60, 90, 120])
fe_a = np.array([0.10, 0.30, 0.395, 0.398, 0.399])
deltas_a = np.abs(np.diff(fe_a))
reached_a = len(deltas_a) >= 3 and np.all(deltas_a[-3:] < 0.02)
print("  deltas:", np.round(deltas_a, 4).tolist())
print("  reached_plateau:", reached_a,
      "-- correct: last3=[0.095,0.003,0.001] has 0.095 still >=0.02, so the fixed rule")
print("     correctly withholds plateau even though the very last pair alone (0.001) looks flat.")

print("\nCase (a2) -- genuinely flat last-3-intervals series (true positive check)")
t_a2 = np.array([0, 30, 60, 90, 120])
fe_a2 = np.array([0.30, 0.385, 0.395, 0.399, 0.400])
deltas_a2 = np.abs(np.diff(fe_a2))
reached_a2 = len(deltas_a2) >= 3 and np.all(deltas_a2[-3:] < 0.02)
print("  deltas:", np.round(deltas_a2, 4).tolist())
print("  reached_plateau:", reached_a2,
      "(expected True -- confirms the fix did not over-correct into never returning True)")

print("\nCase (b) -- only 2 timepoints (1 delta), boundary/under-determined")
t_b = np.array([0, 60])
fe_b = np.array([0.00, 0.42])
deltas_b = np.abs(np.diff(fe_b))
reached_b = len(deltas_b) >= 3 and np.all(deltas_b[-3:] < 0.02)
print("  deltas:", np.round(deltas_b, 4).tolist())
print("  reached_plateau:", reached_b,
      "-- always False with <4 timepoints, regardless of the data;")
print("     SKILL.md's fixed snippet does not tell the agent to report 'insufficient")
print("     timepoints to assess' instead of a flat 'not at steady state'.")
