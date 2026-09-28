#!/usr/bin/env python3
"""Probe the documented unsorted Path.glob traversal on the WSL ext4 filesystem."""

import json
import tempfile
from pathlib import Path


with tempfile.TemporaryDirectory(prefix="batch-glob-", dir="/tmp") as root_name:
    root = Path(root_name)
    left = root / "left"
    right = root / "right"
    left.mkdir()
    right.mkdir()
    names = [f"sample_{i:03d}.fasta" for i in range(200)]
    for name in reversed(names):
        (left / name).write_text(f">{name}\nACGT\n", encoding="ascii")
    for name in names:
        (right / name).write_text(f">{name}\nACGT\n", encoding="ascii")
    left_order = [path.name for path in left.glob("*.fasta")]
    right_order = [path.name for path in right.glob("*.fasta")]
    print(
        json.dumps(
            {
                "filesystem": "/tmp (WSL ext4)",
                "logical_filename_sets_equal": set(left_order) == set(right_order),
                "orders_equal": left_order == right_order,
                "left_is_sorted": left_order == sorted(left_order),
                "right_is_sorted": right_order == sorted(right_order),
                "left_first_12": left_order[:12],
                "right_first_12": right_order[:12],
            },
            indent=2,
        )
    )
