"""In3 verdict: tipdate.py's LSD2 regex missed a negative CI bound; re-parse and apply the Skill's rules."""
import json
import re

import numpy as np

txt = open("lsd2.timetree.lsd", errors="replace").read()
num = r"([-\d.eE+]+)"
m = re.search(rf"rate\s+{num}\s*\[{num};\s*{num}\],\s*tMRCA\s+{num}\s*\[{num};\s*{num}\]", txt)
rate, rlo, rhi, t, tlo, thi = (float(x) for x in m.groups())
j = json.load(open("tipdate_results.json"))
reps = np.array(j["dr_reps"])
lo, hi = np.percentile(reps, [2.5, 97.5])
print(f"LSD2 (Skill command): rate {rate:.3e} [{rlo:.3e}; {rhi:.3e}], tMRCA {t:.2f} [{tlo:.4g}; {thi:.2f}]")
print(f"truth: rate {j['truth']['strict_clock_rate']}, tMRCA {j['truth']['true_tmrca']}")
print(f"root-to-tip: slope {j['rtt']['slope']:.3e}, R^2 {j['rtt']['r2']:.3f}, x-intercept {j['rtt']['x_intercept']:.2f}")
print(f"date-randomization ({len(reps)} reps): 95% range [{lo:.3e}, {hi:.3e}]")
overlap = rlo <= hi and rhi >= lo
print("real rate CI overlaps randomized cloud:", overlap, "-> NO temporal signal; do not date" if overlap else "")
print("R^2 below ~0.2 red flag:", j["rtt"]["r2"] < 0.2)
