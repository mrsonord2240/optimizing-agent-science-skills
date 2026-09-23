"""
Input 5 (Stress / multi-part) — "For a CRBN PROTAC series (5 compounds, use
the enumerated linkers), report: (a) the composition/property table, (b)
cooperativity alpha from provided synthetic binary/ternary Kd values, and
(c) DC50/Dmax and hook-effect detection from a synthetic cellular
dose-response dataset. Flag any compound whose dose-response shows a hook
effect."

Multi-part stress input spanning three of the Skill's documented workflows:
linker enumeration + property calc (protac_enumerate.py, executed),
cooperativity alpha (SKILL.md formula, executed on synthetic Kd data), and
DC50/Dmax/hook-effect characterization from a synthetic dose-response curve
(4-parameter logistic fit + hook detection, using numpy/scipy which the
audit env already has). Datasets are synthetic and generated inline; this
is declared explicitly per AUDIT_BRIEF Step 2.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-protac-degraders\skill_copy")
from protac_enumerate import enumerate_linkers, compute_protac_size
import numpy as np
from scipy.optimize import curve_fit

target_fragment = "[*]c1cc(Nc2ncc(-c3ccccc3)nc2N2CCNCC2)ccn1"
e3_fragment = "[*]c1ccc2c(c1)C(=O)N(C1CCC(=O)NC1=O)C2=O"

# (a) composition table for 5 compounds
results = enumerate_linkers(target_fragment, e3_fragment)
five = list(results.items())[:5]
print("(a) Composition table (5-compound series)")
for name, smi in five:
    props = compute_protac_size(smi)
    print(f"  {name:<18} MolWt={props['MolWt']:.1f}  TPSA={props['TPSA']:.1f}  LogP={props['LogP']:.2f}")

# (b) cooperativity alpha from synthetic ITC-style Kd values (nM)
print("\n(b) Cooperativity alpha (synthetic binary vs ternary Kd, nM)")
synthetic_kd = {
    "short_alkyl": {"Kd_binary": 850.0, "Kd_ternary": 62.0},
    "short_pegylated": {"Kd_binary": 850.0, "Kd_ternary": 140.0},
    "piperazine_short": {"Kd_binary": 850.0, "Kd_ternary": 910.0},
    "medium_alkyl": {"Kd_binary": 850.0, "Kd_ternary": 1500.0},
    "medium_pegylated": {"Kd_binary": 850.0, "Kd_ternary": 310.0},
}
for name, kd in synthetic_kd.items():
    alpha = kd["Kd_binary"] / kd["Kd_ternary"]
    tag = "positive" if alpha > 1 else ("negative" if alpha < 1 else "none")
    print(f"  {name:<18} alpha={alpha:.2f}  ({tag} cooperativity)")

# (c) DC50/Dmax from synthetic cellular dose-response with a hook effect
print("\n(c) DC50/Dmax with hook-effect detection (synthetic cellular data)")


def logistic_with_hook(conc_log10, dc50_log10, dmax, hook_log10, hook_strength):
    """4-parameter logistic degradation curve with an added high-dose hook term."""
    sigmoid = dmax / (1 + 10 ** (dc50_log10 - conc_log10))
    hook = hook_strength * np.clip(conc_log10 - hook_log10, 0, None) ** 2
    return np.clip(sigmoid - hook, 0, 100)


rng = np.random.default_rng(42)  # seeded -> deterministic synthetic data
conc_log10 = np.linspace(-9, -4.3, 14)  # 1 nM .. ~50 uM
true_params = dict(dc50_log10=-7.3, dmax=88.0, hook_log10=-5.5, hook_strength=180.0)
clean = logistic_with_hook(conc_log10, **true_params)
noisy = np.clip(clean + rng.normal(0, 2.0, size=clean.size), 0, 100)

for c, d in zip(10 ** conc_log10, noisy):
    print(f"  [PROTAC]={c*1e9:8.1f} nM   %degradation={d:5.1f}")

peak_idx = int(np.argmax(noisy))
downturn = peak_idx < len(noisy) - 1 and noisy[-1] < noisy[peak_idx] - 15
print(f"\n  Peak degradation {noisy[peak_idx]:.1f}% at "
      f"{10**conc_log10[peak_idx]*1e9:.0f} nM; final-point degradation "
      f"{noisy[-1]:.1f}% at {10**conc_log10[-1]*1e9:.0f} nM.")
print(f"  Hook effect flag (>15pp downturn from peak to top concentration): {downturn}")

try:
    popt, _ = curve_fit(
        lambda x, d50, dm: dm / (1 + 10 ** (d50 - x)),
        conc_log10[: peak_idx + 2], noisy[: peak_idx + 2],
        p0=[-7.0, 90.0], maxfev=5000,
    )
    print(f"  Fitted (ascending-arm only) DC50 = {10**popt[0]*1e9:.1f} nM, Dmax = {popt[1]:.1f}%")
except Exception as e:
    print(f"  Curve fit failed: {e}")

print("\nNote: cooperativity alpha and DC50/Dmax above are computed from "
      "SYNTHETIC data for demonstration; alpha must come from a real ITC/"
      "SPR experiment and DC50/Dmax from a real cellular assay, as SKILL.md "
      "states throughout.")
