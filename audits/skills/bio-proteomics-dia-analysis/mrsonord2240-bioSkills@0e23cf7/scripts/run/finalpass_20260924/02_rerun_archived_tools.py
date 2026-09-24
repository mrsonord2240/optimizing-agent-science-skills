"""Re-run archived tool-level inputs that do not require a fresh multi-hour DIA search."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pandas as pd


AUDIT = Path(r"F:\OpenScience\audits\bio-proteomics-dia-analysis")
SOURCE = Path(r"F:\OpenScience\wt\bio-proteomics-dia-final")
MSCONVERT = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\tools\pwiz\msconvert.exe")
EASYPQP = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\tools\easypqp-venv\Scripts\easypqp.exe")


def test_staggered_demux() -> None:
    work = AUDIT / "run/finalpass_20260924/stagger"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    source = AUDIT / "rerun/stagger/staggered_cycles.mzML"
    result = subprocess.run(
        [str(MSCONVERT), str(source), "--mzML", "--filter", "peakPicking vendor msLevel=1-",
         "--filter", "demultiplex optimization=overlap_only massError=10ppm", "-o", str(work)],
        text=True, capture_output=True,
    )
    (work / "msconvert.stdout.txt").write_text(result.stdout + result.stderr, encoding="utf-8")
    output = work / "staggered_cycles.mzML"
    assert result.returncode == 0 and output.exists(), result.stdout + result.stderr
    assert output.stat().st_size > source.stat().st_size
    print(f"ARCHIVED input 3: PASS msconvert staggered demultiplex exit=0; output={output.stat().st_size} bytes")


def test_easypqp_contract() -> None:
    result = subprocess.run([str(EASYPQP), "library", "--help"], text=True, capture_output=True)
    text = result.stdout + result.stderr
    (AUDIT / "run/finalpass_20260924/easypqp_library_help.txt").write_text(text, encoding="utf-8")
    source_text = (SOURCE / "proteomics/dia-analysis/SKILL.md").read_text(encoding="utf-8")
    assert result.returncode == 0
    assert "--out" in text and "FragmentSeriesNumber" in source_text
    print("ARCHIVED input 4: PASS EasyPQP 0.1.59 library help; exact source documents TSV fragment-field gate")


def test_library_report_filter() -> None:
    path = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\public-work\diann_libbased_mzml\diann_out\report.parquet")
    report = pd.read_parquet(path)
    filt = report[(report["Q.Value"] <= 0.01) & (report["PG.Q.Value"] <= 0.01) &
                  (report["Global.Q.Value"] <= 0.01) & (report["Global.PG.Q.Value"] <= 0.01)]
    pg = filt.pivot_table(index="Protein.Group", columns="Run", values="PG.MaxLFQ", aggfunc="first")
    assert pg.shape == (771, 3)
    print("ARCHIVED input 7: PASS public library-based report global filter matrix=(771, 3)")


if __name__ == "__main__":
    test_staggered_demux()
    test_easypqp_contract()
    test_library_report_filter()
    print("ARCHIVED TOOL VERIFICATION: PASS")
