#!/usr/bin/env python3
"""Build deterministic candidate-manifest and audit artifact hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = Path(
    r"F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification"
)
ARTIFACTS = [
    "report.json",
    "viewer.md",
    "source-identity.json",
    "inputs.json",
    "execution-classifications.json",
    "finding-ledger.md",
    "scientific-source-notes.md",
    "scripts/run_reaudit.py",
    "scripts/run_isolated.sh",
    "scripts/build_artifact_hashes.py",
    "scripts/validate_report.py",
    "evidence/execution.json",
    "evidence/candidate-manifest.json",
    "evidence/unit-tests.log",
    "evidence/standalone-demo.log",
    "evidence/live-interface-smoke.log",
    "evidence/reaudit.log",
    "evidence/preflight.log",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_candidate_manifest() -> dict[str, object]:
    rows = []
    files = []
    for path in sorted(
        (item for item in CANDIDATE.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(CANDIDATE).as_posix(),
    ):
        relative = path.relative_to(CANDIDATE).as_posix()
        digest = sha256(path)
        size = path.stat().st_size
        rows.append(f"{relative}\t{size}\t{digest}")
        files.append({"path": relative, "bytes": size, "sha256": digest})
    manifest = "\n".join(rows).encode("utf-8")
    return {
        "schema": "sha256-manifest-v1",
        "identity": hashlib.sha256(manifest).hexdigest(),
        "manifest_bytes": len(manifest),
        "file_count": len(files),
        "files": files,
    }


def main() -> int:
    candidate_manifest = build_candidate_manifest()
    (ROOT / "evidence" / "candidate-manifest.json").write_text(
        json.dumps(candidate_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    records = []
    for relative in ARTIFACTS:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        records.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    (ROOT / "artifact-hashes.json").write_text(
        json.dumps(records, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "candidate_identity": candidate_manifest["identity"],
        "artifact_count": len(records),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
