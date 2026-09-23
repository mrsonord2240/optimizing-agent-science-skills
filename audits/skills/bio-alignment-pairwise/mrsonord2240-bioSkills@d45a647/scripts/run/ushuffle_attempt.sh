#!/bin/bash
# Skill: "for DNA, use the dinucleotide shuffle of Altschul & Erickson 1985 via `ushuffle`" (no code shipped). Attempt to install into a scratch --target dir (no env change).
# Windows venv attempt: F:/OpenScience/audit-envs/alignment/Scripts/python.exe -m pip install --target <scratch> ushuffle  -> "Failed building wheel for ushuffle"
# WSL attempt (this script, run via wsl_run.sh):
micromamba run -n alignment python -m pip install --target /tmp/us_target ushuffle 2>&1 | tail -4
micromamba run -n alignment env PYTHONPATH=/tmp/us_target python -c "import ushuffle; print(ushuffle.shuffle(b'ACGTACGTAGCTAGCTAGGATCC', 23, 2))" 2>&1 | tail -3
