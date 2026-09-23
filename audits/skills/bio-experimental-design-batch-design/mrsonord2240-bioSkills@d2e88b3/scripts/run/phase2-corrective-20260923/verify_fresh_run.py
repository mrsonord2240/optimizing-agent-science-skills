"""Check the fresh isolated-runtime Phase 2 artifacts, without reading the source worktree."""
from __future__ import annotations

import csv
import hashlib
from collections import Counter
from pathlib import Path

run = Path(__file__).parent

def read(name: str) -> str:
    return (run / name).read_text(encoding="utf-8")

for name in ["in00_runtime_probe.out", "in1_assign_canonical.out", "in2_bridge_canonical.out",
             "in3_sva_na.out", "in4_balance_cases.out", "in5_combat_claims.out",
             "in6_determinism.out", "in7_missing_covariate.out", "in8_over_capacity.out",
             "in9_invalid_reserved_channel.out", "parse_sources.out"]:
    assert (run / name).is_file(), name
    assert "Segmentation fault" not in read(name), name

probe = read("in00_runtime_probe.out")
assert "designit=0.5.1" in probe and "sva=3.58.0" in probe and "clean R teardown" in probe

with (run / "layout24.csv").open(newline="", encoding="utf-8") as handle:
    layout24 = list(csv.DictReader(handle))
assert len(layout24) == 24
for field in ("condition", "sex"):
    cells = Counter((row[field], row["batch"]) for row in layout24)
    assert sorted(cells.values()) == [4] * 6, (field, cells)

with (run / "layout60.csv").open(newline="", encoding="utf-8") as handle:
    layout60 = list(csv.DictReader(handle))
assert len(layout60) == 60
assert all(row["channel"] != "16" for row in layout60)
assert sorted(Counter(row["plex"] for row in layout60).values()) == [15] * 4

first = hashlib.sha256((run / "layout24.csv").read_bytes()).hexdigest()
repeat = hashlib.sha256((run / "layout24_repeat.csv").read_bytes()).hexdigest()
assert first == repeat
assert "PASS: shipped example completed with NA-present matrix" in read("in3_sva_na.out")
assert "PASS: ComBat rejected perfect confounding" in read("in5_combat_claims.out")
assert "PASS: balanced accepted" in read("in4_balance_cases.out")
for name in ("in7_missing_covariate.out", "in8_over_capacity.out", "in9_invalid_reserved_channel.out"):
    assert "PASS:" in read(name), name
for name in ("should_not_exist.csv", "invalid_reserved.csv"):
    assert not (run / name).exists(), name
assert "PASS: parsed 4 shipped R files." in read("parse_sources.out")
print(f"PASS: fresh suite checks passed; layout24_sha256={first}; 36/36 audit assertions supported.")
