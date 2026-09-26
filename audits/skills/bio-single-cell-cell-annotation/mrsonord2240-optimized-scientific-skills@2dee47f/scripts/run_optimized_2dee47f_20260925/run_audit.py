"""Execute all seven re-audit cases and persist complete stdout/stderr logs."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
RUN = ROOT / "run"
PYTHON = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\Scripts\python.exe")
GIT_BASH = Path(r"C:\Program Files\Git\bin\bash.exe")
RS = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/tools/rs.sh"
SOURCE_EXAMPLE = Path(r"F:\OpenScience\audit-sources\optimized-scientific-skills-2dee47f\skills\bio-single-cell-cell-annotation\examples\celltypist_annotation.py")
MODEL_LOW = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")


def run_case(name: str, commands: list[list[str]], nonzero_success_marker: str | None = None) -> None:
    chunks: list[str] = []
    for command in commands:
        chunks.append("COMMAND: " + subprocess.list2cmdline(command))
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        chunks.append(f"EXIT_CODE: {completed.returncode}")
        chunks.append("STDOUT:\n" + completed.stdout)
        chunks.append("STDERR:\n" + completed.stderr)
        marker_ok = nonzero_success_marker is not None and nonzero_success_marker in completed.stdout
        if completed.returncode != 0 and not marker_ok:
            (RUN / f"{name}.log").write_text("\n".join(chunks), encoding="utf-8")
            raise SystemExit(f"{name} failed with exit {completed.returncode}")
        if completed.returncode != 0 and marker_ok:
            chunks.append(
                "AUDIT_NOTE: nonzero Windows process teardown accepted only because the checked "
                f"success marker was present: {nonzero_success_marker}"
            )
    (RUN / f"{name}.log").write_text("\n".join(chunks), encoding="utf-8")
    print(f"{name}: PASS")


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if start <= 1:
        run_case("input1", [
        [str(PYTHON), str(RUN / "input1_prepare.py")],
        [
            str(PYTHON), str(SOURCE_EXAMPLE),
            "--input", str(ROOT / "data" / "input1_clustered.h5ad"),
            "--model", str(MODEL_LOW),
            "--output", str(ROOT / "data" / "input1_annotated.h5ad"),
            "--figure", str(ROOT / "data" / "input1_annotation.png"),
            "--counts-output", str(ROOT / "data" / "input1_counts.csv"),
        ],
        [str(PYTHON), str(RUN / "input1_validate.py")],
        ])
    if start <= 2:
        run_case(
            "input2",
            [[str(GIT_BASH), RS, str(RUN / "input2.R").replace("\\", "/")]],
            nonzero_success_marker="SingleR regression PASS",
        )
    if start <= 3:
        run_case("input3", [[str(PYTHON), str(RUN / "input3.py")]])
    if start <= 4:
        run_case(
            "input4",
            [[str(GIT_BASH), RS, str(RUN / "input4.R").replace("\\", "/")]],
            nonzero_success_marker="normalized_marker_validation=PASS",
        )
    if start <= 5:
        run_case("input5", [[str(PYTHON), str(RUN / "input5.py")]])
    if start <= 6:
        run_case("input6", [[str(PYTHON), str(RUN / "input6.py")]])
    if start <= 7:
        run_case("input7", [[str(PYTHON), str(RUN / "input7.py")]])


if __name__ == "__main__":
    main()
