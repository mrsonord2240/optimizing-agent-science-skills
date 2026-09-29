#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
SCRIPT = CANDIDATE / "scripts/extract_targeted_umi.py"


def write_fastq(path: Path, sequence: str) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as text:
                text.write(f"@read1 description\n{sequence}\n+\n{'I' * len(sequence)}\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


with tempfile.TemporaryDirectory(prefix="ago-umi-reaudit2-") as temp:
    root = Path(temp)
    r1, r2 = root / "R1.fastq.gz", root / "R2.fastq.gz"
    write_fastq(r1, "AACCGGTT")
    write_fastq(r2, "ACGTACGTACGG")
    common = [sys.executable, str(SCRIPT), "--read1", str(r1), "--read2", str(r2)]
    success = []
    for length, expected in ((9, "ACGTACGTA"), (10, "ACGTACGTAC")):
        output, manifest = root / f"umi-{length}.fastq", root / f"umi-{length}.json"
        p = subprocess.run(common + ["--output-fastq", str(output), "--manifest", str(manifest), "--umi-length", str(length), "--library-id", f"audit2-{length}", "--protocol-source", f"fixture-protocol-{length}nt"], text=True, capture_output=True)
        assert p.returncode == 0, p.stderr
        header = output.read_text(encoding="utf-8").splitlines()[0]
        doc = json.loads(manifest.read_text(encoding="utf-8"))
        assert header.startswith(f"@read1_{expected} ")
        assert doc["declared_umi_length"] == length and doc["library_id"] == f"audit2-{length}"
        assert doc["protocol_source"] == f"fixture-protocol-{length}nt"
        success.append({"length": length, "expected_umi": expected, "header": header, "output_sha256": sha(output), "manifest_sha256": sha(manifest)})

    failure_cases = (
        ("missing-length", ["--library-id", "audit2", "--protocol-source", "protocol"], "--umi-length"),
        ("zero-length", ["--umi-length", "0", "--library-id", "audit2", "--protocol-source", "protocol"], "between 1 and 64"),
        ("noninteger-length", ["--umi-length", "nine", "--library-id", "audit2", "--protocol-source", "protocol"], "invalid int value"),
        ("blank-library", ["--umi-length", "9", "--library-id", "   ", "--protocol-source", "protocol"], "must be non-empty"),
        ("blank-protocol", ["--umi-length", "9", "--library-id", "audit2", "--protocol-source", "   "], "must be non-empty"),
        ("short-r2", ["--umi-length", "13", "--library-id", "audit2", "--protocol-source", "protocol"], "shorter than declared UMI length 13"),
    )
    failures = []
    for name, opts, diagnostic in failure_cases:
        output, manifest = root / f"{name}.fastq", root / f"{name}.json"
        p = subprocess.run(common + ["--output-fastq", str(output), "--manifest", str(manifest)] + opts, text=True, capture_output=True)
        assert p.returncode != 0 and diagnostic in p.stderr and not output.exists() and not manifest.exists(), (name, p.returncode, p.stderr)
        failures.append({"case": name, "returncode": p.returncode, "diagnostic": diagnostic, "outputs_absent": True})
    print(json.dumps({"successes": success, "failures": failures, "assertions_passed": 8, "fail_closed": True}, indent=2, sort_keys=True))
