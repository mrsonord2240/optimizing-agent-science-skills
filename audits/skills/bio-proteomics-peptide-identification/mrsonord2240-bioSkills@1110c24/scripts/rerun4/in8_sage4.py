"""Input 8 regression + new Input 10: SKILL.md table block on real Sage output,
and the Percolator 1% list vs Sage's own, on PXD070049 Condition A REP1."""
import re
import sys

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


sage = pd.read_csv(rf"{W}\sage_out\sage\results.sage.tsv", sep="\t")
print("Sage rows", len(sage), "| label counts", sage["label"].value_counts().to_dict())
own = sage[(sage["label"] == 1) & (sage["spectrum_q"] <= 0.01)]
print("Sage's own spectrum_q <= 0.01 target PSMs:", len(own))

mapped = sage.rename(columns={"scannr": "scan", "sage_discriminant_score": "score",
                              "proteins": "protein"})
kept, all_ = run_snippet(mapped)
print(f"SKILL snippet: decoys detected {int(all_['is_decoy'].sum())} | kept {len(kept)}")
print("  scan-set identical to Sage's own list:",
      set(kept["scan"]) == set(own["scannr"]))


def species(protein_series):
    out = {}
    for p in protein_series:
        first = str(p).split(";")[0]
        key = "HUMAN" if "_HUMAN" in first else "YEAST" if "_YEAST" in first \
            else "ECOLI" if "_ECOLI" in first else "other"
        out[key] = out.get(key, 0) + 1
    return out


print("  species of the kept list:", species(kept["protein"]))

# Percolator output from examples/dda_search.sh
def read_perc(path):
    """Percolator's results file has a ragged trailing proteinIds column."""
    rows = [ln.rstrip("\n").split("\t") for ln in open(path, encoding="utf-8")]
    hdr, n = rows[0], len(rows[0])
    body = [r[: n - 1] + [";".join(r[n - 1:])] for r in rows[1:]]
    return pd.DataFrame(body, columns=hdr).astype({"q-value": float})


perc = read_perc(rf"{W}\sage_out\psms.target.tsv")
print("\nPercolator psms.target.tsv columns:", list(perc.columns)[:6])
p1 = perc[perc["q-value"] <= 0.01]
print(f"Percolator PSMs at q <= 0.01: {len(p1)}")
pep = read_perc(rf"{W}\sage_out\peptides.target.tsv")
print(f"Percolator peptides at q <= 0.01: {int((pep['q-value'] <= 0.01).sum())}")
print("  any decoy left in psms.target.tsv (rev_ in proteinIds):",
      bool(perc.iloc[:, -1].astype(str).str.contains("rev_").any()))
qcol = list(perc.columns).index("q-value") + 1
print(f"  q-value column index in the Sage-pin results: {qcol} (the Skill warns it moves)")

comet_perc = read_perc(rf"{W}\comet_out\psms.target.tsv")
qcol_c = list(comet_perc.columns).index("q-value") + 1
print(f"  q-value column index in the Comet-pin results: {qcol_c}")
print(f"  Comet+Percolator PSMs at q <= 0.01: {int((comet_perc['q-value'] <= 0.01).sum())}")
print("  -> the Skill's 'locate by name' warning is real: index differs "
      f"({qcol} vs {qcol_c})")
