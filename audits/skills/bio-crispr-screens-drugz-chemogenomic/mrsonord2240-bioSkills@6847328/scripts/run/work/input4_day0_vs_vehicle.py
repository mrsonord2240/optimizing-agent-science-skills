"""Input 4 - Edge: the documented Day-0-vs-Drug failure mode. Regression of pre-fix Input 4.
Runs drugZ with T0 as control instead of vehicle, on the same drug arm as Input 1, and
compares how many planted sensitizers are recovered / how much proliferation noise appears.
"""
import subprocess, sys
import pandas as pd

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data\synthetic_drug_vehicle_counts.txt"
WORK = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"
OUT = f"{WORK}\\input4_day0.txt"

r = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", OUT,
                     "-c", "T0", "-x", "Drug_r1,Drug_r2,Drug_r3", "-unpaired", "-p", "5"],
                    capture_output=True, text=True)
print("returncode:", r.returncode)
print(r.stderr[-400:])

std = pd.read_csv(f"{WORK}\\input1_output.txt", sep="\t")
day0 = pd.read_csv(OUT, sep="\t")

sensitizers = "CCDC89,CER1,CFL2,GALNT11,IL18R1,OSTM1".split(",")
std_ranks = {g: int(std.loc[std.GENE == g, "rank_synth"].values[0]) for g in sensitizers}
day0_ranks = {g: int(day0.loc[day0.GENE == g, "rank_synth"].values[0]) for g in sensitizers}
day0_fdr = {g: float(day0.loc[day0.GENE == g, "fdr_synth"].values[0]) for g in sensitizers}

print("Vehicle-vs-Drug rank_synth:", std_ranks)
print("Day0-vs-Drug rank_synth:", day0_ranks)
print("Day0-vs-Drug fdr_synth:", day0_fdr)

n_spurious_std = int((std["fdr_synth"] < 0.05).sum())
n_spurious_day0 = int((day0["fdr_synth"] < 0.05).sum())
print("genes with fdr_synth<0.05 under Vehicle-vs-Drug:", n_spurious_std)
print("genes with fdr_synth<0.05 under Day0-vs-Drug:", n_spurious_day0)
