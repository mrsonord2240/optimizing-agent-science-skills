#!/usr/bin/env python3
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    "report.json",
    "viewer.md",
    "source-identity.json",
    "finding-ledger.md",
    "scientific-source-notes.md",
    "inputs/test-inputs.md",
    "scripts/run_reaudit2.sh",
    "scripts/hash_core_artifacts.py",
    "validate_report.py",
    "evidence/execution.log",
    "evidence/execution-status.tsv",
    "evidence/schema-validation.json",
    "evidence/candidate-manifest.tsv",
    "evidence/candidate-identity.txt",
    "evidence/environment.tsv",
    "evidence/baalchip-packages-entry.txt",
    "evidence/baalchip-source-binding.tsv",
    "evidence/package-install-probe.log",
    "evidence/baalchip-runtime-boundary.tsv",
    "evidence/wasp-live.tsv",
    "evidence/wasp-hdf5-live.tsv",
    "evidence/rasqual-binary-contract.tsv",
    "evidence/rasqual-cohort.tsv",
    "evidence/interval-live.tsv",
    "evidence/alleleseq-binding.tsv",
    "evidence/alleleseq-boundary.tsv",
]


def main() -> int:
    rows = []
    for relative in PATHS:
        path = ROOT / relative
        raw = path.read_bytes()
        rows.append(f"{relative}\t{len(raw)}\t{sha256(raw).hexdigest()}")
    output = ROOT / "evidence" / "artifact-hashes.tsv"
    output.write_text("path\tbytes\tsha256\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"hashed {len(rows)} core artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
