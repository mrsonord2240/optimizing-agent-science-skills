#!/usr/bin/env python3
"""Independent final re-audit harness for bio-codon-usage.

This harness imports the exact candidate without modifying it, exercises every
shipped Python surface, probes the four repaired findings, and emits one JSON
object to stdout. It deliberately does not depend on the delta harness.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import warnings

from Bio import SeqIO
from Bio.Data import CodonTable
from Bio.Seq import Seq
from Bio.SeqUtils import CodonAdaptationIndex, GC123


CANDIDATE = Path("/mnt/openscience/wt/opt10-codon-usage/skills/bio-codon-usage")
SCRIPTS = CANDIDATE / "scripts"
TESTS = CANDIDATE / "tests" / "test_codon_usage.py"
FIXTURES = Path("/mnt/openscience/audit-envs/bio-codon-usage/fixtures")
PYTHON = Path("/mnt/openscience/audit-envs/bio-codon-usage/env/bin/python")
CODONW = Path("/mnt/openscience/audit-envs/bio-codon-usage/env/bin/codonw")

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
from codon_utils import (  # noqa: E402
    CAIScoringError,
    CDSValidationError,
    calculate_cai_guarded,
    codon_frequencies,
    count_codons,
    optimize_dna_table_aware,
    validate_cds,
)
from rscu_analysis import calculate_rscu  # noqa: E402


checks: list[dict[str, object]] = []


def check(group: str, name: str, passed: bool, detail: object) -> None:
    checks.append({"group": group, "name": name, "pass": bool(passed), "detail": detail})


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str], *, cwd: Path | None = None) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "cwd": str(cwd) if cwd else None,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "stdout_sha256": sha256_bytes(completed.stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(completed.stderr.encode("utf-8")),
    }


results: dict[str, object] = {
    "runtime": {
        "python": sys.version,
        "biopython": __import__("Bio").__version__,
        "candidate": str(CANDIDATE),
    },
    "checks": checks,
}


# Input 1: all shipped entrypoints, import-safety, candidate tests, and reruns.
script_runs: dict[str, object] = {}
for script_name in ("basic_analysis.py", "rscu_analysis.py", "cai_optimization.py"):
    first = run([str(PYTHON), str(SCRIPTS / script_name)])
    second = run([str(PYTHON), str(SCRIPTS / script_name)])
    script_runs[script_name] = {"first": first, "second": second}
    check("canonical", f"{script_name} first run exits zero", first["returncode"] == 0, first["returncode"])
    check("canonical", f"{script_name} second run exits zero", second["returncode"] == 0, second["returncode"])
    check("canonical", f"{script_name} stderr empty", first["stderr"] == second["stderr"] == "", first["stderr"])
    check(
        "determinism",
        f"{script_name} reruns are byte-identical",
        first["stdout_sha256"] == second["stdout_sha256"] and first["stderr_sha256"] == second["stderr_sha256"],
        {"first": first["stdout_sha256"], "second": second["stdout_sha256"]},
    )

    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        runpy.run_path(str(SCRIPTS / script_name), run_name="reaudit_import_probe")
    check("canonical", f"{script_name} is import-safe", stdout.getvalue() == stderr.getvalue() == "", {"stdout": stdout.getvalue(), "stderr": stderr.getvalue()})

test_first = run([str(PYTHON), str(TESTS)])
test_second = run([str(PYTHON), str(TESTS)])
check("canonical", "focused candidate tests pass twice", test_first["returncode"] == test_second["returncode"] == 0, {"first": test_first["returncode"], "second": test_second["returncode"]})
normalized_test_first = re.sub(r"Ran (\d+) tests in [0-9.]+s", r"Ran \1 tests in <elapsed>", test_first["stderr"])
normalized_test_second = re.sub(r"Ran (\d+) tests in [0-9.]+s", r"Ran \1 tests in <elapsed>", test_second["stderr"])
check("determinism", "focused test reruns have identical cases and outcomes", normalized_test_first == normalized_test_second and test_first["stdout"] == test_second["stdout"], {"first": normalized_test_first, "second": normalized_test_second})
check("canonical", "standard example reports CAI 1.000 and preserved protein", "Optimized CAI: 1.000" in script_runs["cai_optimization.py"]["first"]["stdout"] and "Protein preserved: MAALDDKG*" in script_runs["cai_optimization.py"]["first"]["stdout"], script_runs["cai_optimization.py"]["first"]["stdout"])
results["canonical"] = {"scripts": script_runs, "tests": {"first": test_first, "second": test_second}}


# Input 2: table-2 TGA/TGG x AGA/AGG preservation and table mismatch.
table2 = CodonTable.unambiguous_dna_by_id[2]
table2_index = CodonAdaptationIndex([Seq("ATGTGATGAAGA")], table=table2)
table2_cases: list[dict[str, object]] = []
for sense, stop in (("TGA", "AGA"), ("TGG", "AGG"), ("TGA", "AGG"), ("TGG", "AGA")):
    query = Seq(f"ATG{sense}{stop}")
    optimized, source_validation, optimized_validation = optimize_dna_table_aware(
        table2_index, query, table_id=2, strict=False
    )
    source_protein = str(query.translate(table=2))
    optimized_protein = str(optimized.translate(table=2))
    row = {
        "query": str(query),
        "optimized": str(optimized),
        "source_codons": list(source_validation.codons),
        "optimized_codons": list(optimized_validation.codons),
        "source_protein": source_protein,
        "optimized_protein": optimized_protein,
    }
    table2_cases.append(row)
    check("alternate_table", f"{sense}/{stop} preserves table-2 protein", source_protein == optimized_protein == "MW*", row)
    check("alternate_table", f"{sense}/{stop} retains a table-2 terminal stop", optimized_validation.codons[-1] in {"AGA", "AGG"}, row)

standard_index = CodonAdaptationIndex(
    [Seq("ATGGCTGCTGCTTAA"), Seq("ATGGCTGCTGCTTAA")],
    table=CodonTable.unambiguous_dna_by_id[1],
)
try:
    calculate_cai_guarded(standard_index, "ATGTGAAGA", table_id=2)
except ValueError as exc:
    mismatch_error = str(exc)
else:
    mismatch_error = None
check("alternate_table", "CAI table mismatch is rejected", mismatch_error is not None and "not constructed" in mismatch_error, mismatch_error)
results["alternate_table"] = {"cases": table2_cases, "mismatch_error": mismatch_error}


# Input 3: shared strict/permissive validator and exact discard reports.
strict_cases = {
    "empty": "",
    "partial": "ATGAA",
    "shifted": "AATGCTTAA",
    "ambiguous": "ATGNNNTAA",
    "internal_stop": "ATGTAAGCTTAA",
    "whitespace": "ATG GCT TAA",
}
strict_results: dict[str, object] = {}
for label, sequence in strict_cases.items():
    try:
        validate_cds(sequence, table_id=1, policy="strict")
    except CDSValidationError as exc:
        strict_results[label] = str(exc)
    else:
        strict_results[label] = None
    check("validation", f"strict validator rejects {label}", strict_results[label] is not None, strict_results[label])

permissive_sequence = "ATGNNNGCTTAAAA"
permissive = validate_cds(permissive_sequence, table_id=1, policy="permissive")
discard_rows = [
    {"offset": item.offset, "text": item.text, "reason": item.reason}
    for item in permissive.discarded
]
expected_discards = [
    {"offset": 3, "text": "NNN", "reason": "codon contains non-ACGT symbols"},
    {"offset": 12, "text": "AA", "reason": "incomplete trailing codon"},
]
check("validation", "permissive validator retains exact in-frame CDS", permissive.sequence == "ATGGCTTAA", permissive.sequence)
check("validation", "permissive validator reports exact discards", discard_rows == expected_discards, discard_rows)

count_result, count_validation = count_codons(permissive_sequence, table_id=1, policy="permissive")
frequency_result, frequency_validation = codon_frequencies(permissive_sequence, table_id=1, policy="permissive")
rscu_result, rscu_validation = calculate_rscu(permissive_sequence, table_id=1, policy="permissive")
check("validation", "counts frequencies and RSCU share validator state", count_validation == frequency_validation == rscu_validation == permissive, {"codons": list(permissive.codons)})
check("validation", "permissive counts are exact", dict(count_result) == {"ATG": 1, "GCT": 1, "TAA": 1}, dict(count_result))
check("validation", "permissive frequencies sum to one", abs(sum(frequency_result.values()) - 1.0) < 1e-12, frequency_result)
check("validation", "RSCU alanine family preserves expected sum", abs(sum(rscu_result[c] for c in ("GCT", "GCC", "GCA", "GCG")) - 4.0) < 1e-12, {c: rscu_result[c] for c in ("GCT", "GCC", "GCA", "GCG")})
results["validation"] = {
    "strict": strict_results,
    "permissive": {
        "sequence": permissive.sequence,
        "codons": list(permissive.codons),
        "discarded": discard_rows,
        "discard_summary": permissive.discard_summary(),
        "counts": dict(count_result),
        "frequencies": frequency_result,
        "rscu_alanine": {c: rscu_result[c] for c in ("GCT", "GCC", "GCA", "GCG")},
    },
}


# Input 4: exact Biopython 1.85 behavior, guard semantics, standard optimization.
stop_index = CodonAdaptationIndex([Seq("ATGGCTTAAGCTTAA")])
stop_with = stop_index.calculate(Seq("GCTTAG"))
stop_without = stop_index.calculate(Seq("GCT"))
pseudocount_weight = CodonAdaptationIndex([Seq("GCT" * 10)])["GCC"]
tie_index = CodonAdaptationIndex([Seq("GCTGCCGCAGCG")])
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    tie_index.optimize(Seq("GCT"), strict=False)
strict_tie_error = None
try:
    tie_index.optimize(Seq("GCT"), strict=True)
except ValueError as exc:
    strict_tie_error = str(exc)

zero_guard_error = None
try:
    calculate_cai_guarded(
        standard_index,
        "ATGTGG",
        table_id=1,
        require_terminal_stop=False,
    )
except CAIScoringError as exc:
    zero_guard_error = str(exc)

guarded = calculate_cai_guarded(standard_index, "ATGGCTTAA", table_id=1)
standard_query = Seq("ATGGCAGCATTAGATGATAAAGGATAA")
standard_optimized, _, _ = optimize_dna_table_aware(
    CodonAdaptationIndex(
        [
            Seq("ATGGCTGCTGCTCTGCTGCTGGACGACAAAAAAGGTGGTGCTCTGGACAAAGGTGCTTAA"),
            Seq("ATGGCTCTGCTGGACAAAGGTGCTGCTCTGCTGGACGACAAAAAAGGTGGTGCTCTGTAA"),
            Seq("ATGCTGGCTGACGACAAAGGTGGTGCTGCTCTGCTGAAAAAAGACGGTGCTCTGGCTTAA"),
        ],
        table=CodonTable.unambiguous_dna_by_id[1],
    ),
    standard_query,
    table_id=1,
    strict=False,
)
check("biopython_semantics", "indexed stop contributes to Biopython CAI", stop_with < stop_without, {"with_stop": stop_with, "without_stop": stop_without})
check("biopython_semantics", "unobserved GCC normalizes to 0.05", abs(pseudocount_weight - 0.05) < 1e-12, pseudocount_weight)
check("biopython_semantics", "strict false emits no warning", len(caught) == 0, [str(item.message) for item in caught])
check("biopython_semantics", "strict true rejects a synonymous tie", strict_tie_error is not None, strict_tie_error)
check("biopython_semantics", "zero denominator is intercepted with actionable error", zero_guard_error is not None and "no included codons" in zero_guard_error and "0:ATG" in zero_guard_error and "1:TGG" in zero_guard_error, zero_guard_error)
check("biopython_semantics", "guard reports included and excluded codons", guarded.included_codons == 2 and guarded.excluded_codons[0][1] == "ATG", {"included": guarded.included_codons, "excluded": guarded.excluded_codons})
check("biopython_semantics", "standard max-CAI optimization preserves protein", standard_optimized.translate(table=1) == standard_query.translate(table=1) == Seq("MAALDDKG*"), {"query": str(standard_query), "optimized": str(standard_optimized), "protein": str(standard_optimized.translate(table=1))})
results["biopython_semantics"] = {
    "stop_with": stop_with,
    "stop_without": stop_without,
    "pseudocount_weight_gcc": pseudocount_weight,
    "strict_false_warnings": [str(item.message) for item in caught],
    "strict_true_error": strict_tie_error,
    "zero_guard_error": zero_guard_error,
    "guarded_score": guarded.score,
    "guarded_included": guarded.included_codons,
    "guarded_excluded": guarded.excluded_codons,
    "standard_query": str(standard_query),
    "standard_optimized": str(standard_optimized),
    "standard_protein": str(standard_optimized.translate(table=1)),
}


# Input 5: public table-11 CDS, fresh codonW controls, and Nc boundary.
public_record = next(SeqIO.parse(FIXTURES / "NC_000913.3_337-2799_thrA.fasta", "fasta"))
public_validation = validate_cds(public_record.seq, table_id=11, policy="strict")
public_counts, public_count_validation = count_codons(public_record.seq, table_id=11, policy="strict")
public_freqs, public_frequency_validation = codon_frequencies(public_record.seq, table_id=11, policy="strict")
public_rscu, public_rscu_validation = calculate_rscu(public_record.seq, table_id=11, policy="strict")
public_gc = GC123(Seq(public_validation.sequence))
check("public_control", "public thrA validates under table 11", len(public_validation.sequence) == 2463 and len(public_validation.codons) == 821 and public_validation.codons[0] == "ATG" and public_validation.codons[-1] == "TGA" and public_validation.discarded == (), {"length": len(public_validation.sequence), "codons": len(public_validation.codons), "first": public_validation.codons[0], "last": public_validation.codons[-1]})
check("public_control", "public analyses share exact validation state", public_validation == public_count_validation == public_frequency_validation == public_rscu_validation, public_validation.discard_summary())
check("public_control", "public counts and frequencies are complete", sum(public_counts.values()) == 821 and abs(sum(public_freqs.values()) - 1.0) < 1e-12, {"counts": sum(public_counts.values()), "frequency_sum": sum(public_freqs.values())})
check("public_control", "public RSCU and GC123 are finite", all(value >= 0 for value in public_rscu.values()) and all(0 <= value <= 100 for value in public_gc), {"rscu_size": len(public_rscu), "gc123": public_gc})

codonw_runs: dict[str, object] = {}
with tempfile.TemporaryDirectory(prefix="codon-reaudit-") as temp_name:
    temp = Path(temp_name)
    for label, source_name, expected in (
        ("heterogeneous", "nc-heterogeneous.fasta", "30.77"),
        ("public_thra", "nc-public-thrA.fasta", "47.41"),
    ):
        target = temp / source_name
        shutil.copyfile(FIXTURES / source_name, target)
        invocation = run(
            [str(CODONW), str(target), "-nomenu", "-silent", "-nowarn", "-machine", "-enc", "-noblk"],
            cwd=temp,
        )
        out_file = target.with_suffix(".out")
        out_text = out_file.read_text(encoding="utf-8", errors="replace") if out_file.exists() else ""
        codonw_runs[label] = {"invocation": invocation, "output": out_text, "output_sha256": sha256_bytes(out_text.encode("utf-8"))}
        check("external_nc_boundary", f"fresh codonW {label} exits zero", invocation["returncode"] == 0, invocation["returncode"])
        check("external_nc_boundary", f"fresh codonW {label} reproduces expected Nc", expected in out_text, out_text)

skill_text = (CANDIDATE / "SKILL.md").read_text(encoding="utf-8")
metrics_text = (CANDIDATE / "references" / "metrics-and-methods.md").read_text(encoding="utf-8")
all_candidate_text = "\n".join(
    path.read_text(encoding="utf-8")
    for path in CANDIDATE.rglob("*")
    if path.is_file() and path.suffix in {".md", ".py"}
)
candidate_script_text = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (CANDIDATE / "scripts").glob("*.py")
)
check("external_nc_boundary", "false standard-Nc implementation and trigger claim are absent", "def effective_nc" not in candidate_script_text and "RSCU, and Nc" not in skill_text, {"implementation_absent": "def effective_nc" not in candidate_script_text, "trigger_claim_absent": "RSCU, and Nc" not in skill_text})
check("external_nc_boundary", "SKILL explicitly says Nc is not calculated", "does not calculate Nc" in skill_text, "present" if "does not calculate Nc" in skill_text else "missing")
check("external_nc_boundary", "cross-study estimator boundary is explicit", "Do not compare the removed approximation across studies" in metrics_text and "record the exact estimator and version" in skill_text, "explicit")
results["public_and_external_boundary"] = {
    "public_thrA": {
        "id": public_record.id,
        "length": len(public_validation.sequence),
        "codons": len(public_validation.codons),
        "first": public_validation.codons[0],
        "last": public_validation.codons[-1],
        "discarded": discard_rows if False else [],
        "count_total": sum(public_counts.values()),
        "frequency_sum": sum(public_freqs.values()),
        "gc123": public_gc,
    },
    "codonw": codonw_runs,
    "nc_boundary": {
        "implementation_absent": "def effective_nc" not in candidate_script_text,
        "skill_disclaims_nc": "does not calculate Nc" in skill_text,
        "cross_study_boundary": "Do not compare the removed approximation across studies" in metrics_text,
    },
}


passed = sum(1 for item in checks if item["pass"])
results["summary"] = {"passed": passed, "total": len(checks), "failed": [item for item in checks if not item["pass"]]}
print(json.dumps(results, indent=2, sort_keys=True, default=str))

