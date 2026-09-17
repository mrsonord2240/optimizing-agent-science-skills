"""
Input 4 (Variant B) -- POST-FIX regression test, bio-crispr-screens-batch-correction.

Real request simulated: "I have a 2-batch HAP1 screen with vehicle/treatment arms
in each batch. Add batch as a covariate to my MAGeCK MLE design matrix instead of
pre-correcting, and tell me if the treatment beta still recovers known essential
genes."

Regression target: this pattern was already clean pre-fix; the only SKILL.md
change here is a P2 doc fix (added `--permutation-round 10` to the documented
`mageck mle` invocation and a new Reproducibility paragraph). This re-run uses
the CURRENT documented command verbatim, including the new flag, to confirm it
is a real, accepted mageck 0.5.9.5 option (not just plausible-looking text).
"""
import subprocess
import sys
from pathlib import Path

RUN = Path(r"F:\OpenScience\audits\bio-crispr-screens-batch-correction\run")
PYTHON = r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe"
MAGECK = r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"

# Reuse the already-generated Input 4 data (make_input4_subset.py), which is
# independent of the SKILL.md text change and was not affected by any fix.
counts = RUN / "input4_mle_counts.txt"
design = RUN / "input4_design.txt"
assert counts.exists() and design.exists(), "run make_input4_subset.py first"

# === Current (post-fix) SKILL.md command, VERBATIM, including the new flag ===
cmd = [
    PYTHON, MAGECK, "mle",
    "--count-table", str(counts),
    "--design-matrix", str(design),
    "--permutation-round", "10",
    "--output-prefix", str(RUN / "input4_batch_mle_postfix"),
]
print("Running:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT (tail):\n", result.stdout[-2000:])
print("STDERR (tail):\n", result.stderr[-3000:])
print("Return code:", result.returncode)
assert result.returncode == 0, "mageck mle with --permutation-round 10 must succeed (documented flag)"

# Confirm --permutation-round is a real, recognized flag (not silently ignored) by
# comparing against --help's own listing.
help_result = subprocess.run([PYTHON, MAGECK, "mle", "--help"], capture_output=True, text=True)
assert "--permutation-round" in help_result.stdout, "flag must appear in mageck mle --help"
print("\nConfirmed: --permutation-round is a real, documented mageck mle 0.5.9.5 flag "
      "(present in `mageck mle --help`), not a plausible-looking invention.")
