#!/usr/bin/env python3
"""Bounded behavioral audit for the exact bio-batch-processing candidate."""

from __future__ import annotations

import csv
import gzip
import importlib.util
import json
import os
import resource
import shutil
import subprocess
import tempfile
from pathlib import Path

import pyfastx
import pysam
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


AUDIT = Path("/mnt/openscience/audits/bio-batch-processing/initial-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-batch-processing/skills/bio-batch-processing")
ENV_ROOT = Path("/mnt/openscience/audit-envs/bio-batch-processing")
PUBLIC = ENV_ROOT / "data" / "public"
PYTHON = ENV_ROOT / "conda-env" / "bin" / "python"
EVIDENCE = AUDIT / "evidence"
INPUTS = AUDIT / "inputs"


def load_candidate_module():
    path = CANDIDATE / "scripts" / "batch_process.py"
    spec = importlib.util.spec_from_file_location("candidate_batch_process", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_small_fastas(directory: Path, records: list[SeqRecord]) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, batch in enumerate((records[:3], records[3:6]), start=1):
        path = directory / f"part_{index}.fasta"
        SeqIO.write(batch, path, "fasta")
        paths.append(path)
    return paths


def exact_summary_recipe(data_dir: Path, output: Path) -> None:
    summaries = []
    for fasta_file in data_dir.glob("*.fasta"):
        count = total = 0
        min_len = None
        max_len = 0
        for record in SeqIO.parse(fasta_file, "fasta"):
            length = len(record.seq)
            count += 1
            total += length
            max_len = max(max_len, length)
            min_len = length if min_len is None else min(min_len, length)
        summaries.append(
            {
                "file": fasta_file.name,
                "sequences": count,
                "total_bp": total,
                "min_len": min_len or 0,
                "max_len": max_len,
                "avg_len": total / count if count else 0,
            }
        )
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summaries[0].keys())
        writer.writeheader()
        writer.writerows(summaries)


def exact_prefix_recipe(input_fasta: Path, cwd: Path) -> dict[str, object]:
    prior_cwd = Path.cwd()
    handles = {}
    before_fds = len(list(Path("/proc/self/fd").iterdir()))
    error = None
    try:
        os.chdir(cwd)
        try:
            for record in SeqIO.parse(input_fasta, "fasta"):
                prefix = record.id.split("_")[0]
                if prefix not in handles:
                    handles[prefix] = open(f"{prefix}.fasta", "w")
                SeqIO.write(record, handles[prefix], "fasta")
        except OSError as exc:
            error = {"type": type(exc).__name__, "message": str(exc)}
        open_fds = len(list(Path("/proc/self/fd").iterdir()))
        return {
            "prefixes": len(handles),
            "fd_before": before_fds,
            "fd_while_open": open_fds,
            "fd_delta": open_fds - before_fds,
            "error": error,
        }
    finally:
        for handle in handles.values():
            handle.close()
        os.chdir(prior_cwd)


