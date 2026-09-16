"""NEW Input 10: does the pass-4 SILAC labeling-efficiency code actually MODEL
what it claims, or does it just parse?

The fixer reports recovering 0.9306 / 0.0745 from a pilot built at 0.93 / 0.08.
This builds an INDEPENDENT pilot generator (different seed, different peptide
length model, different intensity distribution) and sweeps incorporation and
Arg->Pro conversion over a grid, so the check is whether the estimator tracks
the truth across the range rather than hitting one number once.

The two functions are extracted VERBATIM from the fork's SKILL.md.
"""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

QK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\quantification\SKILL.md"
SRC = [b for h, l, b in blocks(QK, "python") if h.startswith("Check labeling efficiency")][0]
NS = {}
exec(compile(SRC, "<SKILL.md: Check labeling efficiency and Arg->Pro first>", "exec"), NS)
silac_labeling_efficiency = NS["silac_labeling_efficiency"]
arg_to_pro_shift = NS["arg_to_pro_shift"]

AA = list("ACDEFGHIKLMNPQRSTVWY")


def make_pilot(n_peptides, incorporation, rng):
    """HEAVY-ONLY pilot: cells grown in heavy medium, nothing mixed in.

    A fraction (1 - incorporation) of each peptide's protein pool is still the
    pre-existing unlabeled (light) protein. Per-peptide incorporation varies a
    little around the population value; intensities are log-normal over four
    orders of magnitude.
    """
    total = 10 ** rng.uniform(4.0, 8.0, n_peptides)
    # per-peptide incorporation jitter on the logit scale, then clipped
    logit = np.log(incorporation / (1 - incorporation)) + rng.normal(0, 0.35, n_peptides)
    eff_i = np.clip(1 / (1 + np.exp(-logit)), 0.5, 0.999)
    heavy = total * eff_i
    light = total * (1 - eff_i)
    seqs = ["".join(rng.choice(AA, size=rng.integers(7, 26))) for _ in range(n_peptides)]
    return pd.DataFrame({"Sequence": seqs, "Intensity H": heavy, "Intensity L": light}), eff_i


def make_ratio_table(n_peptides, conversion, rng, base_log2=0.0):
    """1:1 forward mix. Arg->Pro drains the heavy channel once per proline."""
    seqs = ["".join(rng.choice(AA, size=rng.integers(7, 26))) for _ in range(n_peptides)]
    npro = np.array([s.count("P") for s in seqs])
    true_log2 = base_log2 + npro * np.log2(1 - conversion) + rng.normal(0, 0.12, n_peptides)
    return pd.DataFrame({"Sequence": seqs, "Ratio H/L": 2.0 ** true_log2}), npro


print("=== silac_labeling_efficiency: does the estimate track the truth? ===")
print(f"{'true eff':>9} {'est eff':>9} {'err':>8} {'med pep':>8} {'<95%':>6} "
      f"{'bias@1:1':>9} {'closed form':>11} {'pass95':>7}")
for true_eff in (0.999, 0.98, 0.95, 0.93, 0.88, 0.75, 0.50):
    rng = np.random.default_rng(20260915 + int(true_eff * 1000))
    pilot, eff_i = make_pilot(1200, true_eff, rng)
    # intensity-weighted TRUE incorporation of this particular draw
    truth = float(pilot["Intensity H"].sum() / (pilot["Intensity H"] + pilot["Intensity L"]).sum())
    r = silac_labeling_efficiency(pilot)
    closed = np.log2(truth / (2 - truth))
    print(f"{truth:9.4f} {r['incorporation']:9.4f} {r['incorporation'] - truth:+8.4f} "
          f"{r['median_peptide_incorporation']:8.4f} {r['peptides_below_95pct']:6d} "
          f"{r['expected_log2_HL_bias_at_1to1']:9.4f} {closed:11.4f} {str(r['pass_95pct']):>7}")

