"""Show MAGeCK's required three-column --list-seq contract for the P2 finding."""
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
bad = RUN / "two_column_library.csv"
bad.write_text("id,sequence\ncount_g1,ACGTACGTACGTACGTACGA\n", encoding="ascii")
mageck = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck")
result = subprocess.run(
    [sys.executable, str(mageck), "count", "--list-seq", str(bad), "--sample-label", "Bad", "--fastq", str(RUN / "S1.fastq"), "--output-prefix", "two_column_run"],
    cwd=RUN,
    text=True,
    capture_output=True,
)
(RUN / "two_column_count.stdout.log").write_text(result.stdout, encoding="utf-8")
(RUN / "two_column_count.stderr.log").write_text(result.stderr, encoding="utf-8")
assert result.returncode != 0, "two-column library unexpectedly succeeded"
assert not (RUN / "two_column_run.count.txt").exists(), "invalid library unexpectedly produced a count table"
print(f"two_column_library_rejected=true; returncode={result.returncode}")
