#!/usr/bin/env python3
"""Hash the explicit public re-audit artifact set."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    "report.json",
    "viewer.md",
    "source-identity.json",
    "inputs.json",
    "finding-ledger.md",
    "scripts/capture_identity.py",
    "scripts/reaudit_cases.py",
    "scripts/validate_report.py",
    "scripts/hash_artifacts.py",
    "evidence/reaudit-results.json",
    "evidence/schema-validation.json",
    "evidence/assertions.json",
    "evidence/commands.log",
    "evidence/static-evaluation.md",
    "evidence/structural-precheck.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


payload = {
    "candidate_content_sha256": "f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd",
    "artifacts": [
        {"path": relative, "bytes": (ROOT / relative).stat().st_size, "sha256": sha256(ROOT / relative)}
        for relative in PATHS
    ],
}
(ROOT / "evidence" / "artifact-hashes.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"artifacts": len(PATHS), "candidate_content_sha256": payload["candidate_content_sha256"]}, sort_keys=True))
