"""Input 6 - NEW (not in pre-fix audit): T3 Result Determinism check, and regression of the
fix log's claim that the "Unstable hits across libraries or sub-samples" failure mode was
retitled/corrected to state a rerun on identical input cannot show instability because
drugZ has no seed. Verifies that claim directly: run the same command twice, diff outputs.
"""
import subprocess, sys, filecmp

PY = sys.executable
DRUGZ = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\drugz\drugz.py"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\data\synthetic_drug_vehicle_counts.txt"
WORK = r"F:\OpenScience\audits\bio-crispr-screens-drugz-chemogenomic\run\work"

out_a = f"{WORK}\\input6_rerun_a.txt"
out_b = f"{WORK}\\input6_rerun_b.txt"

for out in (out_a, out_b):
    r = subprocess.run([PY, DRUGZ, "-i", DATA, "-o", out,
                         "-c", "Veh_r1,Veh_r2,Veh_r3", "-x", "Drug_r1,Drug_r2,Drug_r3", "-p", "5"],
                        capture_output=True, text=True)
    print(out, "returncode:", r.returncode)

identical = filecmp.cmp(out_a, out_b, shallow=False)
print("byte-identical reruns:", identical)

import pandas as pd
a = pd.read_csv(out_a, sep="\t")
b = pd.read_csv(out_b, sep="\t")
max_diff = (a.set_index("GENE")["normZ"] - b.set_index("GENE")["normZ"]).abs().max()
print("max |normZ| diff between reruns:", max_diff)
