"""Inspect the first Pwalign PID4 mismatch in Phase 2's audit reconstruction."""
import csv
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN / "skill" / "examples"))
from identity_matrix import pairwise_identity

with (RUN.parent / "data" / "derived" / "pid_pairs_R.tsv").open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        p_prefix, s_prefix = row["pfull"][:int(row["ps"]) - 1], row["sfull"][:int(row["ss"]) - 1]
        p_suffix, s_suffix = row["pfull"][int(row["pe"]):], row["sfull"][int(row["se"]):]
        a = p_prefix + "-" * len(s_prefix) + row["a"] + p_suffix + "-" * len(s_suffix)
        b = "-" * len(p_prefix) + s_prefix + row["b"] + "-" * len(p_suffix) + s_suffix
        expected = float(row["PID4"])
        actual = pairwise_identity(a, b, "pid4") * 100
        if abs(expected - actual) >= 0.011:
            print(row["name"], "expected", expected, "actual", actual)
            print("ranges", row["ps"], row["pe"], row["ss"], row["se"])
            print("lengths full/aligned/rebuilt", len(row["pfull"]), len(row["sfull"]), len(row["a"]), len(row["b"]), len(a), len(b))
            print("ungapped rebuilt", len(a.replace("-", "")), len(b.replace("-", "")))
            break
