#!/usr/bin/env python3
"""Independent exact-byte re-audit harness for bio-cfdna-preprocessing."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

import pysam


RUN_ROOT = Path("/mnt/openscience/audits/bio-cfdna-preprocessing/reaudit-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-cfdna/skills/bio-cfdna-preprocessing")
TOOL_ROOT = Path("/mnt/openscience/audit-envs/bio-cfdna-preprocessing")
FIXTURE = TOOL_ROOT / "data" / "synthetic-umi"
PUBLIC_BAM = TOOL_ROOT / "data" / "nf-core-human" / "test.paired_end.sorted.bam"
EXPECTED_IDENTITY = "148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def candidate_identity() -> dict:
    files = sorted((p for p in CANDIDATE.rglob("*") if p.is_file()), key=lambda p: p.relative_to(CANDIDATE).as_posix().casefold())
    records = []
    manifest_files = []
    for path in files:
        rel = path.relative_to(CANDIDATE).as_posix()
        file_hash = sha256_file(path)
        size = path.stat().st_size
        records.append(f"{rel}\t{size}\t{file_hash}\n")
        manifest_files.append({"path": rel, "bytes": size, "sha256": file_hash})
    manifest = "".join(records).encode("utf-8")
    return {
        "schema": "sha256-manifest-v1",
        "content_sha256": hashlib.sha256(manifest).hexdigest(),
        "manifest_bytes": len(manifest),
        "file_count": len(files),
        "files": manifest_files,
    }


def import_candidate():
    script = CANDIDATE / "scripts" / "preprocess_cfdna.py"
    spec = importlib.util.spec_from_file_location("cfdna_reaudit_candidate", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def summarize_bam(path: Path) -> dict:
    with pysam.AlignmentFile(path, "rb", check_sq=False) as bam:
        header = bam.header.to_dict()
        records = list(bam.fetch(until_eof=True))
    names = [record.query_name for record in records]
    return {
        "path": str(path),
        "sort_order": header.get("HD", {}).get("SO"),
        "group_order": header.get("HD", {}).get("GO"),
        "records": len(records),
        "rx_records": sum(record.has_tag("RX") for record in records),
        "za_records": sum(record.has_tag("ZA") for record in records),
        "zb_records": sum(record.has_tag("ZB") for record in records),
        "mi_records": sum(record.has_tag("MI") for record in records),
        "first_qnames": names[:8],
        "adjacent_first_pairs": all(names[i] == names[i + 1] for i in range(0, min(len(names) - 1, 8), 2)),
    }


def inspect_workflow(root: Path) -> dict:
    stage_paths = {
        "extracted_umis": root / "final_umis.bam",
        "extracted_queryname": root / "final_umis.queryname.bam",
        "aligned_unsorted": root / "final_aligned.unsorted.bam",
        "aligned_template_coordinate": root / "final_aligned.template-coordinate.bam",
        "grouped": root / "final_grouped.bam",
        "consensus_unmapped": root / "final_consensus.unmapped.bam",
        "consensus_mapped_unsorted": root / "final_consensus.mapped.unsorted.bam",
        "consensus_mapped_queryname": root / "final_consensus.mapped.queryname.bam",
        "filtered_queryname": root / "final_filtered.queryname.bam",
        "final": root / "final.bam",
    }
    missing = [name for name, path in stage_paths.items() if not path.is_file()]
    if missing:
        raise AssertionError(f"missing stages: {missing}")
    stages = {name: summarize_bam(path) for name, path in stage_paths.items()}
    final = stage_paths["final"]
    quickcheck = subprocess.run(["samtools", "quickcheck", "-v", str(final)], capture_output=True, text=True)
    index_path = Path(f"{final}.bai")
    return {
        "stages": stages,
        "index_present": index_path.is_file(),
        "quickcheck_returncode": quickcheck.returncode,
        "quickcheck_stdout": quickcheck.stdout,
        "quickcheck_stderr": quickcheck.stderr,
    }


def run_workflow(module, name: str, input_bam: Path, reference: Path, *, duplex: bool) -> dict:
    root = RUN_ROOT / "work" / name
    root.mkdir(parents=True, exist_ok=False)
    command_log = []
    pipeline_log = []
    original_run = module._run
    original_pipeline = module._run_pipeline

    def logged_run(cmd):
        command_log.append([str(part) for part in cmd])
        return original_run(cmd)

    def logged_pipeline(stages):
        materialized = [[str(part) for part in stage] for stage in stages]
        pipeline_log.append(materialized)
        return original_pipeline(materialized)

    module._run = logged_run
    module._run_pipeline = logged_pipeline
    output = root / "final.bam"
    started = time.perf_counter()
    try:
        returned = module.preprocess_cfdna(input_bam, output, reference, duplex=duplex, threads=2)
    finally:
        module._run = original_run
        module._run_pipeline = original_pipeline
    inspection = inspect_workflow(root)
    inspection.update(
        {
            "duplex": duplex,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
            "returned_output": str(returned),
            "output_matches_requested": returned == output,
            "commands": command_log,
            "pipelines": pipeline_log,
        }
    )
    return inspection


def prepare_metachar_fixture() -> tuple[Path, Path]:
    root = RUN_ROOT / "work" / "space ; dollar $ and [brackets]"
    root.mkdir(parents=True, exist_ok=False)
    for source in FIXTURE.glob("reference.fa*"):
        shutil.copy2(source, root / source.name)
    shutil.copy2(FIXTURE / "reference.dict", root / "reference.dict")
    input_bam = root / "raw ; input $.bam"
    shutil.copy2(FIXTURE / "raw.unmapped.bam", input_bam)
    return input_bam, root / "reference.fa"


def qc_cases(module) -> dict:
    public_1 = module.insert_size_qc(PUBLIC_BAM)
    public_2 = module.insert_size_qc(PUBLIC_BAM)
    public_150 = module.insert_size_qc(PUBLIC_BAM, max_size=150)
    flagged = module.insert_size_qc(FIXTURE / "flag-qc.bam")

    empty = RUN_ROOT / "work" / "empty.bam"
    with pysam.AlignmentFile(FIXTURE / "flag-qc.bam", "rb") as source:
        with pysam.AlignmentFile(empty, "wb", header=source.header):
            pass
    empty_result = module.insert_size_qc(empty)

    errors = {}
    for value in (0, -1, True, 1.5):
        try:
            module.insert_size_qc(FIXTURE / "flag-qc.bam", max_size=value)
        except Exception as exc:  # intentional audit capture
            errors[repr(value)] = {"type": type(exc).__name__, "message": str(exc)}
        else:
            errors[repr(value)] = {"type": None, "message": "no exception"}
    return {
        "public_first": public_1,
        "public_second": public_2,
        "public_deterministic": public_1 == public_2,
        "public_max_150": public_150,
        "flag_fixture": flagged,
        "empty": empty_result,
        "invalid_bounds": errors,
    }


def static_checks() -> dict:
    script = CANDIDATE / "scripts" / "preprocess_cfdna.py"
    tree = ast.parse(script.read_text(encoding="utf-8"))
    shell_true = []
    eval_exec = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                eval_exec.append({"name": node.func.id, "line": node.lineno})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    shell_true.append(node.lineno)

    docs = "\n".join(path.read_text(encoding="utf-8") for path in [
        CANDIDATE / "SKILL.md",
        CANDIDATE / "usage-guide.md",
        CANDIDATE / "references" / "fgbio-consensus-workflow.md",
        CANDIDATE / "references" / "method-selection-and-fragment-qc.md",
        CANDIDATE / "references" / "scientific-references.md",
    ])
    guidance_terms = {
        term: bool(re.search(pattern, docs, re.IGNORECASE))
        for term, pattern in {
            "recovery": r"recover(?:y|able)",
            "molecule_count": r"molecule (?:count|depth)|molecular depth",
            "background": r"background",
            "targets": r"target design|targets",
            "preanalytics": r"pre-analytic|pre-analytic|preanalyt",
            "caller": r"call(?:er|ing rule)",
            "lod": r"\bLoD\b|limit of detection",
            "assay_conditional": r"assay-specific|validated assay|empirical(?:ly)?",
        }.items()
    }
    dois = sorted(set(re.findall(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", docs)))
    return {"shell_true_lines": shell_true, "eval_exec": eval_exec, "guidance_terms": guidance_terms, "dois": dois}


def direct_execution() -> dict:
    proc = subprocess.run(
        [sys.executable, str(CANDIDATE / "scripts" / "preprocess_cfdna.py")],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def main() -> int:
    RUN_ROOT.joinpath("evidence").mkdir(parents=True, exist_ok=True)
    RUN_ROOT.joinpath("work").mkdir(parents=True, exist_ok=True)
    identity_before = candidate_identity()
    if identity_before["content_sha256"] != EXPECTED_IDENTITY:
        raise SystemExit(f"identity mismatch before execution: {identity_before['content_sha256']}")

    module = import_candidate()
    ordinary_simplex = run_workflow(module, "fresh-simplex", FIXTURE / "raw.unmapped.bam", FIXTURE / "reference.fa", duplex=False)
    ordinary_duplex = run_workflow(module, "fresh-duplex", FIXTURE / "raw.unmapped.bam", FIXTURE / "reference.fa", duplex=True)
    second_duplex = run_workflow(module, "fresh-duplex-repeat", FIXTURE / "raw.unmapped.bam", FIXTURE / "reference.fa", duplex=True)
    unusual_input, unusual_reference = prepare_metachar_fixture()
    metachar_simplex = run_workflow(
        module,
        "space ; dollar $ and [brackets]/output ; $ [safe]",
        unusual_input,
        unusual_reference,
        duplex=False,
    )

    results = {
        "phase": "reaudit-scientific-skill",
        "auditor": "independent fresh re-auditor; did not perform initial audit or fix",
        "identity_before": identity_before,
        "direct_execution": direct_execution(),
        "ordinary_simplex": ordinary_simplex,
        "ordinary_duplex": ordinary_duplex,
        "second_duplex": second_duplex,
        "metachar_simplex": metachar_simplex,
        "metachar_shell_side_effect_absent": not (RUN_ROOT / "work" / "space ; dollar $ and [brackets]" / "safe").exists(),
        "qc": qc_cases(module),
        "static": static_checks(),
        "identity_after": candidate_identity(),
    }
    results["identity_stable"] = results["identity_before"] == results["identity_after"]
    result_path = RUN_ROOT / "evidence" / "reaudit-results.json"
    result_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "result_path": str(result_path),
        "identity": results["identity_after"]["content_sha256"],
        "identity_stable": results["identity_stable"],
        "simplex_records": ordinary_simplex["stages"]["final"]["records"],
        "duplex_records": ordinary_duplex["stages"]["final"]["records"],
        "duplex_repeat_records": second_duplex["stages"]["final"]["records"],
        "metachar_records": metachar_simplex["stages"]["final"]["records"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
