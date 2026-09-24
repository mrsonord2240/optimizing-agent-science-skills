from __future__ import annotations

import subprocess
import sys
from pathlib import Path


stage, rscript, ssg, database, sites, reader = map(Path, sys.argv[1:])
stage.mkdir(parents=True, exist_ok=True)
subprocess.run(
    [
        str(rscript), str(ssg / "ssgsea-cli.R"), "-i", str(sites),
        "-o", str(stage / "run"), "-d", str(database), "-z", str(ssg),
        "-n", "rank", "-w", "0.75", "-c", "z.score",
        "-t", "area.under.RES", "-s", "NES", "-p", "1000",
        "-m", "10", "-x", "TRUE", "-e", "FALSE", "-l", "FALSE",
    ],
    check=True,
)
subprocess.run(
    [sys.executable, str(reader), "read", "--prefix", str(stage / "run"),
     "--out", str(stage / "result.csv")],
    check=True,
)
