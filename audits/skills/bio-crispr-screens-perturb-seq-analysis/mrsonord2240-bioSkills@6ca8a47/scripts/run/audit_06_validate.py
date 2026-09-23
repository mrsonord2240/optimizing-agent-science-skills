"""Validate that the shipped multiome CLI ranked every planted peak first."""
from pathlib import Path
import pandas as pd

path = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data\multiome_peaks.tsv")
out = pd.read_csv(path, sep="\t").sort_values("pvals_adj")
top5 = set(out.head(5)["names"])
planted = {f"peak_{i}" for i in range(5)}
assert top5 == planted, (top5, planted)
print(f"planted_top5={len(top5 & planted)}/5")
print("top5=" + ",".join(out.head(5)["names"]))
