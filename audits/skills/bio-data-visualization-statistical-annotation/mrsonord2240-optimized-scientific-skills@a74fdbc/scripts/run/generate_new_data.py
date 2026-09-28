"""Generate deterministic synthetic fixtures for the two new re-audit inputs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20260927)

# New input 8: unequal sample sizes and deliberately unequal variances.  The
# scientific request calls for Welch's test rather than Student's t-test.
welch = pd.DataFrame(
    {
        "group": ["Reference"] * 22 + ["Treatment"] * 31,
        "value": np.concatenate(
            [
                rng.normal(loc=0.0, scale=0.65, size=22),
                rng.normal(loc=0.95, scale=2.20, size=31),
            ]
        ),
    }
)
welch.to_csv(DATA / "welch_unequal_variance.csv", index=False)

# New input 9: the same biological subject is incorrectly assigned to both
# groups.  A safe nested-data workflow must reject this before model fitting.
rows: list[dict[str, object]] = []
for group, subjects, offset in (
    ("Control", ["C1", "C2", "shared"], 0.0),
    ("Treatment", ["T1", "T2", "shared"], 0.4),
):
    for subject_index, subject in enumerate(subjects):
        for replicate in range(6):
            rows.append(
                {
                    "group": group,
                    "subject_id": subject,
                    "value": offset + subject_index * 0.2 + replicate * 0.03,
                }
            )
invalid_nested = pd.DataFrame(rows)
invalid_nested.to_csv(DATA / "nested_cross_group_subject.csv", index=False)

print(f"wrote {len(welch)} rows to {DATA / 'welch_unequal_variance.csv'}")
print(f"wrote {len(invalid_nested)} rows to {DATA / 'nested_cross_group_subject.csv'}")
