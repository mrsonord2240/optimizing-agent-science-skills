#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import tempfile
from pathlib import Path

CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
PYTHON = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python")


def hyb_row(read_id: str, mirna: str, target: str) -> str:
    first = [target, "23", "40", "101", "118", "2e-4"]
    second = [mirna, "1", "22", "1", "22", "1e-4"]
    return "\t".join([read_id, "ACGT" * 10, ".", *first, *second, ""]) + "\n"


with tempfile.TemporaryDirectory(prefix="ago-expression-audit2-") as temporary:
    root = Path(temporary)
    mirna = "MIMAT1_MirBase_miR-1_microRNA"
    run1, run2 = root / "run1.hyb", root / "run2.hyb"
    run1.write_text(hyb_row("nan-expression", mirna, "ENST1_gene_mRNA"), encoding="utf-8")
    run2.write_text(hyb_row("nan-expression", mirna, "ENST1_gene_mRNA"), encoding="utf-8")
    expression = root / "expression.tsv"
    expression.write_text(
        "mirna_id\texpression_value\texpression_unit\texpression_source\n"
        f"{mirna}\tNaN\tTPM\tmatched-small-rna\n", encoding="utf-8")
    outputs = {key: root / value for key, value in {
        "sites": "sites.tsv", "targets": "targets.tsv", "excluded": "excluded.tsv",
        "support": "support.tsv", "manifest": "manifest.json",
    }.items()}
    command = [str(PYTHON), str(CANDIDATE / "scripts/consensus_hyb.py"),
        "--hyb", str(run1), str(run2), "--sites", str(outputs["sites"]),
        "--targets", str(outputs["targets"]), "--excluded", str(outputs["excluded"]),
        "--support", str(outputs["support"]), "--manifest", str(outputs["manifest"]),
        "--reads", str(run1), "--expression", str(expression), "--expression-threshold", "100",
        "--hyb-commit", "028ab6371ce793ca5e86f475fce1f2cc6ad3c677", "--hyb-db", "fixture", "--run-id", "audit2-nan"]
    result = subprocess.run(command, text=True, capture_output=True)
    rows = list(csv.DictReader(outputs["sites"].open(encoding="utf-8"), delimiter="\t")) if outputs["sites"].exists() else []
    manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8")) if outputs["manifest"].exists() else {}
    finding_reproduced = result.returncode == 0 and len(rows) == 1 and rows[0]["expression_value"].lower() == "nan" and manifest.get("accepted_rows") == 1
    print(json.dumps({
        "threshold": 100, "expression_value": "NaN", "returncode": result.returncode,
        "accepted_rows": manifest.get("accepted_rows"), "site_expression_value": rows[0].get("expression_value") if rows else None,
        "stderr": result.stderr, "nan_bypasses_threshold": finding_reproduced,
    }, indent=2, sort_keys=True))
    assert finding_reproduced
