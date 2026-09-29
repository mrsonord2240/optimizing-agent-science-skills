#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import csv
import json
import sys
from pathlib import Path


def inventory(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


a, b = map(Path, sys.argv[1:3])
left, right = inventory(a), inventory(b)
assert len(left) == len(right) == 25, (len(left), len(right))
assert left.keys() == right.keys()
raw_results = []
same_nonstdout = True
stdout_checks = []
for rel in sorted(left):
    x, y = left[rel], right[rel]
    if rel.endswith("hyb.stdout.log"):
        xa, ya = x.read_text(encoding="utf-8").splitlines(), y.read_text(encoding="utf-8").splitlines()
        okay = len(xa) == len(ya) and xa[0].startswith("hyb: ") and ya[0].startswith("hyb: ") and xa[1:] == ya[1:]
        stdout_checks.append({"path": rel, "same_after_first_timestamp_line": okay, "first_line_differs": xa[0] != ya[0]})
    else:
        okay = x.read_bytes() == y.read_bytes()
        same_nonstdout &= okay
        if rel.startswith("raw/") and rel.endswith("_hybrids_ua.hyb"):
            rows = x.read_text(encoding="utf-8").splitlines()
            raw_results.append({"path": rel, "rows": len(rows), "field_counts": sorted({len(row.split("\t")) for row in rows}), "sha256": sha(x)})
assert same_nonstdout
assert len(stdout_checks) == 2 and all(x["same_after_first_timestamp_line"] for x in stdout_checks)
assert all(x["rows"] == 111 and x["field_counts"] == [16] for x in raw_results) and len(raw_results) == 2
structured = ("sites.tsv", "targets.tsv", "support.tsv", "excluded.tsv", "manifest.json")
structured_hashes = {}
for name in structured:
    assert sha(a / name) == sha(b / name), name
    structured_hashes[name] = sha(a / name)
manifests = [json.loads((root / "manifest.json").read_text(encoding="utf-8")) for root in (a, b)]
assert manifests[0] == manifests[1]
assert manifests[0]["accepted_rows"] == 111 and manifests[0]["excluded_rows"] == 0
assert manifests[0]["replicates"] == 2 and manifests[0]["target_rows"] == 111
with (a / "support.tsv").open(encoding="utf-8", newline="") as handle:
    support = list(csv.DictReader(handle, delimiter="\t"))
assert len(support) == 111
assert all(row["runs_supporting_assignment"] == "2" and row["runs_present"] == "2" and row["runs_required"] == "2" and row["supporting_run_indices"] == "1,2" and row["accepted"] == "true" for row in support)
print(json.dumps({
    "workflow_file_count_each": len(left),
    "all_nonstdout_files_byte_identical": same_nonstdout,
    "stdout_logs": stdout_checks,
    "raw_runs": raw_results,
    "raw_run_count_per_workflow": len(raw_results),
    "structured_output_sha256": structured_hashes,
    "manifest_counts": {k: manifests[0][k] for k in ("accepted_rows", "excluded_rows", "replicates", "target_rows")},
    "support_rows": len(support),
    "every_support_row_two_of_two": True,
    "repeatability_pass": True,
}, indent=2, sort_keys=True))
