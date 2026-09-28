#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sites(root: Path) -> dict[str, tuple[str, ...]]:
    with (root / "sites.tsv").open(encoding="utf-8", newline="") as handle:
        return {row["read_id"]: tuple(row.values()) for row in csv.DictReader(handle, delimiter="\t")}


def load_excluded(root: Path) -> dict[str, str]:
    with (root / "excluded.tsv").open(encoding="utf-8", newline="") as handle:
        return {row["read_id"]: row["reason"] for row in csv.DictReader(handle, delimiter="\t")}


left, right = map(Path, sys.argv[1:3])
left_manifest = json.loads((left / "manifest.json").read_text(encoding="utf-8"))
right_manifest = json.loads((right / "manifest.json").read_text(encoding="utf-8"))
left_sites, right_sites = load_sites(left), load_sites(right)
left_excluded, right_excluded = load_excluded(left), load_excluded(right)
left_ids, right_ids = set(left_sites), set(right_sites)
shared = left_ids & right_ids
changed_shared = sorted(read_id for read_id in shared if left_sites[read_id] != right_sites[read_id])
payload = {
    "pair_a": {
        "accepted": left_manifest["accepted_rows"],
        "excluded": left_manifest["excluded_rows"],
        "reasons": left_manifest["exclusion_reasons"],
        "sites_sha256": sha(left / "sites.tsv"),
        "targets_sha256": sha(left / "targets.tsv"),
    },
    "pair_b": {
        "accepted": right_manifest["accepted_rows"],
        "excluded": right_manifest["excluded_rows"],
        "reasons": right_manifest["exclusion_reasons"],
        "sites_sha256": sha(right / "sites.tsv"),
        "targets_sha256": sha(right / "targets.tsv"),
    },
    "cross_pair": {
        "identical_sites_bytes": (left / "sites.tsv").read_bytes() == (right / "sites.tsv").read_bytes(),
        "identical_targets_bytes": (left / "targets.tsv").read_bytes() == (right / "targets.tsv").read_bytes(),
        "accepted_only_in_a": sorted(left_ids - right_ids),
        "accepted_only_in_b": sorted(right_ids - left_ids),
        "changed_assignments_among_shared": changed_shared,
        "exclusion_reason_changed": sorted(read_id for read_id in set(left_excluded) & set(right_excluded) if left_excluded[read_id] != right_excluded[read_id]),
    },
}
print(json.dumps(payload, indent=2, sort_keys=True))

