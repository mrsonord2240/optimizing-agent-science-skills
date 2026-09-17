"""Input 1 - Canonical: standard vehicle vs drug drugZ run, exactly the SKILL.md CLI pattern.
Regression of pre-fix audit Input 1. Checks: all planted sensitizers/suppressors recovered,
no NaN, all documented columns present.
"""
import subprocess, sys, json
import pandas as pd

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data\synthetic_drug_vehicle_counts.txt"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work\input1_output.txt"

cmd = [PY, DRUGZ, "-i", DATA, "-o", OUT,
       "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3", "-p", "5"]
r = subprocess.run(cmd, capture_output=True, text=True)
print("returncode:", r.returncode)
print("stderr tail:", r.stderr[-800:])

df = pd.read_csv(OUT, sep="\t")
print("rows:", len(df), "cols:", list(df.columns))
print("NaN in normZ:", df["normZ"].isna().sum())

sensitizers = "CCDC89,CER1,CFL2,GALNT11,IL18R1,OSTM1".split(",")
suppressors = "FZD1,G6PC2,GTDC1,MAGT1,PLEKHH2,POF1B".split(",")
paradox = "RGS2"

df_sorted_synth = df.sort_values("rank_synth")
df_sorted_supp = df.sort_values("rank_supp")

sens_ranks = {g: int(df.loc[df.GENE == g, "rank_synth"].values[0]) for g in sensitizers}
supp_ranks = {g: int(df.loc[df.GENE == g, "rank_supp"].values[0]) for g in suppressors}
paradox_rank = int(df.loc[df.GENE == paradox, "rank_supp"].values[0])

print("sensitizer rank_synth:", sens_ranks)
print("suppressor rank_supp:", supp_ranks)
print("paradox gene rank_supp:", paradox_rank)
print("max sensitizer rank_synth:", max(sens_ranks.values()), "max suppressor rank_supp:", max(supp_ranks.values()))
