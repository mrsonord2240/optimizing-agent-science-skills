#!/usr/bin/env python3
"""Independent bounded audit harness for the exact bio-codon-usage candidate."""

from __future__ import annotations

import contextlib
import hashlib
import inspect
import io
import json
import math
import re
import runpy
import subprocess
import sys
import warnings
from pathlib import Path

import Bio
from Bio.Data import CodonTable
from Bio.Data.CodonTable import standard_dna_table
from Bio.Seq import Seq
from Bio.SeqUtils import CodonAdaptationIndex, GC123


RUN = Path("/mnt/openscience/audits/bio-codon-usage/initial-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-codon-usage/skills/bio-codon-usage")
TOOLING = Path("/mnt/openscience/audit-envs/bio-codon-usage")
ENV = TOOLING / "env"
CODONW = ENV / "bin/codonw"
EVIDENCE = RUN / "evidence"
INPUTS = RUN / "inputs"
OUTPUTS = RUN / "outputs"
for directory in (EVIDENCE, INPUTS, OUTPUTS):
    directory.mkdir(parents=True, exist_ok=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exception_record(callable_):
    try:
        value = callable_()
        return {"type": None, "message": None, "value": str(value)}
    except Exception as exc:  # noqa: BLE001 - boundary behavior is the subject.
        return {"type": type(exc).__name__, "message": str(exc), "value": None}


checks: list[dict] = []


def check(name: str, passed: bool, detail) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


# Exact candidate identity, calculated without using the preparation harness.
manifest_lines: list[str] = []
for path in sorted((p for p in CANDIDATE.rglob("*") if p.is_file()), key=lambda p: p.relative_to(CANDIDATE).as_posix()):
    data = path.read_bytes()
    manifest_lines.append(
        f"{path.relative_to(CANDIDATE).as_posix()}\t{len(data)}\t{sha256_bytes(data)}"
    )
manifest = "\n".join(manifest_lines).encode("utf-8")
(EVIDENCE / "candidate-manifest-current.tsv").write_bytes(manifest)
identity = sha256_bytes(manifest)
check("candidate-file-count", len(manifest_lines) == 9, len(manifest_lines))
check("candidate-manifest-bytes", len(manifest) == 862, len(manifest))
check(
    "candidate-identity",
    identity == "13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77",
    identity,
)


def run_script(name: str, ordinal: int) -> dict:
    command = [sys.executable, str(CANDIDATE / "scripts" / name)]
    completed = subprocess.run(command, text=True, capture_output=True, timeout=30, check=False)
    stem = Path(name).stem
    (OUTPUTS / f"{ordinal:02d}-{stem}.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (OUTPUTS / f"{ordinal:02d}-{stem}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_sha256": sha256_bytes(completed.stdout.encode()),
        "stderr_sha256": sha256_bytes(completed.stderr.encode()),
        "stdout_lines": completed.stdout.splitlines(),
        "stderr_lines": completed.stderr.splitlines(),
    }


# Execute every shipped script twice and compare exact bytes.
scripts = ("basic_analysis.py", "rscu_analysis.py", "cai_optimization.py")
first_runs = {name: run_script(name, index + 1) for index, name in enumerate(scripts)}
second_runs = {name: run_script(name, index + 4) for index, name in enumerate(scripts)}
for name in scripts:
    first = first_runs[name]
    second = second_runs[name]
    check(f"{name}-exit-zero", first["returncode"] == 0, first["returncode"])
    check(f"{name}-stderr-empty", not first["stderr_lines"], first["stderr_lines"])
    check(
        f"{name}-byte-deterministic",
        first["stdout_sha256"] == second["stdout_sha256"],
        [first["stdout_sha256"], second["stdout_sha256"]],
    )


def load_script(name: str) -> dict:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return runpy.run_path(str(CANDIDATE / "scripts" / name))


basic = load_script("basic_analysis.py")
rscu_module = load_script("rscu_analysis.py")
count_codons = basic["count_codons"]
codon_frequencies = basic["codon_frequencies"]
calculate_rscu = rscu_module["calculate_rscu"]

boundary = {
    "valid_counts": dict(count_codons("ATGAAATTTTAA")),
    "partial_counts": dict(count_codons("ATGAA")),
    "shifted_counts": dict(count_codons("AATGAAATTTTAA")),
    "ambiguous_counts": dict(count_codons("ATGNNNTAA")),
    "empty_frequencies": codon_frequencies(""),
    "empty_gc123": exception_record(lambda: GC123(Seq(""))),
    "rscu_valid": calculate_rscu("CTTCTG"),
    "rscu_partial_equals_prefix": calculate_rscu("CTTCT") == calculate_rscu("CTT"),
    "rscu_ambiguous_equals_valid": calculate_rscu("CTTNNNCTG") == calculate_rscu("CTTCTG"),
    "rscu_stop_equals_valid": calculate_rscu("CTTTAACTG") == calculate_rscu("CTTCTG"),
}
check("valid-codon-count", boundary["valid_counts"] == {"ATG": 1, "AAA": 1, "TTT": 1, "TAA": 1}, boundary["valid_counts"])
check("partial-is-silently-truncated", boundary["partial_counts"] == {"ATG": 1}, boundary["partial_counts"])
check("shifted-frame-is-silently-accepted", list(boundary["shifted_counts"]) == ["AAT", "GAA", "ATT", "TTA"], boundary["shifted_counts"])
check("ambiguity-is-retained-in-basic-count", "NNN" in boundary["ambiguous_counts"], boundary["ambiguous_counts"])
check("empty-frequency-helper-is-safe", boundary["empty_frequencies"] == {}, boundary["empty_frequencies"])
check("empty-gc123-errors", boundary["empty_gc123"]["type"] == "ZeroDivisionError", boundary["empty_gc123"])
check("rscu-partial-is-silently-truncated", boundary["rscu_partial_equals_prefix"], boundary["rscu_partial_equals_prefix"])
check("rscu-ambiguity-is-silently-ignored", boundary["rscu_ambiguous_equals_valid"], boundary["rscu_ambiguous_equals_valid"])
check("rscu-stop-is-silently-ignored", boundary["rscu_stop_equals_valid"], boundary["rscu_stop_equals_valid"])


# Independent Biopython 1.85 CAI probes.
reference = [Seq("ATGGCTGCTGCTTAA"), Seq("ATGGCTGCTGCTTAA")]
cai = CodonAdaptationIndex(reference, table=standard_dna_table)
stop_index = CodonAdaptationIndex([Seq("ATGGCTTAAGCTTAA")])
score_no_stop = stop_index.calculate(Seq("GCT"))
score_with_unobserved_stop = stop_index.calculate(Seq("GCTTAG"))
unobserved_weight = CodonAdaptationIndex([Seq("GCT" * 10)])["GCC"]
empty_score = exception_record(lambda: cai.calculate(Seq("")))
excluded_score = exception_record(lambda: cai.calculate(Seq("ATGTGG")))
partial_score = exception_record(lambda: cai.calculate(Seq("GCTAT")))

tie_index = CodonAdaptationIndex([Seq("GCTGCCGCAGCG")])
strict_tie = exception_record(lambda: tie_index.optimize(Seq("GCT"), strict=True))
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    nonstrict_tie = tie_index.optimize(Seq("GCT"), strict=False)
nonstrict_warnings = [str(item.message) for item in caught]

table2 = CodonTable.unambiguous_dna_by_id[2]
table2_index = CodonAdaptationIndex([Seq("ATGTGATGATAA")], table=table2)
table2_tgg = exception_record(lambda: table2_index.calculate(Seq("TGG")))
table2_optimized_tga = table2_index.optimize(Seq("TGA"), seq_type="DNA", strict=False)
table2_input_protein = str(Seq("TGA").translate(table=2))
table2_output_protein = str(table2_optimized_tga.translate(table=2))

cai_observations = {
    "biopython": Bio.__version__,
    "python": sys.version,
    "constructor_signature": str(inspect.signature(CodonAdaptationIndex)),
    "calculate_signature": str(inspect.signature(CodonAdaptationIndex.calculate)),
    "optimize_signature": str(inspect.signature(CodonAdaptationIndex.optimize)),
    "score_without_stop": score_no_stop,
    "score_with_unobserved_TAG": score_with_unobserved_stop,
    "unobserved_GCC_weight_when_GCT_seen_10x": unobserved_weight,
    "empty_query": empty_score,
    "excluded_only_ATG_TGG": excluded_score,
    "partial_query": partial_score,
    "strict_tie": strict_tie,
    "nonstrict_output": str(nonstrict_tie),
    "nonstrict_warnings": nonstrict_warnings,
    "table2_TGG_only": table2_tgg,
    "table2_optimize_TGA": str(table2_optimized_tga),
    "table2_input_translation": table2_input_protein,
    "table2_output_translation": table2_output_protein,
}
check("biopython-is-1.85", Bio.__version__ == "1.85", Bio.__version__)
check("stop-codon-contributes-to-cai", score_with_unobserved_stop < score_no_stop, [score_no_stop, score_with_unobserved_stop])
check("pseudocount-is-family-normalized", math.isclose(unobserved_weight, 0.05), unobserved_weight)
check("empty-query-raises-zero-division", empty_score["type"] == "ZeroDivisionError", empty_score)
check("atg-tgg-only-raises-zero-division", excluded_score["type"] == "ZeroDivisionError", excluded_score)
check("partial-query-raises-type-error", partial_score["type"] == "TypeError", partial_score)
check("strict-tie-raises-value-error", strict_tie["type"] == "ValueError", strict_tie)
check("nonstrict-tie-emits-no-warning", not nonstrict_warnings, nonstrict_warnings)
check("table2-tgg-is-hard-excluded", table2_tgg["type"] == "ZeroDivisionError", table2_tgg)
check("table2-optimization-breaks-protein", table2_input_protein != table2_output_protein, [table2_input_protein, table2_output_protein, str(table2_optimized_tga)])


# Execute the exact documented simplified Nc helper and compare to codonW.
metrics_text = (CANDIDATE / "references/metrics-and-methods.md").read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", metrics_text, flags=re.DOTALL)
nc_block = next(block for block in blocks if "def effective_nc" in block)
nc_namespace = {"CodonTable": CodonTable, "count_codons": count_codons}
exec(compile(nc_block, "metrics-and-methods.md:effective_nc", "exec"), nc_namespace)
effective_nc = nc_namespace["effective_nc"]


def read_fasta(path: Path) -> str:
    return "".join(line.strip() for line in path.read_text(encoding="ascii").splitlines() if not line.startswith(">"))


fixture_sources = {
    "heterogeneous": TOOLING / "fixtures/nc-heterogeneous.fasta",
    "public_thra": TOOLING / "fixtures/NC_000913.3_337-2799_thrA.fasta",
}
nc_results = {}
for label, source in fixture_sources.items():
    sequence = read_fasta(source)
    input_path = INPUTS / f"nc-{label}.fasta"
    input_path.write_text(f">{label}\n{sequence}\n", encoding="ascii")
    output_path = OUTPUTS / f"nc-{label}.out"
    bulk_path = OUTPUTS / f"nc-{label}.blk"
    local_input = OUTPUTS / f"nc-{label}.fasta"
    local_input.write_bytes(input_path.read_bytes())
    for stale in (output_path, bulk_path):
        if stale.exists():
            stale.unlink()
    command = [
        str(CODONW), local_input.name, output_path.name, bulk_path.name,
        "-nomenu", "-silent", "-nowarn", "-machine", "-enc", "-noblk",
    ]
    completed = subprocess.run(command, cwd=OUTPUTS, text=True, capture_output=True, timeout=30, check=False)
    output_text = output_path.read_text(encoding="utf-8", errors="replace") if output_path.exists() else ""
    match = re.search(r"\n\S+\s+([0-9.]+)\s*", output_text)
    codonw_nc = float(match.group(1)) if match else None
    nc_results[label] = {
        "sequence_length": len(sequence),
        "sequence_sha256": sha256_bytes(sequence.encode()),
        "simplified_nc": effective_nc(sequence),
        "codonw_nc": codonw_nc,
        "codonw_returncode": completed.returncode,
        "codonw_stdout": completed.stdout,
        "codonw_stderr": completed.stderr,
        "codonw_command": command,
    }
check("codonw-heterogeneous-exit-zero", nc_results["heterogeneous"]["codonw_returncode"] == 0, nc_results["heterogeneous"]["codonw_returncode"])
check("codonw-public-thra-exit-zero", nc_results["public_thra"]["codonw_returncode"] == 0, nc_results["public_thra"]["codonw_returncode"])
check("heterogeneous-nc-diverges-materially", abs(nc_results["heterogeneous"]["simplified_nc"] - nc_results["heterogeneous"]["codonw_nc"]) > 10, nc_results["heterogeneous"])
check("public-thra-nc-is-close-but-not-equal", 1 < abs(nc_results["public_thra"]["simplified_nc"] - nc_results["public_thra"]["codonw_nc"]) < 2, nc_results["public_thra"])


result = {
    "candidate": str(CANDIDATE),
    "candidate_identity": identity,
    "environment_prefix": sys.prefix,
    "checks_passed": sum(item["passed"] for item in checks),
    "checks_total": len(checks),
    "checks": checks,
    "standalone": first_runs,
    "boundary": boundary,
    "cai": cai_observations,
    "nc": nc_results,
    "environment_lock_sha256": sha256_bytes((TOOLING / "environment-explicit.lock").read_bytes()),
}
(EVIDENCE / "audit-results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
(EVIDENCE / "audit-transcript.txt").write_text(
    "\n".join(
        [
            f"candidate={CANDIDATE}",
            f"identity={identity}",
            f"python={sys.version.split()[0]}",
            f"biopython={Bio.__version__}",
            f"checks={result['checks_passed']}/{result['checks_total']}",
        ]
        + [f"{'PASS' if item['passed'] else 'FAIL'} {item['name']}: {item['detail']}" for item in checks]
    )
    + "\n",
    encoding="utf-8",
)
print(json.dumps({"checks_passed": result["checks_passed"], "checks_total": result["checks_total"], "identity": identity}))
if result["checks_passed"] != result["checks_total"]:
    raise SystemExit(1)
