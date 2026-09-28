#!/usr/bin/env python3
"""Independent execution matrix for bio-batch-processing final certification."""

from __future__ import annotations

import ast
import csv
import gzip
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import traceback
import warnings
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
warnings.simplefilter("error", ResourceWarning)

AUDIT = Path("/mnt/openscience/audits/bio-batch-processing/reaudit-opt10-20260928")
EVIDENCE = AUDIT / "evidence"
CANDIDATE = Path("/mnt/openscience/wt/opt10-batch-processing/skills/bio-batch-processing")
TOOLS = Path("/mnt/openscience/audit-envs/bio-batch-processing")
PYTHON = TOOLS / "conda-env/bin/python"
PUBLIC = TOOLS / "data/public"
sys.path.insert(0, str(CANDIDATE / "scripts"))

from Bio import SeqIO  # noqa: E402
from Bio.Seq import Seq  # noqa: E402
from Bio.SeqRecord import SeqRecord  # noqa: E402
import batch_process as batch  # noqa: E402
import pyfastx_index  # noqa: E402
import pysam  # noqa: E402


EXPECTED_IDENTITY = "f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd"
RESULTS = {"candidate_identity": EXPECTED_IDENTITY, "cases": [], "surface_checks": {}}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_fasta(path: Path, records) -> int:
    return SeqIO.write(
        (SeqRecord(Seq(sequence), id=identifier, description="") for identifier, sequence in records),
        path,
        "fasta",
    )


