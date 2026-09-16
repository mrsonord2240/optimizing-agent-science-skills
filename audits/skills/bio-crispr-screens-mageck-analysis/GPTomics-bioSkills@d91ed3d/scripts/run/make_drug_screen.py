import numpy as np
import pandas as pd

rng = np.random.default_rng(101)

# 30 hit genes (synthetic-lethal with drug), 4 sgRNAs each: 2 "good" (efficient) guides, 2 "poor" (inefficient) guides
# 60 neutral genes, 4 sgRNAs each
n_hit, n_neutral = 20, 60
n_ntc = 30
base_mean = 600

rows = []
eff_rows = []
for gi in range(n_hit):
    g = f"HIT{gi}"
    for s in range(4):
        sgid = f"{g}_sg{s}"
        efficient = s < 2  # first two guides are efficient knockouts
        eff_score = rng.uniform(0.85, 1.0) if efficient else rng.uniform(0.05, 0.25)
        eff_rows.append((sgid, eff_score))
        guide_mean = base_mean * rng.uniform(0.8, 1.2)
        veh = [rng.poisson(guide_mean) for _ in range(2)]
        # drug depletion scaled by actual efficacy (poor guides show ~no depletion)
        depletion_mult = 1.0 - 0.85 * eff_score  # efficient guide -> near 0.15x; poor guide -> near 0.96x
        drug = [rng.poisson(max(guide_mean * depletion_mult * rng.uniform(0.9, 1.1), 1)) for _ in range(2)]
        rows.append([sgid, g] + veh + drug)

for gi in range(n_neutral):
    g = f"NEU{gi}"
    for s in range(4):
        sgid = f"{g}_sg{s}"
        eff_rows.append((sgid, rng.uniform(0.4, 0.9)))
        guide_mean = base_mean * rng.uniform(0.8, 1.2)
        veh = [rng.poisson(guide_mean) for _ in range(2)]
        drug = [rng.poisson(max(guide_mean * rng.uniform(0.9, 1.1), 1)) for _ in range(2)]
        rows.append([sgid, g] + veh + drug)

ntc_ids = []
for i in range(n_ntc):
    sgid = f"NTC_{i:04d}"
    eff_rows.append((sgid, 0.5))
    guide_mean = base_mean * rng.uniform(0.8, 1.2)
    veh = [rng.poisson(guide_mean) for _ in range(2)]
    drug = [rng.poisson(max(guide_mean * rng.uniform(0.9, 1.1), 1)) for _ in range(2)]
    rows.append([sgid, "NonTargeting"] + veh + drug)
    ntc_ids.append(sgid)

cols = ["sgRNA", "Gene", "Veh_r1", "Veh_r2", "Drug_r1", "Drug_r2"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("synthetic_drug_screen_counts.txt", sep="\t", index=False)
with open("synthetic_drug_ntcs.txt", "w") as f:
    f.write("\n".join(ntc_ids) + "\n")
eff_df = pd.DataFrame(eff_rows, columns=["sgRNA", "efficiency"])
eff_df.to_csv("synthetic_sgrna_efficiency.txt", sep="\t", index=False)
print(df.shape, "hit genes:", n_hit, "neutral:", n_neutral, "ntcs:", n_ntc)
