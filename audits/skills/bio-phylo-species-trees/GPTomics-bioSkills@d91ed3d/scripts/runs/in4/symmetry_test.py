"""Auditor-added minority-quartet symmetry test for Input 4 (SYNTHETIC intro set), 2026-09-15.

The Skill says to "confirm the asymmetry" (q2 != q3) before invoking introgression but gives no test.
Under pure ILS the two minority quartet topologies are equally likely, so the effective gene counts f2 and f3 written
by `astral -u 2` (estimated gene trees, runs/in4/species_annot.tre) are compared with an exact two-sided binomial test
of H0: f2 = f3. The counts are quartet-averaged (fractional) and are rounded to integers for the test.
The same f2/f3 values appear as t2/t3 counts in runs/in4/est/freqQuad.csv.

Produces runs/in4/symmetry_test.txt (original run was this code via stdin; output identical).
"""
from scipy.stats import binomtest

ROWS = [("Sp_A,Sp_B", 39, 43), ("Sp_A,Sp_B,Sp_C", 19.4167, 72.6667), ("Sp_D,Sp_E", 21.4444, 16.6667),
        ("Sp_A..Sp_E", 22.25, 29.8333), ("Sp_A..Sp_E,Sp_H", 17.2, 15.4)]

if __name__ == "__main__":
    print("branch               f2      f3      p(two-sided, H0 f2=f3)  verdict")
    for name, f2, f3 in ROWS:
        k, n = round(f2), round(f2) + round(f3)
        p = binomtest(k, n, 0.5).pvalue
        print(f"{name:<20} {f2:7.2f} {f3:7.2f}  {p:.2e}               {'ASYMMETRIC' if p < 0.05 else 'symmetric'}")
