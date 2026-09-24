#!/bin/bash
# Final-pass fresh input 8: exercise the source-tip order-check code on real,
# shuffled, uBAM, and CRAM inputs, plus the clarified -T/-@ behavior.
set -euo pipefail
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
ROOT=/mnt/openscience/audits/bio-alignment-sorting/run
SOURCE=/mnt/openscience/worktrees/bio-alignment-sorting-finalpass/alignment-files/alignment-sorting/SKILL.md
DATA=/mnt/openscience/audit-envs/alignment-files/public-data
WORK=$ROOT/work/finalpass_in08
rm -rf "$WORK"
mkdir -p "$WORK/tmpdir"
cd "$WORK"

python - "$SOURCE" <<'PY'
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
start = text.index("### Check Sort Order in pysam")
block = re.search(r"```python\n(.*?)```", text[start:], re.S).group(1)
open("skillfns.py", "w", encoding="utf-8").write(block)
print("extracted source-tip order checker", len(block.splitlines()), "lines")
PY

python - "$DATA" <<'PY'
import pysam
import sys
from skillfns import is_coordinate_sorted

data = sys.argv[1]
checks = {
    "coordinate BAM": (f"{data}/human/test.paired_end.sorted.bam", None, True),
    "shuffled BAM": ("/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_real.bam", None, False),
    "CRAM with explicit reference": (f"{data}/human/test.paired_end.sorted.cram", f"{data}/human/genome.fasta", True),
}
header = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "unsorted"}})
with pysam.AlignmentFile("ubam.bam", "wb", header=header) as out:
    record = pysam.AlignedSegment(header)
    record.query_name = "unaligned"
    record.flag = 4
    record.query_sequence = "ACGT"
    record.query_qualities = pysam.qualitystring_to_array("IIII")
    out.write(record)
checks["uBAM without @SQ"] = ("ubam.bam", None, False)
for label, (path, reference, expected) in checks.items():
    actual = is_coordinate_sorted(path, reference)
    print(f"{label}: {actual} (expected {expected})")
    assert actual is expected
PY

samtools sort -T "$WORK/tmpdir" -o tempdir_sort.bam "$ROOT/data/shuffled_real.bam"
test -z "$(find "$WORK/tmpdir" -mindepth 1 -print -quit)"
samtools sort -@ 0 -o threads0.bam "$ROOT/data/shuffled_real.bam"
samtools sort -@ 4 -o threads4.bam "$ROOT/data/shuffled_real.bam"
cmp <(samtools view threads0.bam) <(samtools view threads4.bam)
echo "PASS: source-tip checker handles uBAM and CRAM; existing -T directory and -@ output behavior verified"
