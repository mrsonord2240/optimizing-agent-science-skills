#!/usr/bin/env python3
"""Re-auditor's independent verification of ternary_geometry_screen.py.

Runs cases the fixer's own __main__ block did NOT use:
1. A literature-representative PEG3 linker (MZ1-style JQ1->VHL PROTAC linker
   chemistry: -O-CH2CH2-O-CH2CH2-O-CH2CH2- backbone) fed directly to
   linker_reach(), not through the LINKERS dict.
2. A finer-grained pure-alkyl chain-length series (C1..C7 spacer bonds between
   attachment carbons, i.e. 7 points instead of the fixer's 3-point
   short/medium/long check) to see whether monotonicity holds throughout, not
   only at 3 widely-spaced samples.
3. An independent re-implementation of the all-trans zigzag theoretical bound
   (not calling the module's private _theoretical_max_reach_alkyl) cross-checked
   against every alkyl point.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "skill_copy" / "examples"))
from ternary_geometry_screen import linker_reach  # noqa: E402

BOND_LEN = 1.54
TETRA_HALF_ANGLE = math.radians(54.75)


def independent_theoretical_bound(n_bonds):
    return n_bonds * BOND_LEN * math.sin(TETRA_HALF_ANGLE)


print("=== Case 1: literature-representative PEG3 linker (MZ1-style), not in LINKERS ===")
peg3_linker = "[*:1]CCOCCOCCOCC[*:2]"
r = linker_reach(peg3_linker, n_confs=40, seed=7)
print(f"  n_bonds={r['n_bonds']}  min={r['min_A']:.2f}  mean={r['mean_A']:.2f}  max={r['max_A']:.2f}  n_confs={r['n_confs']}")
theo = independent_theoretical_bound(r["n_bonds"])
print(f"  independent theoretical bound (all-trans zigzag): {theo:.2f} A")
assert r["max_A"] <= theo + 0.5, "PEG3 linker sampled max exceeds independent theoretical bound"
assert r["n_confs"] > 0, "no conformers embedded for PEG3 linker"
print("  PASS: PEG3 linker reach within independent theoretical bound\n")

print("=== Case 2: fine-grained pure-alkyl series, C1..C7 spacer bonds ===")
alkyl_smis = {
    f"c{n}": f"[*:1]{'C' * n}[*:2]" for n in range(1, 8)
}
results = {}
for name, smi in alkyl_smis.items():
    results[name] = linker_reach(smi, n_confs=30, seed=42)
    theo = independent_theoretical_bound(results[name]["n_bonds"])
    print(f"  {name}: n_bonds={results[name]['n_bonds']:>2}  max={results[name]['max_A']:.2f} A  theo_bound={theo:.2f} A")
    assert results[name]["max_A"] <= theo + 0.5, f"{name}: sampled max exceeds independent theoretical bound"

max_by_chain = [results[f"c{n}"]["max_A"] for n in range(1, 8)]
print(f"  max_A sequence: {[round(x,2) for x in max_by_chain]}")
non_decreasing = all(max_by_chain[i] <= max_by_chain[i + 1] + 1e-6 for i in range(len(max_by_chain) - 1))
assert non_decreasing, "reach is not monotonically non-decreasing across the fine-grained C1..C7 series"
print("  PASS: max reach is monotonically non-decreasing across 7 alkyl chain lengths (finer grain than fixer's 3-point check)\n")

print("ALL INDEPENDENT TERNARY-REACH CHECKS PASSED")