def parse_ids(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as handle:
        return [record.id for record in SeqIO.parse(handle, "fasta")]


def iter_fasta_paths(paths):
    """Yield records while explicitly closing each input handle."""
    for path in paths:
        with Path(path).open("r", encoding="utf-8") as handle:
            yield from SeqIO.parse(handle, "fasta")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def case(index, kind, label, function):
    record = {"index": index, "type": kind, "label": label, "status": "ERROR", "checks": {}}
    try:
        with tempfile.TemporaryDirectory(prefix=f"batch-reaudit-{index}-") as temporary:
            function(Path(temporary), record["checks"])
        record["status"] = "COMPLETED"
    except Exception as exc:
        record["error"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
    RESULTS["cases"].append(record)


def canonical(root: Path, out: dict):
    data = root / "data"
    data.mkdir()
    first = data / "b.fasta"
    second = data / "a.fasta"
    write_fasta(first, [(f"b{i}", "ACGT" * (i + 1)) for i in range(4)])
    write_fasta(second, [(f"a{i}", "GCA" * (i + 1)) for i in range(3)])

    counts = {path.name: batch.count_streaming(path, "fasta") for path in batch.stable_paths(data, "*.fasta")}
    check(counts == {"a.fasta": 3, "b.fasta": 4}, f"unexpected counts: {counts}")

    chunks = [Path(path) for path in batch.split_by_count(first, "fasta", 3, root / "chunk")]
    chunk_sizes = [len(parse_ids(path)) for path in chunks]
    check(chunk_sizes == [3, 1], f"unexpected chunks: {chunk_sizes}")
    fresh = root / "fresh.fasta"
    write_fasta(fresh, [(f"fresh{i}", "AT") for i in range(5)])
    fresh_chunks = [Path(path) for path in batch.split_by_count(fresh, "fasta", 2, root / "fresh-chunk")]
    check([len(parse_ids(path)) for path in fresh_chunks] == [2, 2, 1], "fresh split not 2/2/1")

    merged = root / "merged.fasta"
    merged_count = SeqIO.write(
        iter_fasta_paths(batch.stable_paths(data, "*.fasta")),
        merged,
        "fasta",
    )
    check(merged_count == 7 and parse_ids(merged) == ["a0", "a1", "a2", "b0", "b1", "b2", "b3"], "merge mismatch")

    index_path = root / "combined.idx"
    records = SeqIO.index_db(str(index_path), [str(path) for path in batch.stable_paths(data, "*.fasta")], "fasta")
    check(len(records) == 7 and str(records["b3"].seq) == "ACGT" * 4, "initial index mismatch")
    records.close()
    reopened = SeqIO.index_db(str(index_path))
    check(len(reopened) == 7 and len(reopened["a2"].seq) == 9, "reopened index mismatch")
    reopened.close()

    converted = root / "orchid.fasta"
    converted_count = SeqIO.convert(str(PUBLIC / "ls_orchid.gbk"), "genbank", str(converted), "fasta")
    check(converted_count == 94, f"conversion count {converted_count}")
    with (PUBLIC / "ls_orchid.gbk").open() as source, converted.open() as target:
        source_first = next(SeqIO.parse(source, "genbank"))
        target_first = next(SeqIO.parse(target, "fasta"))
    check(source_first.id == target_first.id and source_first.seq == target_first.seq, "conversion sequence mismatch")

    demo = subprocess.run(
        [str(PYTHON), "-B", str(CANDIDATE / "scripts/batch_process.py")],
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
    )
    check("sample0.fasta: 5 sequences" in demo.stdout, "demo count missing")
    check("Split sample0.fasta into 3 chunks of <=2 records" in demo.stdout, "demo split missing")
    check("Indexed 15 records across 3 files" in demo.stdout and "length: 52" in demo.stdout, "demo index values missing")
    out.update({
        "counts": counts,
        "chunk_sizes": chunk_sizes,
        "fresh_chunk_sizes": [len(parse_ids(path)) for path in fresh_chunks],
        "merged_records": merged_count,
        "indexed_records": 7,
        "converted_records": converted_count,
        "standalone_stdout": demo.stdout.strip().splitlines(),
    })


def readers(root: Path, out: dict):
    compressed_fasta = root / "orchid.fasta.gz"
    with (PUBLIC / "ls_orchid.fasta").open("rb") as source, gzip.open(compressed_fasta, "wb") as target:
        shutil.copyfileobj(source, target)
    with (PUBLIC / "ls_orchid.fasta").open() as handle:
        records = list(SeqIO.parse(handle, "fasta"))
    first_id, last_id = records[0].id, records[-1].id
    first = pyfastx_index.inspect_fasta(compressed_fasta, first_id)
    index_path = Path(first["index"])
    index_hash = sha256(index_path)
    index_inode = index_path.stat().st_ino
    second = pyfastx_index.inspect_fasta(compressed_fasta, last_id)
    check(sha256(index_path) == index_hash and index_path.stat().st_ino == index_inode, "function did not reuse index")
    cli = subprocess.run(
        [str(PYTHON), "-B", str(CANDIDATE / "scripts/pyfastx_index.py"), str(compressed_fasta), "--record-id", first_id],
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
    )
    cli_payload = json.loads(cli.stdout)
    check(first["records"] == second["records"] == cli_payload["records"] == 94, "pyfastx record count mismatch")
    check(first["selected_length"] == len(records[0]) and second["selected_length"] == len(records[-1]), "random-access length mismatch")
    check(sha256(index_path) == index_hash and index_path.stat().st_ino == index_inode, "CLI rebuilt index")

    compressed_fastq = root / "example.fastq.gz"
    with (PUBLIC / "example.fastq").open("rb") as source, gzip.open(compressed_fastq, "wb") as target:
        shutil.copyfileobj(source, target)
    with pysam.FastxFile(str(compressed_fastq)) as handle:
        thin = list(handle)
    with (PUBLIC / "example.fastq").open() as handle:
        full = list(SeqIO.parse(handle, "fastq"))
    check(len(thin) == len(full) == 3, "FASTQ count mismatch")
    check(thin[0].sequence == str(full[0].seq), "FASTQ sequence mismatch")
    check(list(thin[0].get_quality_array()) == full[0].letter_annotations["phred_quality"], "Phred+33 mismatch")

    legacy = root / "legacy.fastq"
    legacy.write_text("@legacy\nACGT\n+\nhhhh\n", encoding="ascii")
    with pysam.FastxFile(str(legacy)) as handle:
        pysam_quality = next(handle).get_quality_array()[0]
    with legacy.open() as handle:
        illumina_quality = next(SeqIO.parse(handle, "fastq-illumina")).letter_annotations["phred_quality"][0]
    check((pysam_quality, illumina_quality) == (71, 40), f"quality caveat mismatch: {(pysam_quality, illumina_quality)}")
    out.update({
        "pyfastx_records": 94,
        "function_selected_lengths": [first["selected_length"], second["selected_length"]],
        "cli_selected_length": cli_payload["selected_length"],
        "index_reused_function_and_cli": True,
        "fastq_records": 3,
        "phred33_first_range": [min(thin[0].get_quality_array()), max(thin[0].get_quality_array())],
        "legacy_pysam_vs_illumina": [pysam_quality, illumina_quality],
    })


def edges(root: Path, out: dict):
    empty_summary = root / "empty-summary.csv"
    check(batch.summarize_files([], "fasta", empty_summary) == [], "empty summary did not return []")
    with empty_summary.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    check(rows == [list(batch.SUMMARY_FIELDS)], f"unexpected empty schema: {rows}")

    empty_fasta = root / "empty.fasta"
    empty_fasta.write_text("", encoding="utf-8")
    zero_summary = root / "zero-summary.csv"
    zero_rows = batch.summarize_files([empty_fasta], "fasta", zero_summary)
    check(zero_rows == [{"file": "empty.fasta", "sequences": 0, "total_bp": 0, "min_len": 0, "max_len": 0, "avg_len": 0}], f"empty file metrics mismatch: {zero_rows}")

    missing = root / "deliberately-missing.fasta"
    invalid_errors = {}
    for value in (False, True, 0, -1, 1.5, "2"):
        before = sorted(path.name for path in root.iterdir())
        try:
            batch.split_by_count(missing, "fasta", value, root / "invalid")
        except ValueError as exc:
            invalid_errors[repr(value)] = str(exc)
            check("records_per_file must be a positive integer" in str(exc), f"non-actionable error: {exc}")
        else:
            raise AssertionError(f"invalid chunk accepted: {value!r}")
        check(before == sorted(path.name for path in root.iterdir()), f"invalid chunk {value!r} created output")

    valid = root / "valid.fasta"
    write_fasta(valid, [(f"v{i}", "AC") for i in range(5)])
    valid_chunks = [Path(path) for path in batch.split_by_count(valid, "fasta", 2, root / "valid")]
    check([len(parse_ids(path)) for path in valid_chunks] == [2, 2, 1], "valid split mismatch")
    for invalid_workers in (0, -2, True, 1.5):
        try:
            batch.process_files_parallel([], workers=invalid_workers)
        except ValueError as exc:
            check("workers must be a positive integer" in str(exc), "worker error not actionable")
        else:
            raise AssertionError(f"invalid workers accepted: {invalid_workers!r}")
    out.update({
        "header": rows[0],
        "empty_file_row": zero_rows[0],
        "invalid_chunk_errors": invalid_errors,
        "valid_chunk_sizes": [len(parse_ids(path)) for path in valid_chunks],
        "invalid_workers_rejected": 4,
    })


def prefix_safety(root: Path, out: dict):
    safety = {}
    source = root / "hostile.fasta"
    sibling = root / "escaped.fasta"
    sibling.write_text("sentinel\n", encoding="utf-8")
    write_fasta(source, [("../escaped_record", "ACGT")])
    hostile_out = root / "hostile-out"
    try:
        batch.split_by_prefix(source, "fasta", hostile_out, max_open_files=2)
    except ValueError as exc:
        check("unsafe record-id prefix" in str(exc), "hostile path error mismatch")
    else:
        raise AssertionError("hostile traversal accepted")
    hostile_manifest = json.loads((hostile_out / "split-prefix-manifest.json").read_text())
    check(sibling.read_text() == "sentinel\n", "sibling overwritten")
    check(hostile_manifest["status"] == "partial" and hostile_manifest["records_written"] == 0, "hostile manifest mismatch")
    safety["traversal_rejected_sibling_preserved"] = True

    reserved = root / "reserved.fasta"
    write_fasta(reserved, [("CON_1", "A")])
    try:
        batch.split_by_prefix(reserved, "fasta", root / "reserved-out", max_open_files=2)
    except ValueError as exc:
        check("reserved filename" in str(exc), "reserved-name error mismatch")
    else:
        raise AssertionError("reserved filename accepted")

    existing = root / "existing.fasta"
    write_fasta(existing, [("sample_1", "AC")])
    existing_out = root / "existing-out"
    existing_out.mkdir()
    target = existing_out / "sample.fasta"
    target.write_text("sentinel\n", encoding="utf-8")
    try:
        batch.split_by_prefix(existing, "fasta", existing_out, max_open_files=2)
    except FileExistsError:
        pass
    else:
        raise AssertionError("existing target overwritten")
    check(target.read_text() == "sentinel\n", "existing target content changed")
    safety["exclusive_target_preserved"] = True

    manifest_source = root / "manifest.fasta"
    write_fasta(manifest_source, [("safe_1", "AC")])
    try:
        batch.split_by_prefix(manifest_source, "fasta", root / "manifest-out", manifest_name="../escaped.json")
    except ValueError as exc:
        check("directly inside output_directory" in str(exc), "manifest containment error mismatch")
    else:
        raise AssertionError("manifest path escaped")
    check(not (root / "escaped.json").exists(), "escaped manifest created")
    safety["manifest_escape_rejected"] = True

    collision = root / "collision.fasta"
    write_fasta(collision, [("Sample_1", "AC"), ("sample_2", "GT")])
    collision_out = root / "collision-out"
    try:
        batch.split_by_prefix(collision, "fasta", collision_out, max_open_files=2)
    except ValueError as exc:
        check("case-insensitive filesystems" in str(exc), "collision error mismatch")
    else:
        raise AssertionError("case-insensitive collision accepted")
    collision_manifest = json.loads((collision_out / "split-prefix-manifest.json").read_text())
    check(collision_manifest["status"] == "partial" and collision_manifest["records_written"] == 1, "collision accounting mismatch")

    many = root / "many.fasta"
    write_fasta(many, ((f"p{i:04d}_1", "ACGT") for i in range(2048)))
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    desired = min(32, hard)
    resource.setrlimit(resource.RLIMIT_NOFILE, (desired, hard))
    before = len(os.listdir("/proc/self/fd"))
    try:
        manifest = batch.split_by_prefix(many, "fasta", root / "many-out", max_open_files=8)
    finally:
        resource.setrlimit(resource.RLIMIT_NOFILE, (soft, hard))
    after = len(os.listdir("/proc/self/fd"))
    parsed_total = sum(len(parse_ids(root / "many-out" / item["path"])) for item in manifest["files"])
    check(manifest["status"] == "complete", "many-prefix manifest incomplete")
    check(manifest["records_written"] == len(manifest["files"]) == parsed_total == 2048, "many-prefix totals mismatch")
    check(sum(item["records"] for item in manifest["files"]) == 2048, "manifest per-file total mismatch")
    check(after <= before + 1, f"descriptor leak: before={before}, after={after}")

    interleaved = root / "interleaved.fasta"
    write_fasta(interleaved, [("a_1", "A"), ("b_1", "CC"), ("c_1", "GGG"), ("a_2", "TTTT")])
    inter_manifest = batch.split_by_prefix(interleaved, "fasta", root / "interleaved-out", max_open_files=2)
    check(inter_manifest["records_written"] == 4 and parse_ids(root / "interleaved-out/a.fasta") == ["a_1", "a_2"], "evicted group lost data")
    out.update({
        "safety": safety,
        "case_collision_partial_records": collision_manifest["records_written"],
        "many_prefixes": 2048,
        "max_open_files": 8,
        "rlimit_nofile": desired,
        "parsed_records": parsed_total,
        "fd_before_after": [before, after],
        "interleaved_a_ids": parse_ids(root / "interleaved-out/a.fasta"),
    })


def deterministic_parallel(root: Path, out: dict):
    left, right = root / "left", root / "right"
    for directory in (left, right):
        (directory / "z").mkdir(parents=True)
    relative_names = ["z/B.fasta", "a.fasta", "z/a.fasta"]
    for directory, order in ((left, relative_names), (right, list(reversed(relative_names)))):
        for relative in order:
            path = directory / relative
            write_fasta(path, [(relative.replace("/", "-") + "-1", "ACG"), (relative.replace("/", "-") + "-2", "TT")])
    left_paths = batch.stable_paths(left, "*.fasta", recursive=True)
    right_paths = batch.stable_paths(right, "*.fasta", recursive=True)
    left_rel = [path.relative_to(left).as_posix() for path in left_paths]
    right_rel = [path.relative_to(right).as_posix() for path in right_paths]
    expected = ["a.fasta", "z/a.fasta", "z/B.fasta"]
    check(left_rel == right_rel == expected, f"stable order mismatch: {left_rel} / {right_rel}")

    left_summary = left / "summary.csv"
    right_summary = right / "summary.csv"
    left_rows = batch.summarize_files(left_paths, "fasta", left_summary)
    right_rows = batch.summarize_files(right_paths, "fasta", right_summary)
    check(left_rows == right_rows and left_summary.read_bytes() == right_summary.read_bytes(), "summary is not byte deterministic")

    def merge(paths, destination):
        return SeqIO.write(iter_fasta_paths(paths), destination, "fasta")

    left_merged = left / "merged.fasta"
    right_merged = right / "merged.fasta"
    check(merge(left_paths, left_merged) == merge(right_paths, right_merged) == 6, "merge count mismatch")
    check(left_merged.read_bytes() == right_merged.read_bytes(), "merge bytes differ")

    fork_rows = batch.process_files_parallel(list(reversed(left_paths)), workers=2, start_method="fork")
    spawn_rows = batch.process_files_parallel(right_paths, workers=2, start_method="spawn")
    rerun_rows = batch.process_files_parallel(left_paths, workers=2, start_method="spawn")
    check(fork_rows == spawn_rows == rerun_rows, f"parallel results differ: {fork_rows} / {spawn_rows}")
    check(sum(row["count"] for row in fork_rows) == 6 and sum(row["total_bp"] for row in fork_rows) == 15, "parallel totals mismatch")
    out.update({
        "stable_relative_paths": expected,
        "summary_sha256": sha256(left_summary),
        "merge_sha256": sha256(left_merged),
        "parallel_rows": fork_rows,
        "fork_spawn_rerun_equal": True,
        "records": 6,
        "total_bp": 15,
    })


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    identity = json.loads((AUDIT / "source-identity.json").read_text())
    check(identity["candidate"]["content_sha256"] == EXPECTED_IDENTITY, "candidate identity drift")

    python_files = sorted(CANDIDATE.rglob("*.py"))
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    RESULTS["surface_checks"]["ast_files"] = [path.relative_to(CANDIDATE).as_posix() for path in python_files]
    RESULTS["surface_checks"]["candidate_cache_before"] = identity["candidate_cache_artifacts"]
    RESULTS["surface_checks"]["versions"] = {
        "python": sys.version.split()[0],
        "biopython": __import__("Bio").__version__,
        "pysam": pysam.__version__,
        "pyfastx": __import__("pyfastx").version(),
    }
    RESULTS["surface_checks"]["isolation"] = {
        "user": os.environ.get("USER"),
        "wsl_interop": os.environ.get("WSL_INTEROP"),
        "mount_f_present": os.path.ismount("/mnt/f"),
        "candidate_writable_attempted": False,
    }

    case(1, "Canonical", "Count, merge, split, index, convert, and standalone demo", canonical)
    case(2, "Variant A", "pyfastx gzip reuse and pysam quality semantics", readers)
    case(3, "Edge", "Empty summaries and invalid chunk/worker bounds", edges)
    case(4, "Variant B", "Contained prefix splitting under hostile and high-cardinality inputs", prefix_safety)
    case(5, "Stress", "Creation-order determinism and fork/spawn parity", deterministic_parallel)

    shipped = subprocess.run(
        [str(PYTHON), "-B", str(CANDIDATE / "tests/test_batch_process.py")],
        text=True,
        capture_output=True,
        timeout=120,
        env={**os.environ, "PYTHONWARNINGS": "error::ResourceWarning", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    RESULTS["surface_checks"]["shipped_regression_suite"] = {
        "returncode": shipped.returncode,
        "stdout": shipped.stdout.strip().splitlines(),
        "stderr": shipped.stderr.strip().splitlines(),
        "resource_warnings_fatal": True,
    }
    RESULTS["all_cases_completed"] = all(record["status"] == "COMPLETED" for record in RESULTS["cases"])
    RESULTS["all_surfaces_passed"] = RESULTS["all_cases_completed"] and shipped.returncode == 0
    RESULTS["surface_checks"]["candidate_cache_after"] = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file() and (path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts)
    )
    (EVIDENCE / "reaudit-results.json").write_text(json.dumps(RESULTS, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_cases_completed": RESULTS["all_cases_completed"],
        "all_surfaces_passed": RESULTS["all_surfaces_passed"],
        "case_statuses": [record["status"] for record in RESULTS["cases"]],
        "shipped_suite_returncode": shipped.returncode,
    }, sort_keys=True))
    if not RESULTS["all_surfaces_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
