"""Re-run archived DIA assertions against the final source worktree.

All generated reports here are SYNTHETIC unless their path says public-work.
"""
from __future__ import annotations

import os
import re
import runpy
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE = Path(r"F:\OpenScience\wt\bio-proteomics-dia-final")
AUDIT = Path(r"F:\OpenScience\audits\bio-proteomics-dia-analysis")
SKILL = SOURCE / "proteomics/dia-analysis/SKILL.md"
EXAMPLE = SOURCE / "proteomics/dia-analysis/examples/diann_analysis.sh"
FIXTURE = SOURCE / "proteomics/dia-analysis/examples/testdata"
PUBLIC = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\public-work\diann_predlib_mzml\diann_out\report.parquet")


def filter_source() -> str:
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(r"```python\n(import pandas as pd, numpy as np.*?pg = np\.log2\(pg\.replace\(0, np\.nan\)\).*?)\n```", text, re.S)
    assert match, "could not extract the canonical filter block"
    return match.group(1)


def run_filter(path: Path) -> pd.DataFrame:
    ns: dict[str, object] = {}
    code = filter_source().replace("'diann_out/report.parquet'", repr(str(path)))
    exec(compile(code, str(SKILL), "exec"), ns)
    return ns["pg"]  # type: ignore[return-value]


def check_fixture() -> None:
    subprocess.run(["python", str(FIXTURE / "make_synthetic_report.py")], check=True)
    pg = run_filter(FIXTURE / "synthetic_report.parquet")
    assert pg.shape == (2, 2), pg.shape
    assert "LOWCONF_GLOBAL_ONLY" not in pg.index
    assert not np.isinf(pg.to_numpy(dtype=float)).any()
    assert pd.isna(pg.loc["P002", "control"])
    print(f"FRESH fixture: PASS matrix={pg.shape}; globally-unconfident group excluded; zero->NaN")


def check_archived_report() -> None:
    raw = AUDIT / "data/report.parquet"
    report = pd.read_parquet(raw)
    pg = run_filter(raw)
    assert not any(pg.index.str.startswith("LOWCONF"))
    assert not np.isinf(pg.to_numpy(dtype=float)).any()
    print(f"ARCHIVED input 1: PASS rows={len(report)} matrix={pg.shape} LOWCONF=0")


def check_archived_public() -> None:
    report = pd.read_parquet(PUBLIC)
    pg = run_filter(PUBLIC)
    assert pg.shape == (4375, 3), pg.shape
    assert not np.isinf(pg.to_numpy(dtype=float)).any()
    log = PUBLIC.with_name("report.log.txt").read_text(encoding="utf-8")
    assert "Protein groups matrix saved" in log
    matrix = pd.read_csv(PUBLIC.with_name("report.pg_matrix.tsv"), sep="\t")
    assert len(matrix) == 4440 and len(matrix) > len(pg)
    print(f"ARCHIVED input 6: PASS real DIA-NN 2.6.1 rows={len(report)} filtered={pg.shape}; pg_matrix=4440 > report filter=4375")


def check_stress() -> None:
    work = AUDIT / "run/finalpass_20260924/stress"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    old = Path.cwd()
    try:
        os.chdir(work)
        # Archived deterministic generator, but the filter is extracted from the exact final source.
        runpy.run_path(str(AUDIT / "runs/in5_make_cohort.py"), run_name="__main__")
        # The archived generator retains its historical output path under AUDIT/data.
        pq = AUDIT / "data/cohort600_report.parquet"
        pg = run_filter(pq)
        assert pg.shape == (2000, 600), pg.shape
        assert not any(pg.index.str.startswith("FALSE"))
        assert not np.isinf(pg.to_numpy(dtype=float)).any()
        print(f"ARCHIVED input 5: PASS synthetic 600-run matrix={pg.shape}; FALSE=0; -Inf=0")
    finally:
        os.chdir(old)
        (AUDIT / "data/cohort600_report.parquet").unlink(missing_ok=True)
        shutil.rmtree(work, ignore_errors=True)


def check_example() -> None:
    root = AUDIT / "run/finalpass_20260924/example_smoke"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    try:
        (root / "uniprot_human_reviewed.fasta").write_text(">P1\nPEPTIDE\n", encoding="utf-8")
        (root / "run A.mzML").touch()
        (root / "runB.mzML").touch()
        bindir = root / "bin"
        bindir.mkdir()
        stub = bindir / "diann"
        stub.write_text(
            "#!/usr/bin/env bash\n"
            "set -e\n"
            "n=0; [ -f .diann_calls ] && n=$(cat .diann_calls); n=$((n+1)); printf '%s' \"$n\" > .diann_calls\n"
            "printf '%s\\n' \"$@\" > \"call${n}.args\"\n"
            "if [ \"$n\" -eq 1 ]; then\n"
            "  [ \"$#\" -gt 0 ] && ! printf '%s\\n' \"$@\" | grep -qx -- '--f'\n"
            "  mkdir -p diann_out; : > diann_out/human.predicted.speclib\n"
            "else\n"
            "  [ \"$(printf '%s\\n' \"$@\" | grep -cx -- '--f')\" -eq 2 ]\n"
            "  ! printf '%s\\n' \"$@\" | grep -Eq -- '^--fasta-search$|^--predictor$'\n"
            "fi\n",
            encoding="utf-8", newline="\n",
        )
        stub.chmod(0o755)
        def bash_path(path: Path) -> str:
            return "/mnt/" + path.drive[0].lower() + path.as_posix()[2:]

        command = f"export PATH='{bash_path(bindir)}':$PATH; exec bash '{bash_path(EXAMPLE)}'"
        done = subprocess.run(["bash", "-lc", command], cwd=root, text=True, capture_output=True)
        assert done.returncode == 0, done.stdout + done.stderr
        assert (root / "call1.args").exists() and (root / "call2.args").exists()
        assert "run A.mzML" in (root / "call2.args").read_text(encoding="utf-8")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("FRESH example smoke: PASS two DIA-NN calls; Stage 1 has no raw files; Stage 2 preserves spaced mzML name")


def check_docs() -> None:
    text = SKILL.read_text(encoding="utf-8")
    usage = (SOURCE / "proteomics/dia-analysis/usage-guide.md").read_text(encoding="utf-8")
    assert "matrix count < report count is expected" not in text + usage
    for phrase in ("FragmentCharge", "FragmentType", "FragmentSeriesNumber", "report.log.txt", "separate pipeline step"):
        assert phrase in text
    assert "diann \\\n+    --f sample1.mzML" not in text
    print("FRESH static fences: PASS P1/P2 corrections and single-source command")


if __name__ == "__main__":
    check_docs()
    check_fixture()
    check_archived_report()
    check_archived_public()
    check_stress()
    check_example()
    print("FINAL SOURCE VERIFICATION: PASS")
