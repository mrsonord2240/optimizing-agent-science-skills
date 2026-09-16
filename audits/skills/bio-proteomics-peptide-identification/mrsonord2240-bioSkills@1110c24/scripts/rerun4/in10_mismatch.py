"""Input 10 (adversarial, NEW): decoy-tag mismatch through the whole CLI route.

Comet run with decoy_prefix = rev_ against a database whose decoys are DECOY_.
Checks each stage of the Skill's documented route for a SILENT wrong answer.
"""
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


def load_comet_txt(path):
    df = pd.read_csv(path, sep="\t", skiprows=1)
    df = df.rename(columns={"e-value": "evalue"})
    df["score"] = -np.log10(df["evalue"].clip(lower=1e-300))
    return df


for tag, path in (("decoy_prefix = DECOY_ (correct)", rf"{W}\comet_out\comet.txt"),
                  ("decoy_prefix = rev_ (MISMATCHED)", rf"{W}\in10_mismatch\comet.txt")):
    df = load_comet_txt(path)
    n_dec = int(df["protein"].str.startswith("DECOY_").sum())
    print(f"\n{tag}: rows {len(df)}, rows whose protein starts DECOY_ {n_dec}")
    try:
        kept, all_ = run_snippet(df)
        print(f"  SKILL table snippet: decoys detected {int(all_['is_decoy'].sum())} "
              f"| kept at q<=0.01 {len(kept)}")
    except ValueError as e:
        print(f"  SKILL table snippet raised ValueError: {e}")
