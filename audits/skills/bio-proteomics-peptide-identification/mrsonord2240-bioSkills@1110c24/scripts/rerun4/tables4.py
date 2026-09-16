"""Run the SKILL.md table-FDR block VERBATIM on every PSM table in this audit.

The block is pulled out of the fork's SKILL.md with extract.py; only the
pd.read_csv line is swapped for an already-loaded frame, so the estimator and
the decoy matching are exactly the Skill's text.
"""
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\peptide-identification\SKILL.md"
DATA = r"F:\OpenScience\audits\bio-proteomics-peptide-identification\data"

SRC = [b for h, l, b in blocks(SK, "python") if h.startswith("FDR from a Results Table")][0]
SEP = [b for h, l, b in blocks(SK, "python") if h.startswith("FDR from SEPARATE")][0]


def run_snippet(df):
    """Execute the Skill's concatenated-competition block on `df`."""
    code = re.sub(r"^psms = pd\.read_csv.*$", "psms = _INPUT.copy()", SRC, flags=re.M)
    ns = {"pd": pd, "_INPUT": df}
    exec(compile(code, "<SKILL.md concatenated block>", "exec"), ns)
    return ns["kept"], ns["psms"]


def fdp(kept, col="is_correct"):
    if col not in kept.columns or len(kept) == 0:
        return float("nan")
    return 1 - kept[col].mean()


def main():
    print("=== Input 2 (regression): Comet concatenated .txt, 5 ranks/scan ===")
    comet = pd.read_csv(f"{DATA}/comet_concat.txt", sep="\t")
    comet2 = comet.rename(columns={"xcorr": "score"})
    kept, all_ = run_snippet(comet2)
    print(f"  rows {len(comet)} | after rank-1 dedup {len(all_)} | kept {len(kept)} "
          f"| unique scans {kept['scan'].nunique()} | true FDP {fdp(kept):.4f}")
    print(f"  XCorr at the 1% cut: {kept['score'].min():.3f}")

    print("=== Input 3 (regression): 33-PSM pulldown ===")
    for f in ("pulldown_nodecoy.tsv", "pulldown_topdecoy.tsv"):
        t = pd.read_csv(f"{DATA}/{f}", sep="\t").rename(columns={"xcorr": "score"})
        try:
            kept, all_ = run_snippet(t)
            print(f"  {f}: rows {len(all_)} decoys {int(all_['is_decoy'].sum())} "
                  f"kept at 1% {len(kept)} | q min {all_['qvalue'].min():.4f} "
                  f"max {all_['qvalue'].max():.4f} | any inf {bool(np.isinf(all_['qvalue']).any())}")
        except ValueError as e:
            print(f"  {f}: ValueError -> {e}")

    print("=== Input 6 (regression of the pass-2 P1): FragPipe lowercase rev_ ===")
    rev = comet2.copy()
    rev["protein"] = rev["protein"].str.replace("DECOY_", "rev_", regex=False)
    kept, all_ = run_snippet(rev)
    print(f"  decoys detected {int(all_['is_decoy'].sum())} | kept {len(kept)} "
          f"| unique scans {kept['scan'].nunique()} | true FDP {fdp(kept):.4f}")
    revlow = comet2.copy()
    revlow["protein"] = revlow["protein"].str.replace("DECOY_", "REV__", regex=False)
    kept2, _ = run_snippet(revlow)
    print(f"  MaxQuant REV__ : kept {len(kept2)} | true FDP {fdp(kept2):.4f}")

    print("=== NEW: decoy-free table must raise, not pass everything ===")
    nod = comet2[~comet2["protein"].str.startswith("DECOY_")].copy()
    try:
        kept, _ = run_snippet(nod)
        print(f"  NO ERROR -- kept {len(kept)} (true FDP {fdp(kept):.4f})  <-- silent failure")
    except ValueError as e:
        print(f"  ValueError raised: {e}")

    print("=== Input 7 (regression): lower-is-better E-value as `score` ===")
    ev = comet.rename(columns={"e-value": "score"})
    if "score" not in ev.columns:
        cand = [c for c in comet.columns if "value" in c.lower()]
        ev = comet.rename(columns={cand[0]: "score"})
    kept, _ = run_snippet(ev)
    print(f"  raw E-value as score: kept {len(kept)} | true FDP {fdp(kept):.4f}")
    ev2 = ev.copy()
    ev2["score"] = -np.log10(ev2["score"].clip(lower=1e-300))
    kept, _ = run_snippet(ev2)
    print(f"  -log10(E-value)     : kept {len(kept)} | true FDP {fdp(kept):.4f}")

    print("=== Input 5 (regression): separate searches, SKILL.md block verbatim ===")
    ns = {"np": np, "pd": pd}
    exec(compile(SEP, "<SKILL.md separate block>", "exec"), ns)
    tgt = pd.read_csv(f"{DATA}/separate_target.tsv", sep="\t")
    dec = pd.read_csv(f"{DATA}/separate_decoy.tsv", sep="\t")
    for pi0 in (None, 1.0):
        t, used = ns["separate_search_qvalues"](tgt, dec, pi0=pi0)
        k = t[t["qvalue"] <= 0.01]
        print(f"  pi0={'hat' if pi0 is None else pi0}: pi0-used {used:.3f} kept {len(k)} "
              f"true FDP {fdp(k):.4f}")
    merged = pd.concat([tgt, dec]).rename(columns={"xcorr": "score"})
    kept, _ = run_snippet(merged)
    print(f"  concatenated snippet misapplied to the merged pair: kept {len(kept)} "
          f"true FDP {fdp(kept):.4f}")


if __name__ == "__main__":
    main()
