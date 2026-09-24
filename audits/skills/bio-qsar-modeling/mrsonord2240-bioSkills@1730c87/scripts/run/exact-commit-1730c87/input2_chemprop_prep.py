# bio-qsar-modeling -- Input 2 (Variant A) prep: build the chemprop CSV for a
# classification task exactly as SKILL.md's CLI block expects it.
import pandas as pd

D = r"F:\OpenScience\audits\bio-qsar-modeling\run"
df = pd.read_csv(D + r"\herg_unique.csv")
# SKILL.md OECD principle 1: "Defined endpoint: specific bioassay, units, threshold".
# hERG blocker defined as pChEMBL >= 5 (IC50 <= 10 uM), the common screening threshold.
df['hERG_blocker'] = (df.pchembl_value >= 5.0).astype(int)
out = df.rename(columns={'canonical_smiles': 'smiles'})[['smiles', 'hERG_blocker']]
out.to_csv(D + r"\chemprop_herg.csv", index=False)
print(f"rows={len(out)}  positives={int(out.hERG_blocker.sum())} "
      f"({100*out.hERG_blocker.mean():.1f}%)  negatives={int((1-out.hERG_blocker).sum())}")
print(f"class ratio = {(1-out.hERG_blocker).sum()}:{out.hERG_blocker.sum()} "
      f"neg:pos -- the SKILL.md 'Class imbalance not handled' failure mode applies")
print(out.head(3).to_string(index=False))
