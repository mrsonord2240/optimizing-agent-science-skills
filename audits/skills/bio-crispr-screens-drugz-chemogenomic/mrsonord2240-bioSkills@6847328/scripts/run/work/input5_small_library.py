"""Input 5 - Stress: small/pilot count table vs --half_window_size. Regression of pre-fix
Input 5 plus the fix's specific claim: default half_window_size=500 IndexErrors on a small
table, but roughly a quarter of the total guide count lets it complete.
"""
import subprocess, sys

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data\synthetic_small200_counts.txt"
WORK = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"

with open(DATA) as f:
    n_guides = sum(1 for _ in f) - 1
print("total guides in small table:", n_guides)

# Default half_window_size (500) -- expect IndexError per the fix log
r1 = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", f"{WORK}\\input5_default_hws.txt",
                      "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3", "-p", "5"],
                     capture_output=True, text=True)
print("=== default half_window_size (500) ===")
print("returncode:", r1.returncode)
print("last stderr line:", r1.stderr.strip().splitlines()[-1] if r1.stderr.strip() else "(none)")

# ~1/4 of guide count, per SKILL.md guidance
hws_quarter = max(1, n_guides // 4)
r2 = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", f"{WORK}\\input5_quarter_hws.txt",
                      "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3",
                      "-p", "5", "--half_window_size", str(hws_quarter)],
                     capture_output=True, text=True)
print(f"\n=== half_window_size={hws_quarter} (~1/4 of {n_guides} guides) ===")
print("returncode:", r2.returncode)
if r2.returncode == 0:
    import pandas as pd
    df = pd.read_csv(f"{WORK}\\input5_quarter_hws.txt", sep="\t")
    print("gene rows in output:", len(df), "NaN in normZ:", df['normZ'].isna().sum())
else:
    print("last stderr line:", r2.stderr.strip().splitlines()[-1] if r2.stderr.strip() else "(none)")