print("\n  -> the 1:1 bias claim, checked by simulation rather than algebra:")
for true_eff in (0.98, 0.93, 0.88):
    rng = np.random.default_rng(7 + int(true_eff * 100))
    # forward 1:1 mix: heavy sample (incorporation eff) + light sample (fully light)
    n = 40000
    tot_h_sample = 10 ** rng.uniform(4, 8, n)
    tot_l_sample = tot_h_sample          # 1:1 by protein amount
    H = tot_h_sample * true_eff
    L = tot_h_sample * (1 - true_eff) + tot_l_sample
    observed = float(np.median(np.log2(H / L)))
    predicted = float(np.log2(true_eff / (2 - true_eff)))
    print(f"    eff {true_eff}: simulated median log2 H/L {observed:+.4f} | "
          f"Skill's formula {predicted:+.4f} | diff {observed - predicted:+.4f}")

print("\n=== arg_to_pro_shift: does the slope recover the conversion? ===")
print(f"{'true conv':>9} {'est conv':>9} {'err':>8} {'slope':>8} {'true slope':>11} "
      f"{'pro-free':>9} {'pro+':>6}")
for conv in (0.0, 0.02, 0.05, 0.08, 0.15, 0.30):
    rng = np.random.default_rng(31337 + int(conv * 1000))
    tab, npro = make_ratio_table(1500, conv, rng)
    r = arg_to_pro_shift(tab)
    true_slope = np.log2(1 - conv)
    print(f"{conv:9.3f} {r['conversion_per_proline']:9.4f} "
          f"{r['conversion_per_proline'] - conv:+8.4f} {r['log2_HL_slope_per_proline']:8.4f} "
          f"{true_slope:11.4f} {r['n_pro_free']:9d} {r['n_pro_containing']:6d}")

print("\n  -> specificity: a FLAT labeling offset must NOT look like Arg->Pro")
rng = np.random.default_rng(99)
tab, _ = make_ratio_table(1500, 0.0, rng, base_log2=-0.30)   # offset, no Pro dose
r = arg_to_pro_shift(tab)
print(f"    flat -0.30 offset, no conversion: slope {r['log2_HL_slope_per_proline']:+.4f}, "
      f"implied conversion {r['conversion_per_proline']:+.4f}, "
      f"median log2 H/L of Pro-free peptides {r['median_log2_HL_pro_free']:+.4f}")

print("\n=== guards ===")
try:
    silac_labeling_efficiency(pd.DataFrame({"Intensity H": [0, 0], "Intensity L": [0, 0]}))
    print("    all-zero table: NO ERROR  <-- guard missing")
except ValueError as e:
    print(f"    all-zero table: ValueError -> {e}")
try:
    r = arg_to_pro_shift(pd.DataFrame({"Sequence": ["AAAK"], "Ratio H/L": [1.0]}))
    print(f"    single peptide, no proline variation: slope {r['log2_HL_slope_per_proline']}")
except Exception as e:
    print(f"    single peptide: {type(e).__name__}: {e}")

print("\n=== regression: the audit's own silac_proteins.csv through the ratio block ===")
RAT = [b for h, l, b in blocks(QK, "python") if h.startswith("Ratios that keep")][0]
ns2 = {}
exec(compile(RAT, "<SKILL.md: Ratios that keep on/off biology>", "exec"), ns2)
sp = pd.read_csv(r"F:\OpenScience\audits\bio-proteomics-quantification\data\silac_proteins.csv")
hcols = [c for c in sp.columns if c.startswith("Intensity H")]
lcols = [c for c in sp.columns if c.startswith("Intensity L")]
ratio, presence = ns2["silac_log2_ratio"](sp[hcols[0]], sp[lcols[0]])
import collections  # noqa: E402
print("    rep1 presence:", dict(collections.Counter(presence)),
      "| inf cells:", int(np.isinf(ratio).sum()))
