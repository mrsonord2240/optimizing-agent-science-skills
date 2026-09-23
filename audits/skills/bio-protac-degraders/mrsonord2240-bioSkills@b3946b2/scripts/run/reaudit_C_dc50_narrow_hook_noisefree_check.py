import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(".").resolve().parent / "skill_copy" / "examples"))
from cooperativity_dc50 import detect_hook, fit_dc50, _hook_curve, _hill

true_params = dict(dmax=65.0, dc50=120.0, hill=1.8, hook_k=2500.0, hook_hill=1.1)
conc = np.logspace(0, 4.3, 18)
clean = _hook_curve(conc, **true_params)  # NO noise this time
hook_info = detect_hook(conc, clean)
print("peak_idx", hook_info["peak_idx"], "peak_conc", hook_info["peak_conc"], "peak_pct", hook_info["peak_pct"])
print("n points in ascending slice:", hook_info["peak_idx"]+2, "of", len(conc))
print("conc at slice boundary:", conc[:hook_info["peak_idx"]+2])
print("clean values in slice:", clean[:hook_info["peak_idx"]+2])
fit = fit_dc50(conc, clean, peak_idx=hook_info["peak_idx"])
print("fit (noise-free):", fit)
print("true:", true_params)
print("dmax err (noise-free):", abs(fit["dmax_fit"]-true_params["dmax"]))
print("dc50 err (noise-free) rel:", abs(fit["dc50_fit"]-true_params["dc50"])/true_params["dc50"])

# what's the max clean value ever reached (true asymptotic max of the hook curve, not pure Hill dmax)?
print("max of full clean curve:", clean.max(), "at conc", conc[np.argmax(clean)])
# pure ascending Hill (no hook) values at same concentrations for comparison
pure = _hill(conc, true_params["dmax"], true_params["dc50"], true_params["hill"])
print("pure Hill (no hook) values:", pure)
