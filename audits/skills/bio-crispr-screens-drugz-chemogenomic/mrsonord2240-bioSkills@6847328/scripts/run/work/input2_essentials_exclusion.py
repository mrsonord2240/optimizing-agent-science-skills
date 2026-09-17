"""Input 2 - Variant A: the P0 regression test.
Runs the OLD (pre-fix) broken -r construction (raw tab-separated CEGv2 lines joined with
commas) and the NEW (fixed) SKILL.md-documented construction (parse col 1, skip header),
against the same counts file, and checks how many genes are actually excluded from each.
"""
import subprocess, sys
import pandas as pd

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data\synthetic_drug_vehicle_counts.txt"
WORK = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"
CEG = r"F:\OpenScience\wt\_fixdata\drugz\CEGv2.txt"  # cached real CEGv2.txt from the fix session

with open(CEG) as f:
    lines = f.read().splitlines()
print("CEGv2.txt header:", lines[0])
print("CEGv2.txt total lines (incl header):", len(lines))

# --- OLD (pre-fix) construction: join raw lines with commas ---
old_list = lines  # examples/run_drugz.py (pre-fix) did: ','.join(open(ceg_file).read().splitlines())
old_arg = ",".join(old_list)
old_out = f"{WORK}\\input2_old_broken.txt"
r = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", old_out,
                     "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3",
                     "-r", old_arg, "-p", "5"], capture_output=True, text=True)
print("OLD run returncode:", r.returncode)

# --- NEW (fixed) construction: parse column 1, skip header ---
new_genes = [ln.split("\t")[0].strip() for ln in lines[1:] if ln.strip()]
new_arg = ",".join(new_genes)
new_out = f"{WORK}\\input2_new_fixed.txt"
r2 = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", new_out,
                      "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3",
                      "-r", new_arg, "-p", "5"], capture_output=True, text=True)
print("NEW run returncode:", r2.returncode)
print("Number of genes in CEGv2 gene list (new parsing):", len(new_genes))

std = pd.read_csv(f"{WORK}\\input1_output.txt", sep="\t")
old_df = pd.read_csv(old_out, sep="\t")
new_df = pd.read_csv(new_out, sep="\t")

genes_std = set(std.GENE)
genes_old = set(old_df.GENE)
genes_new = set(new_df.GENE)

removed_old = genes_std - genes_old
removed_new = genes_std - genes_new

print("Genes removed by OLD (broken) -r construction:", len(removed_old), "of", len(new_genes), "listed")
print("Genes removed by NEW (fixed) -r construction:", len(removed_new), "of", len(new_genes), "listed")

# byte-for-byte identity check for the OLD run vs the unfiltered standard run
import numpy as np
merged = std.merge(old_df, on="GENE", suffixes=("_std", "_old"))
max_diff_old = (merged["normZ_std"] - merged["normZ_old"]).abs().max()
print("max |normZ diff| std vs OLD -r run:", max_diff_old)

merged2 = std.merge(new_df, on="GENE", how="left", suffixes=("_std", "_new"))
still_present_targets = [g for g in new_genes if g in genes_new]
print("Of the excluded-gene list, still present in NEW output:", len(still_present_targets), "(sample:", still_present_targets[:5], ")")