def discovered_ids(directory: Path) -> list[str]:
    return [
        record.id
        for filepath in directory.glob("*.fasta")
        for record in SeqIO.parse(filepath, "fasta")
    ]


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    candidate = load_candidate_module()
    source_records = list(SeqIO.parse(PUBLIC / "ls_orchid.fasta", "fasta"))
    results: dict[str, object] = {
        "environment": {
            "python": subprocess.check_output([PYTHON, "--version"], text=True).strip(),
            "wsl_interop": os.environ.get("WSL_INTEROP", "unset"),
            "nofile_soft": resource.getrlimit(resource.RLIMIT_NOFILE)[0],
            "nofile_hard": resource.getrlimit(resource.RLIMIT_NOFILE)[1],
        },
        "cases": {},
    }
    cases: dict[str, object] = results["cases"]  # type: ignore[assignment]
    assertions: dict[str, list[dict[str, object]]] = {}

    with tempfile.TemporaryDirectory(prefix="audit-", dir=AUDIT) as tmp_name:
        tmp = Path(tmp_name)

        # Case 1: shipped standalone script plus imported public functions.
        canonical = tmp / "canonical"
        canonical.mkdir()
        files = candidate.make_demo_fastas(canonical, n_files=3, seqs_per_file=5)
        counts = [candidate.count_streaming(path, "fasta") for path in files]
        chunks = candidate.split_by_count(
            files[0], "fasta", 2, str(canonical / "chunk")
        )
        chunk_counts = [
            sum(1 for _ in SeqIO.parse(path, "fasta")) for path in chunks
        ]
        index_path = canonical / "combined.idx"
        indexed = SeqIO.index_db(index_path, files, "fasta")
        lookup_len = len(indexed["s2_3"].seq)
        indexed.close()
        reopened = SeqIO.index_db(index_path)
        reopen_count = len(reopened)
        reopen_lookup_len = len(reopened["s2_3"].seq)
        reopened.close()
        direct = subprocess.run(
            [PYTHON, CANDIDATE / "scripts" / "batch_process.py"],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        cases["1"] = {
            "status": "COMPLETED",
            "counts": counts,
            "chunk_counts": chunk_counts,
            "index_records_after_reopen": reopen_count,
            "lookup_length": lookup_len,
            "lookup_length_after_reopen": reopen_lookup_len,
            "direct_exit": direct.returncode,
            "direct_stdout": direct.stdout.strip().splitlines(),
            "direct_stderr": direct.stderr.strip(),
        }
        assertions["1"] = [
            {"text": "Streaming counts preserve all records.", "pass": counts == [5, 5, 5]},
            {"text": "Split chunks are bounded and lossless.", "pass": chunk_counts == [2, 2, 1]},
            {"text": "Persistent index reopens with stable lookup values.", "pass": reopen_count == 15 and lookup_len == reopen_lookup_len == 52},
            {"text": "The shipped standalone demonstration exits successfully.", "pass": direct.returncode == 0 and not direct.stderr},
        ]

        # Case 2: advertised pyfastx gzip index plus the documented quality caveat.
        readers = tmp / "readers"
        readers.mkdir()
        fasta_gz = readers / "orchids.fasta.gz"
        with (PUBLIC / "ls_orchid.fasta").open("rb") as src, gzip.open(fasta_gz, "wb") as dst:
            shutil.copyfileobj(src, dst)
        pyfx = pyfastx.Fasta(str(fasta_gz), build_index=True)
        first_sequence_equal = str(pyfx[0].seq) == str(source_records[0].seq)
        legacy = readers / "legacy.fastq"
        legacy.write_text("@legacy\nACGT\n+\nhhhh\n", encoding="ascii")
        with pysam.FastxFile(legacy) as handle:
            pysam_quality = list(next(handle).get_quality_array())
        illumina_record = next(SeqIO.parse(legacy, "fastq-illumina"))
        illumina_quality = list(illumina_record.letter_annotations["phred_quality"])
        cases["2"] = {
            "status": "COMPLETED",
            "pyfastx_records": len(pyfx),
            "pyfastx_index_written": Path(f"{fasta_gz}.fxi").is_file(),
            "pyfastx_first_sequence_equal": first_sequence_equal,
            "pysam_legacy_values": pysam_quality,
            "biopython_phred64_values": illumina_quality,
            "quality_delta": [a - b for a, b in zip(pysam_quality, illumina_quality)],
            "shipped_pyfastx_example": False,
        }
        assertions["2"] = [
            {"text": "pyfastx indexes and randomly accesses gzip FASTA.", "pass": len(pyfx) == 94 and first_sequence_equal},
            {"text": "pyfastx creates its persistent index.", "pass": Path(f"{fasta_gz}.fxi").is_file()},
            {"text": "The pysam Phred+33 caveat is scientifically observable on legacy Phred+64 input.", "pass": pysam_quality == [71] * 4 and illumina_quality == [40] * 4},
            {"text": "The shipped skill provides a runnable pyfastx recipe.", "pass": False},
        ]

        # Case 3: inherited empty-glob and invalid-chunk-size concerns.
        edge = tmp / "edge"
        empty = edge / "empty"
        empty.mkdir(parents=True)
        summary_error = None
        summary_output = edge / "summary.csv"
        try:
            exact_summary_recipe(empty, summary_output)
        except Exception as exc:  # retain the exact public symptom
            summary_error = {"type": type(exc).__name__, "message": str(exc)}
        zero_outputs = candidate.split_by_count(
            PUBLIC / "ls_orchid.fasta", "fasta", 0, str(edge / "zero")
        )
        negative_error = None
        try:
            candidate.split_by_count(
                PUBLIC / "ls_orchid.fasta", "fasta", -1, str(edge / "negative")
            )
        except Exception as exc:
            negative_error = {"type": type(exc).__name__, "message": str(exc)}
        cases["3"] = {
            "status": "ERROR",
            "empty_summary_error": summary_error,
            "empty_summary_output_exists": summary_output.exists(),
            "nonempty_input_records": len(source_records),
            "zero_chunk_outputs": zero_outputs,
            "negative_chunk_error": negative_error,
        }
        assertions["3"] = [
            {"text": "Empty discovery produces a valid header-only CSV or an actionable domain error.", "pass": False},
            {"text": "Zero records_per_file is rejected rather than silently producing no chunks.", "pass": False},
            {"text": "Negative records_per_file is rejected with an actionable skill-level error.", "pass": False},
            {"text": "No input records are silently lost in invalid split requests.", "pass": False},
        ]

        # Case 4: file-descriptor growth and path escape from ID-derived prefixes.
        prefix_case = tmp / "prefix"
        output_dir = prefix_case / "output"
        output_dir.mkdir(parents=True)
        many = prefix_case / "many.fasta"
        high_records = [
            SeqRecord(Seq("ACGT"), id=f"p{i:04d}_record", description="")
            for i in range(2048)
        ]
        SeqIO.write(high_records, many, "fasta")
        high_stats = exact_prefix_recipe(many, output_dir)
        traversal_dir = prefix_case / "traversal-output"
        traversal_dir.mkdir()
        escaped = prefix_case / "escaped.fasta"
        escaped.write_text("sentinel\n", encoding="utf-8")
        hostile = prefix_case / "hostile.fasta"
        SeqIO.write(
            [SeqRecord(Seq("ACGT"), id="../escaped_record", description="")],
            hostile,
            "fasta",
        )
        traversal_stats = exact_prefix_recipe(hostile, traversal_dir)
        escaped_text = escaped.read_text(encoding="utf-8")
        cases["4"] = {
            "status": "ERROR" if high_stats["error"] else "COMPLETED",
            "high_cardinality": high_stats,
            "hostile_prefix": traversal_stats,
            "sibling_overwritten": escaped_text != "sentinel\n",
            "sibling_parse_count": sum(1 for _ in SeqIO.parse(escaped, "fasta")),
            "intended_output_contains_escape": (traversal_dir / "escaped.fasta").exists(),
        }
        assertions["4"] = [
            {"text": "Open handles remain bounded independently of distinct prefix count.", "pass": high_stats["fd_delta"] < 100},
            {"text": "All derived output paths remain inside the intended output directory.", "pass": False},
            {"text": "An existing sibling file cannot be overwritten by a sequence ID.", "pass": escaped_text == "sentinel\n"},
            {"text": "All 2,048 high-cardinality records are written.", "pass": high_stats["prefixes"] == 2048},
        ]

        # Case 5: glob ordering and the exact unguarded Pool recipe under spawn.
        deterministic = tmp / "deterministic"
        left = deterministic / "left"
        right = deterministic / "right"
        left.mkdir(parents=True)
        right.mkdir(parents=True)
        names = [f"file_{i:03d}.fasta" for i in range(50)]
        for index, name in enumerate(reversed(names)):
            SeqIO.write([SeqRecord(Seq("ACGT"), id=f"L{49-index:03d}", description="")], left / name, "fasta")
        for index, name in enumerate(names):
            SeqIO.write([SeqRecord(Seq("ACGT"), id=f"R{index:03d}", description="")], right / name, "fasta")
        left_order = [path.name for path in left.glob("*.fasta")]
        right_order = [path.name for path in right.glob("*.fasta")]
        same_glob_order = left_order == right_order
        spawn_case = tmp / "spawn"
        spawn_data = spawn_case / "data"
        write_small_fastas(spawn_data, source_records)
        try:
            spawn = subprocess.run(
                [PYTHON, INPUTS / "spawn_launcher.py"],
                cwd=spawn_case,
                text=True,
                capture_output=True,
                check=False,
                timeout=15,
            )
            spawn_exit: int | str = spawn.returncode
            spawn_stdout = spawn.stdout.strip()
            spawn_stderr = spawn.stderr.strip()
        except subprocess.TimeoutExpired as exc:
            spawn_exit = "TIMEOUT_15S"
            spawn_stdout = (exc.stdout or "").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            spawn_stderr = (exc.stderr or "").decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        cases["5"] = {
            "status": "ERROR" if spawn_exit != 0 else "COMPLETED",
            "left_glob_first_ten": left_order[:10],
            "right_glob_first_ten": right_order[:10],
            "same_glob_order": same_glob_order,
            "left_sorted": left_order == sorted(left_order),
            "right_sorted": right_order == sorted(right_order),
            "spawn_exit": spawn_exit,
            "spawn_stdout": spawn_stdout,
            "spawn_stderr_excerpt": spawn_stderr[-6000:],
            "spawn_bootstrap_error": "bootstrapping phase" in spawn_stderr,
        }
        assertions["5"] = [
            {"text": "The documented traversal is explicitly sorted and byte-stable for identical filename sets.", "pass": same_glob_order and left_order == sorted(left_order)},
            {"text": "The documented Pool recipe runs under spawn.", "pass": spawn_exit == 0},
            {"text": "Spawn multiprocessing returns the expected six-record total.", "pass": spawn_exit == 0 and "'count': 3" in spawn_stdout},
            {"text": "A platform-specific multiprocessing failure is prevented or explained.", "pass": False},
        ]

    results["assertions"] = assertions
    results["all_cases_executed"] = len(cases) == 5
    (EVIDENCE / "execution-summary.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (EVIDENCE / "assertions.json").write_text(
        json.dumps(assertions, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"all_cases_executed": True, "case_statuses": {k: v["status"] for k, v in cases.items()}}))


if __name__ == "__main__":
    main()
