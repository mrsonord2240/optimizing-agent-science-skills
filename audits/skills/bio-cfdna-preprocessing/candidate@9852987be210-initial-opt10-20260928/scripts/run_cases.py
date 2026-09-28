#!/usr/bin/env python3
"""Bounded, independent initial-audit executions for bio-cfdna-preprocessing."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True

RUN = Path(__file__).resolve().parent
EVIDENCE = RUN / "evidence"
WORK = RUN / "work"
TOOLING = Path("/mnt/openscience/audit-envs/bio-cfdna-preprocessing")
CANDIDATE = Path("/mnt/openscience/wt/opt10-cfdna/skills/bio-cfdna-preprocessing")
SCRIPT = CANDIDATE / "scripts" / "preprocess_cfdna.py"
ENV_BIN = TOOLING / "conda-env" / "bin"
SYNTH = TOOLING / "data" / "synthetic-umi"
PUBLIC_BAM = TOOLING / "data" / "nf-core-human" / "test.paired_end.sorted.bam"
RUN_ENV = os.environ.copy()
RUN_ENV["PATH"] = str(ENV_BIN) + os.pathsep + RUN_ENV.get("PATH", "")
RUN_ENV["PYTHONDONTWRITEBYTECODE"] = "1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_manifest() -> dict[str, Any]:
    files = sorted(
        (path for path in CANDIDATE.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(CANDIDATE).as_posix(),
    )
    rows = []
    identities = []
    for path in files:
        relative = path.relative_to(CANDIDATE).as_posix()
        size = path.stat().st_size
        digest = sha256(path)
        rows.append(f"{relative}\t{size}\t{digest}")
        identities.append({"path": relative, "bytes": size, "sha256": digest})
    manifest = "\n".join(rows) + "\n"
    return {
        "content_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest(),
        "manifest_bytes": len(manifest.encode("utf-8")),
        "file_count": len(files),
        "recipe": "relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; ordinal path order; LF after every record including the final record",
        "files": identities,
    }


def load_candidate():
    spec = importlib.util.spec_from_file_location("candidate_preprocess_cfdna", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run(name: str, argv: list[str] | str, *, shell: bool = False, timeout: int = 180) -> dict[str, Any]:
    stdout_path = EVIDENCE / f"{name}.stdout.txt"
    stderr_path = EVIDENCE / f"{name}.stderr.txt"
    try:
        completed = subprocess.run(
            argv,
            shell=shell,
            executable="/bin/bash" if shell else None,
            env=RUN_ENV,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        return {
            "argv": argv,
            "shell": shell,
            "returncode": completed.returncode,
            "stdout": stdout_path.name,
            "stderr": stderr_path.name,
        }
    except subprocess.TimeoutExpired as error:
        stdout_path.write_text(error.stdout or "", encoding="utf-8")
        stderr_path.write_text(error.stderr or "", encoding="utf-8")
        return {
            "argv": argv,
            "shell": shell,
            "returncode": None,
            "timeout_seconds": timeout,
            "stdout": stdout_path.name,
            "stderr": stderr_path.name,
        }


def q(path: Path) -> str:
    return shlex.quote(str(path))


def bam_count(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        with pysam.AlignmentFile(path, "rb", check_sq=False) as bam:
            return sum(1 for _ in bam.fetch(until_eof=True))
    except Exception:
        return None


def qc_population(path: Path, max_size: int = 600) -> dict[str, int]:
    counts = {
        "all": 0,
        "candidate_included": 0,
        "secondary_included": 0,
        "supplementary_included": 0,
        "duplicate_included": 0,
        "qc_fail_included": 0,
    }
    with pysam.AlignmentFile(path, "rb") as bam:
        for read in bam.fetch():
            counts["all"] += 1
            included = read.is_proper_pair and not read.is_secondary and 0 < read.template_length <= max_size
            if included:
                counts["candidate_included"] += 1
                counts["secondary_included"] += int(read.is_secondary)
                counts["supplementary_included"] += int(read.is_supplementary)
                counts["duplicate_included"] += int(read.is_duplicate)
                counts["qc_fail_included"] += int(read.is_qcfail)
    return counts


def shell_risk() -> dict[str, Any]:
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "run":
            continue
        shell_true = any(
            keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True
            for keyword in node.keywords
        )
        if shell_true:
            calls.append({"line": node.lineno, "source": ast.get_source_segment(source, node)})
    return {
        "shell_true_calls": calls,
        "validated_path_or_thread_arguments": False,
        "risk": "input-derived reference, output, intermediate paths, and thread count are interpolated into shell command strings",
    }


try:
    import pysam
except ImportError as error:  # pragma: no cover - environment evidence
    raise SystemExit(f"Pinned environment is missing pysam: {error}")


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    WORK.mkdir(parents=True, exist_ok=False)
    results: dict[str, Any] = {
        "candidate_identity": candidate_manifest(),
        "python": sys.version.split()[0],
        "pysam": pysam.__version__,
        "shell_risk": shell_risk(),
        "commands": {},
    }
    results["commands"]["structural_precheck"] = run(
        "structural-precheck",
        [
            sys.executable,
            str(RUN / "skill-auditor" / "scripts" / "evaluate_skill.py"),
            str(CANDIDATE),
            "--json-only",
        ],
    )
    results["commands"]["direct_execution"] = run(
        "direct-execution", [sys.executable, str(SCRIPT)]
    )

    candidate = load_candidate()
    flag_bam = SYNTH / "flag-qc.bam"
    results["insert_size_qc"] = {
        "public_bam": str(PUBLIC_BAM),
        "public_result": candidate.insert_size_qc(PUBLIC_BAM),
        "public_population": qc_population(PUBLIC_BAM),
        "flag_fixture": str(flag_bam),
        "flag_result": candidate.insert_size_qc(flag_bam),
        "flag_population": qc_population(flag_bam),
        "empty_max_size_result": candidate.insert_size_qc(flag_bam, max_size=-1),
    }

    raw_bam = SYNTH / "raw.unmapped.bam"
    reference = SYNTH / "reference.fa"
    for label, duplex in (("simplex", False), ("duplex", True)):
        output = WORK / label / "final.bam"
        output.parent.mkdir()
        argv = [
            sys.executable,
            str(TOOLING / "call_candidate.py"),
            "--script", str(SCRIPT),
            "--input", str(raw_bam),
            "--output", str(output),
            "--reference", str(reference),
            "--threads", "2",
        ]
        if duplex:
            argv.append("--duplex")
        results["commands"][f"candidate_{label}"] = run(f"candidate-{label}", argv)
        results[f"candidate_{label}_final_exists"] = output.exists()

    exact_extract = WORK / "exact-extract.bam"
    results["commands"]["exact_extract"] = run(
        "exact-extract",
        [
            "fgbio", "ExtractUmisFromBam",
            "--input", str(raw_bam),
            "--output", str(exact_extract),
            "--read-structure", "6M11S+T", "6M11S+T",
            "--single-tag", "RX",
        ],
    )

    control_umis = TOOLING / "work" / "manual" / "with_umis.bam"
    bwa_sam = WORK / "bwa-direct-bam.sam"
    results["commands"]["bwa_direct_bam"] = run(
        "bwa-direct-bam",
        f"bwa mem -t 2 -Y {q(reference)} {q(control_umis)} > {q(bwa_sam)}",
        shell=True,
    )
    results["commands"]["bwa_direct_bam_parse"] = run(
        "bwa-direct-bam-parse", ["samtools", "view", "-c", str(bwa_sam)]
    )

    coordinate_mapped = TOOLING / "work" / "manual" / "simplex.consensus.mapped.bam"
    queryname_mapped = TOOLING / "work" / "manual" / "simplex.consensus.mapped.queryname.bam"
    exact_filtered = WORK / "filter-coordinate.bam"
    control_filtered = WORK / "filter-queryname.bam"
    filter_args = [
        "--ref", str(reference), "--min-reads", "2",
        "--max-read-error-rate", "0.025", "--max-base-error-rate", "0.1",
        "--min-base-quality", "40", "--reverse-per-base-tags",
    ]
    results["commands"]["filter_coordinate"] = run(
        "filter-coordinate",
        ["fgbio", "FilterConsensusReads", "--input", str(coordinate_mapped), "--output", str(exact_filtered), *filter_args],
    )
    results["commands"]["filter_queryname_control"] = run(
        "filter-queryname-control",
        ["fgbio", "FilterConsensusReads", "--input", str(queryname_mapped), "--output", str(control_filtered), *filter_args],
    )
    results["filter_queryname_control_records"] = bam_count(control_filtered)

    space_source = TOOLING / "work" / "space case"
    space_output = WORK / "space output" / "consensus mapped.bam"
    space_output.parent.mkdir()
    space_unmapped = space_source / "consensus unmapped.bam"
    space_reference = space_source / "reference genome.fa"
    unquoted = (
        f"samtools fastq {space_unmapped} | bwa mem -t 2 -Y -p {space_reference} - "
        f"| fgbio ZipperBams --unmapped {space_unmapped} --ref {space_reference} "
        f"| samtools sort -o {space_output} -"
    )
    results["commands"]["unquoted_space_realign"] = run(
        "unquoted-space-realign", unquoted, shell=True
    )
    results["unquoted_space_output_exists"] = space_output.exists()

    ordinary_output = WORK / "ordinary-realign.bam"
    ordinary_unmapped = TOOLING / "work" / "manual" / "simplex.consensus.unmapped.bam"
    ordinary = (
        f"samtools fastq {q(ordinary_unmapped)} | bwa mem -t 2 -Y -p {q(reference)} - "
        f"| fgbio ZipperBams --unmapped {q(ordinary_unmapped)} --ref {q(reference)} "
        f"| samtools sort -o {q(ordinary_output)} -"
    )
    results["commands"]["quoted_ordinary_realign_control"] = run(
        "quoted-ordinary-realign-control", ordinary, shell=True
    )
    results["quoted_ordinary_realign_records"] = bam_count(ordinary_output)

    output = EVIDENCE / "execution-summary.json"
    output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
