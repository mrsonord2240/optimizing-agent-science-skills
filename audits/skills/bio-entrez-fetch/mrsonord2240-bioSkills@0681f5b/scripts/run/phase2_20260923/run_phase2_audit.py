"""Execute the source Skill's documented Entrez paths from an audit-owned copy."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

AUDIT_ROOT = Path(r"F:\OpenScience\audits\bio-entrez-fetch")
SOURCE = Path(r"F:\OpenScience\wt\entrez-fetch\database-access\entrez-fetch")
WORK = AUDIT_ROOT / "run" / "phase2_20260923"
COPIED = WORK / "copied_source"
OUTPUT = WORK / "outputs"
PYTHON = AUDIT_ROOT / "private_runtime" / "venv" / "Scripts" / "python.exe"


def copy_source() -> None:
    if COPIED.exists():
        shutil.rmtree(COPIED)
    shutil.copytree(SOURCE, COPIED, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def run(name: str, arguments: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        [str(PYTHON), *arguments],
        cwd=COPIED,
        capture_output=True,
        timeout=300,
        check=False,
    )
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    (OUTPUT / f"{name}.stdout.txt").write_text(stdout, encoding="utf-8")
    (OUTPUT / f"{name}.stderr.txt").write_text(stderr, encoding="utf-8")
    return {"exit_code": completed.returncode, "stdout": stdout, "stderr": stderr}


def require(result: dict[str, object], name: str, expected: list[str]) -> None:
    if result["exit_code"] != 0:
        raise RuntimeError(f"{name} exited {result['exit_code']}: {result['stderr']}")
    text = str(result["stdout"])
    missing = [needle for needle in expected if needle not in text]
    if missing:
        raise RuntimeError(f"{name} missing expected output: {missing}")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    copy_source()
    results: dict[str, object] = {}
    results["input1_genbank"] = run("input1_genbank", ["examples/fetch_sequences.py"])
    require(results["input1_genbank"], "input1_genbank", ["Accession: NM_007294.4", "Length: 7088 nt", "CDS features: 1", "CDS-translated proteins:"])
    results["input2_summaries"] = run("input2_summaries", ["examples/fetch_summaries.py"])
    require(results["input2_summaries"], "input2_summaries", ["NM_007294.4", "PubMed docsum", "EFetch / ESummary:"])
    results["input3_pubmed"] = run("input3_pubmed", ["examples/fetch_pubmed.py"])
    require(results["input3_pubmed"], "input3_pubmed", ["MEDLINE format", "XML format", "PMC ID:"])
    results["input4_clinvar"] = run("input4_clinvar", ["scripts/variant_records.py", "--email", "audit@example.org", "--db", "clinvar", "--uid", "4887763"])
    require(results["input4_clinvar"], "input4_clinvar", ["VCV000005107", "Pathogenic"])
    results["input5_snp"] = run("input5_snp", ["scripts/variant_records.py", "--email", "audit@example.org", "--db", "snp", "--uid", "429358"])
    require(results["input5_snp"], "input5_snp", ["'chr': '19'", "'gene': 'APOE'"])
    history_out = OUTPUT / "history_small.fasta"
    results["input6_history"] = run("input6_history", ["scripts/history_fetch.py", "--email", "audit@example.org", "--term", "NM_007294.4[ACCN]", "--out", str(history_out), "--chunk", "4"])
    require(results["input6_history"], "input6_history", ["1 records requested"])
    if not history_out.read_text(encoding="utf-8").startswith(">NM_007294.4"):
        raise RuntimeError("input6_history did not write the expected version-pinned BRCA1 FASTA")
    results["input7_refs"] = run("input7_refs", [str(WORK / "phase2_inline_refs.py")])
    require(results["input7_refs"], "input7_refs", ["ERROR_GUARD PASS", "SRA_ROWS", "SRR000001", "LINEAGE Homo sapiens"])
    summary = {name: {"exit_code": value["exit_code"]} for name, value in results.items()}
    (OUTPUT / "execution_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
