#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
PYTHON = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python")


def run(*args: object, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(arg) for arg in args], text=True, capture_output=True, check=check, env=env)


def hyb_row(read_id: str, first: str, second: str) -> str:
    a = [first, "1", "22", "1", "22", "1e-4"]
    b = [second, "23", "40", "101", "118", "2e-4"]
    return "\t".join([read_id, "ACGT" * 10, ".", *a, *b, ""]) + "\n"


checks: list[dict[str, object]] = []


def record(name: str, passed: bool, detail: object) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    mirna = "MIMAT1_MirBase_miR-1_microRNA"
    target1 = "ENST1_gene_mRNA"
    target2 = "ENST2_gene_mRNA"
    r1 = root / "r1.hyb"
    r2 = root / "r2.hyb"
    r1.write_text(
        hyb_row("stable_target_first", target1, mirna)
        + hyb_row("stable_mirna_first", mirna, target1)
        + hyb_row("unstable", target1, mirna)
        + hyb_row("missing", target1, mirna),
        encoding="utf-8",
    )
    r2.write_text(
        hyb_row("stable_target_first", target1, mirna)
        + hyb_row("stable_mirna_first", mirna, target1)
        + hyb_row("unstable", target2, mirna),
        encoding="utf-8",
    )
    expression = root / "expression.tsv"
    expression.write_text(
        "mirna_id\texpression_value\texpression_unit\texpression_source\n"
        f"{mirna}\t150\tTPM\tmatched-small-rna\n",
        encoding="utf-8",
    )
    outputs = {name: root / name for name in ("sites.tsv", "targets.tsv", "excluded.tsv", "support.tsv", "manifest.json")}
    run(
        PYTHON,
        CANDIDATE / "scripts/consensus_hyb.py",
        "--hyb", r1, r2,
        "--sites", outputs["sites.tsv"],
        "--targets", outputs["targets.tsv"],
        "--excluded", outputs["excluded.tsv"],
        "--support", outputs["support.tsv"],
        "--manifest", outputs["manifest.json"],
        "--reads", r1,
        "--expression", expression,
        "--expression-threshold", "100",
        "--hyb-commit", "028ab6371ce793ca5e86f475fce1f2cc6ad3c677",
        "--hyb-db", "fixture",
        "--run-id", "reaudit",
    )
    sites = list(csv.DictReader(outputs["sites.tsv"].open(encoding="utf-8"), delimiter="\t"))
    excluded = list(csv.DictReader(outputs["excluded.tsv"].open(encoding="utf-8"), delimiter="\t"))
    manifest = json.loads(outputs["manifest.json"].read_text(encoding="utf-8"))
    record("orientation-aware 16-column parsing", [x["source_orientation"] for x in sites] == ["mirna-first", "target-first"], sites)
    record("expression provenance retained", all(x["expression_source"] == "matched-small-rna" and x["expression_unit"] == "TPM" for x in sites), sites)
    reasons = {x["read_id"]: x["reason"] for x in excluded}
    record("ambiguity reason codes", reasons == {"missing": "missing_from_replicate", "unstable": "unstable_assignment"}, reasons)
    record("structured counts reconcile", manifest["accepted_rows"] == 2 and manifest["excluded_rows"] == 2 and manifest["target_rows"] == 1, manifest)

    bad = root / "bad.hyb"
    bad.write_text("id\tseq\t.\n", encoding="utf-8")
    result = run(
        PYTHON, CANDIDATE / "scripts/consensus_hyb.py",
        "--hyb", bad, bad,
        "--sites", root / "bad-sites", "--targets", root / "bad-targets",
        "--excluded", root / "bad-excluded", "--support", root / "bad-support", "--manifest", root / "bad-manifest",
        "--reads", bad, "--hyb-commit", "x", "--hyb-db", "x", "--run-id", "x",
        check=False,
    )
    record("wrong schema fails closed", result.returncode != 0 and "expected 16" in result.stderr, {"returncode": result.returncode, "stderr_tail": result.stderr[-240:]})

    bad_expression = root / "bad-expression.tsv"
    bad_expression.write_text("mirna_id\texpression_value\nfoo\t1\n", encoding="utf-8")
    result = run(
        PYTHON, CANDIDATE / "scripts/consensus_hyb.py",
        "--hyb", r1, r2,
        "--sites", root / "x-sites", "--targets", root / "x-targets",
        "--excluded", root / "x-excluded", "--support", root / "x-support", "--manifest", root / "x-manifest",
        "--reads", r1, "--expression", bad_expression, "--expression-threshold", "1",
        "--hyb-commit", "x", "--hyb-db", "x", "--run-id", "x", check=False,
    )
    record("expression schema fails closed", result.returncode != 0 and "expression header" in result.stderr, {"returncode": result.returncode, "stderr_tail": result.stderr[-240:]})

    hyb_home = root / "hyb home"
    db = hyb_home / "data/db"
    db.mkdir(parents=True)
    (db / "fixture.1.bt2").write_text("index", encoding="utf-8")
    reads = root / "reads * literal.fastq"
    reads.write_text("@r\nACGT\n+\nIIII\n", encoding="utf-8")
    fake = root / "fake hyb"
    fake.write_text(
        "#!/usr/bin/env bash\nset -euo pipefail\nid=; db=\n"
        "for arg in \"$@\"; do case \"$arg\" in id=*) id=${arg#id=};; db=*) db=${arg#db=};; esac; done\n"
        f"printf '%s' '{hyb_row('stable', target1, mirna)}' > \"${{id}}_comp_${{db}}_hybrids_ua.hyb\"\n",
        encoding="utf-8",
    )
    fake.chmod(0o755)
    output = root / "output with spaces"
    env = dict(os.environ)
    env["HYB_HOME"] = str(hyb_home)
    first = run("bash", CANDIDATE / "scripts/run_chimeric_eclip.sh", "--reads", reads, "--hyb-db", "fixture", "--run-id", "safe", "--output-dir", output, "--hyb-bin", fake, env=env)
    record("wrapper quotes paths and publishes complete output", first.returncode == 0 and (output / "manifest.json").is_file(), first.stdout)
    again = run("bash", CANDIDATE / "scripts/run_chimeric_eclip.sh", "--reads", reads, "--hyb-db", "fixture", "--run-id", "safe", "--output-dir", output, "--hyb-bin", fake, check=False, env=env)
    record("existing output refused", again.returncode == 73 and (output / "manifest.json").is_file(), {"returncode": again.returncode, "stderr": again.stderr})

    failing = root / "failing hyb"
    failing.write_text("#!/usr/bin/env bash\necho controlled-failure >&2\nexit 42\n", encoding="utf-8")
    failing.chmod(0o755)
    sentinel = output / "sentinel.txt"
    sentinel.write_text("preserve", encoding="utf-8")
    failed = run("bash", CANDIDATE / "scripts/run_chimeric_eclip.sh", "--reads", reads, "--hyb-db", "fixture", "--run-id", "safe", "--output-dir", output, "--hyb-bin", failing, "--replace", check=False, env=env)
    residue = list(root.glob(".output with spaces.stage.*"))
    record("failed replace propagates status and preserves prior output", failed.returncode == 42 and sentinel.read_text(encoding="utf-8") == "preserve" and not residue, {"returncode": failed.returncode, "residue": [str(x) for x in residue]})

summary = {
    "assertions_passed": sum(bool(x["passed"]) for x in checks),
    "assertions_total": len(checks),
    "checks": checks,
}
(ROOT / "evidence/contract-results.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2, sort_keys=True))

