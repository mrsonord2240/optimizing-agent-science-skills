#!/usr/bin/env python3
"""Re-auditor's independent verification of cooperativity_dc50.py.

Plants a DIFFERENT synthetic dose-response curve than the fixer's own
(dmax=80, dc50=40nM, hill=1.3, hook_k=5000, hook_hill=1.6, seed=42) and checks
that fit_dc50()/detect_hook() recover this new curve's generating parameters
within a reasonable tolerance -- using the module's real functions, not
reimplementing the fit. Also exercises cooperativity_alpha()'s edge cases and
error path independently.

NOTE: the final assertion in this script is EXPECTED TO FAIL (exit code 1) --
that is the re-audit's actual finding, not a bug in this driver. This
curve's hook onset (hook_k/dc50 ~20, shallow hook_hill=1.1) is much closer to
DC50 than the fixer's own demo curve (hook_k/dc50 ~125), and the
ascending-arm-only fit strategy underestimates Dmax by >12pp as a result --
reproduced noise-free in reaudit_C_dc50_narrow_hook_noisefree_check.py to
confirm it is a structural bias, not sampling noise. See the P2 recommendation
in eval_report_bio-protac-degraders_result.json.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "skill_copy" / "examples"))
from cooperativity_dc50 import (  # noqa: E402
    cooperativity_alpha,
    detect_hook,
    fit_dc50,
    _hook_curve,
)

print("=== cooperativity_alpha: independent edge cases ===")
eq = cooperativity_alpha(15.0, 15.0)
assert eq["label"] == "no cooperativity" and abs(eq["alpha"] - 1.0) < 1e-9
print(f"  equal Kd -> alpha={eq['alpha']:.3f} ({eq['label']}) PASS")

neg = cooperativity_alpha(5.0, 50.0)
assert neg["label"] == "negative cooperativity" and neg["alpha"] < 1.0
print(f"  Kd_binary<Kd_ternary -> alpha={neg['alpha']:.3f} ({neg['label']}) PASS")

try:
    cooperativity_alpha(-1.0, 5.0)
    raise AssertionError("expected ValueError on negative Kd, none raised")
except ValueError:
    print("  negative Kd correctly raises ValueError PASS")

print("\n=== Planted synthetic curve #2 (different from fixer's own) ===")
# Fixer's planted curve: dmax=80, dc50=40nM, hill=1.3, hook_k=5000, hook_hill=1.6, seed=42
# This curve: different Dmax, DC50 (3x higher), hill slope, hook location, seed, point count.
true_params = dict(dmax=65.0, dc50=120.0, hill=1.8, hook_k=2500.0, hook_hill=1.1)
rng = np.random.default_rng(123)
n_points = 18
conc = np.logspace(0, 4.3, n_points)  # ~1 nM to ~20 uM
clean = _hook_curve(conc, **true_params)
noise = rng.normal(0, 2.5, size=conc.shape)
observed = np.clip(clean + noise, 0, 100)

hook_info = detect_hook(conc, observed)
print(f"  peak={hook_info['peak_pct']:.1f}% at {hook_info['peak_conc']:.0f} nM, "
      f"final={hook_info['final_pct']:.1f}% at {conc[-1]:.0f} nM, hook_flag={hook_info['hook_effect']}")
assert hook_info["hook_effect"] is True, "expected planted curve #2 to show a hook effect"

fit = fit_dc50(conc, observed, peak_idx=hook_info["peak_idx"])
dc50_err = abs(fit["dc50_fit"] - true_params["dc50"]) / true_params["dc50"]
dmax_err = abs(fit["dmax_fit"] - true_params["dmax"])
print(f"  fitted DC50={fit['dc50_fit']:.1f} nM (planted {true_params['dc50']}), rel_err={dc50_err:.1%}")
print(f"  fitted Dmax={fit['dmax_fit']:.1f}% (planted {true_params['dmax']}), abs_err={dmax_err:.1f}pp")
assert dc50_err < 0.30, f"DC50 recovery error too large: {dc50_err:.1%}"
assert dmax_err < 12.0, f"Dmax recovery error too large: {dmax_err:.1f}pp"
print("  PASS: fit recovers planted curve #2's DC50 and Dmax within tolerance")

print("\n=== Sanity: a genuinely monotonic (non-hook) curve should NOT be flagged ===")
conc2 = np.logspace(0, 3.5, 12)
monotonic = 90.0 / (1.0 + (25.0 / conc2) ** 1.5)
hook_info2 = detect_hook(conc2, monotonic)
assert hook_info2["hook_effect"] is False, "hook incorrectly flagged on a monotonic curve"
print(f"  monotonic curve hook_flag={hook_info2['hook_effect']} PASS (no false positive)")

print("\nALL INDEPENDENT DC50/COOPERATIVITY CHECKS PASSED")
