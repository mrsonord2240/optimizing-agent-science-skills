"""Fresh Phase-2 synthetic fixture for the shipped cS2G lookup wrapper."""
from __future__ import annotations

import gzip
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

audit = Path(r"F:\OpenScience\audits\bio-causal-genomics-effector-gene-prioritization")
script = audit / "run" / "skill_copy" / "examples" / "cs2g_lookup.py"
outdir = audit / "run" / "outputs" / "input10_cs2g"
outdir.mkdir(parents=True, exist_ok=True)
archive = outdir / "cS2G_fixture.zip"

rows = (
    "SNP\tGENE\tcS2G\tINFO\n"
    "rsA\tPCSK9\t0.8\tABC\n"
    "rsA\tLDLR\t0.2\tPromoter\n"
    "rsB\tPCSK9\t0.4\teQTLGen_Finemapped\n"
)
with tempfile.TemporaryDirectory() as td:
    gz = Path(td) / "cS2G.1.SGscore.gz"
    with gzip.open(gz, "wt", encoding="utf-8") as fh:
        fh.write(rows)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(gz, "cS2G_fixture/cS2G.1.SGscore.gz")

proc = subprocess.run(
    [sys.executable, str(script), str(archive), "1", "rsA", "rsB", "rsMissing"],
    check=True, text=True, capture_output=True,
)
(outdir / "input10_cs2g_stdout.txt").write_text(proc.stdout, encoding="utf-8")
(outdir / "input10_cs2g_stderr.txt").write_text(proc.stderr, encoding="utf-8")
assert "PCSK9\t1.2" in proc.stdout, proc.stdout
assert "LDLR\t0.2" in proc.stdout, proc.stdout
assert "rsMissing" in proc.stderr, proc.stderr
print("ASSERTIONS PASS: fixture parsed; PCSK9 aggregates to 1.2, LDLR to 0.2, and missing rsID is reported.")
