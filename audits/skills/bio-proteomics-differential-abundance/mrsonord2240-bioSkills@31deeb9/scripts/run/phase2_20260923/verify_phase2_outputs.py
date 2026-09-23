"""Verify that Phase-2 direct-script output artifacts exist and parse after known R teardown faults."""
import csv
import pathlib
import sys
if len(sys.argv) != 2:
    raise SystemExit("usage: verify_phase2_outputs.py <run-dir>")
run = pathlib.Path(sys.argv[1])
for stem, expected_rows in (("msstats_equal_tested.csv", 290), ("msstats_none_tested.csv", 290)):
    with (run / stem).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    print(f"{stem}: rows={len(rows)} fields={list(rows[0]) if rows else []}")
    assert len(rows) == expected_rows
for stem in ("input9_msqrob2.log", "input12_first.log", "input12_second.log"):
    p = run / stem
    assert p.exists() and p.stat().st_size > 0, stem
print("ALL_DIRECT_OUTPUT_ARTIFACTS_PARSE")
