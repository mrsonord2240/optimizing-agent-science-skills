"""Check the SKILL.md MS-GF+ command block's claimed yield (656 at 1% FDR) by
feeding its own MzIDToTsv output to the Skill's table snippet."""
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\peptide-identification\SKILL.md"
W = r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4"
SRC = [b for h, l, b in blocks(SK, "python") if h.startswith("FDR from a Results Table")][0]


def run_snippet(df):
    code = re.sub(r"^psms = pd\.read_csv.*$", "psms = _INPUT.copy()", SRC, flags=re.M)
    ns = {"pd": pd, "_INPUT": df}
    exec(compile(code, "<SKILL.md concatenated block>", "exec"), ns)
    return ns["kept"], ns["psms"]


df = pd.read_csv(rf"{W}\in10b_msgf\sample.tsv", sep="\t")
print("columns:", [c for c in df.columns][:12])
df = df.rename(columns={"ScanNum": "scan", "Protein": "protein"})
print(f"rows {len(df)} | scans {df['scan'].nunique()} | "
      f"DECOY_ rows {int(df['protein'].str.startswith('DECOY_').sum())}")

df["score"] = -np.log10(df["SpecEValue"].clip(lower=1e-300))
kept, all_ = run_snippet(df)
print(f"-log10(SpecEValue) as score: decoys {int(all_['is_decoy'].sum())} "
      f"| kept at q<=0.01 {len(kept)}")

raw = df.copy()
raw["score"] = raw["SpecEValue"]
kept_raw, _ = run_snippet(raw)
print(f"raw SpecEValue as score    : kept at q<=0.01 {len(kept_raw)} "
      "(the Common Errors row's prediction)")
