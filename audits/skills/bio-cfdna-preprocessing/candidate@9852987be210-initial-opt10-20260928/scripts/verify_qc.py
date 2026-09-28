#!/usr/bin/env python3
"""Independent insert-size arithmetic for the initial audit (does not import candidate code)."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import statistics

import pysam

RUN = Path(__file__).resolve().parent
TOOLING = Path("/mnt/openscience/audit-envs/bio-cfdna-preprocessing")


def summarize(path: Path, max_size: int = 600) -> dict:
    values = []
    flags = {"secondary": 0, "supplementary": 0, "duplicate": 0, "qc_fail": 0}
    with pysam.AlignmentFile(path, "rb") as bam:
        for read in bam.fetch():
            if read.is_proper_pair and not read.is_secondary and 0 < read.template_length <= max_size:
                values.append(read.template_length)
                flags["secondary"] += int(read.is_secondary)
                flags["supplementary"] += int(read.is_supplementary)
                flags["duplicate"] += int(read.is_duplicate)
                flags["qc_fail"] += int(read.is_qcfail)
    if not values:
        metrics = {"n": 0, "mode_bp": 0, "median_bp": 0.0, "short_frac_90_150": 0.0, "frac_over_250bp": 0.0}
    else:
        counts = Counter(values)
        mode = min(value for value, count in counts.items() if count == max(counts.values()))
        metrics = {
            "n": len(values),
            "mode_bp": mode,
            "median_bp": float(statistics.median(values)),
            "short_frac_90_150": sum(90 <= value <= 150 for value in values) / len(values),
            "frac_over_250bp": sum(value > 250 for value in values) / len(values),
        }
    return {"metrics": metrics, "included_flags": flags}


def main() -> None:
    result = {
        "public": summarize(TOOLING / "data" / "nf-core-human" / "test.paired_end.sorted.bam"),
        "flag_fixture": summarize(TOOLING / "data" / "synthetic-umi" / "flag-qc.bam"),
    }
    output = RUN / "evidence" / "independent-qc.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
