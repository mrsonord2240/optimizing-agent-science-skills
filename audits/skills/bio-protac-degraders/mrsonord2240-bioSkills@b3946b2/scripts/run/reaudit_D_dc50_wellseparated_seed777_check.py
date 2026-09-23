import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(".").resolve().parent / "skill_copy" / "examples"))
from cooperativity_dc50 import detect_hook, fit_dc50, _hook_curve

# Well-separated hook (ratio hook_k/dc50 ~100, similar to fixer's own 5000/40=125), but
# different absolute values/seed than both the fixer's curve and my failing curve #2.
true_params = dict(dmax=55.0, dc50=8.0, hill=1.4, hook_k=900.0, hook_hill=2.0)
rng = np.random.default_rng(777)
conc = np.logspace(-0.5, 3.7, 16)
clean = _hook_curve(conc, **true_params)
noise = rng.normal(0, 2.0, size=conc.shape)
observed = np.clip(clean + noise, 0, 100)
hook_info = detect_hook(conc, observed)
print("hook flag:", hook_info["hook_effect"], "peak:", hook_info["peak_pct"], "at", hook_info["peak_conc"])
fit = fit_dc50(conc, observed, peak_idx=hook_info["peak_idx"])
dc50_err = abs(fit["dc50_fit"]-true_params["dc50"])/true_params["dc50"]
dmax_err = abs(fit["dmax_fit"]-true_params["dmax"])
print(f"fit dc50={fit['dc50_fit']:.2f} (true {true_params['dc50']}), rel_err={dc50_err:.1%}")
print(f"fit dmax={fit['dmax_fit']:.2f} (true {true_params['dmax']}), abs_err={dmax_err:.1f}pp")
print("ratio hook_k/dc50:", true_params["hook_k"]/true_params["dc50"])
