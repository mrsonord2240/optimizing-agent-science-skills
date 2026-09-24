#!/usr/bin/env python3
"""Exercise the final-pass parser fixes against a copied, audited Skill."""
import importlib.util
import subprocess
import sys

ROOT = "/mnt/openscience/audits/bio-alignment-indexing/run/final_20260924"
SKILL = f"{ROOT}/skill/examples/fetch_regions.py"
BAM = "/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam"

spec = importlib.util.spec_from_file_location("fetch_regions", SKILL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

assert module.parse_region("ctg,1", ("ctg,1", "chr22")) == ("ctg,1", None, None)
assert module.parse_region("ctg,1:100-200", ("ctg,1", "chr22")) == ("ctg,1", 99, 200)
assert module.parse_region("chr22:0-4000", ("ctg,1", "chr22")) == ("chr22", 0, 4000)
try:
    module.parse_region("chr22:5000-4000", ("ctg,1", "chr22"))
except ValueError as exc:
    assert str(exc) == "start after end"
else:
    raise AssertionError("reversed interval did not fail")

zero = subprocess.run([sys.executable, SKILL, BAM, "chr22:0-4000"], text=True, capture_output=True)
assert zero.returncode == 0, zero.stderr
assert "Total reads in chr22:0-4000: 5550" in zero.stdout, zero.stdout[-200:]

bad = subprocess.run([sys.executable, SKILL, BAM, "chr22:5000-4000"], text=True, capture_output=True)
assert bad.returncode != 0
assert "Bad region 'chr22:5000-4000': start after end" in bad.stderr, bad.stderr
assert "Traceback" not in bad.stderr, bad.stderr

print("PASS parser preserves comma contigs; 0 start matches samtools; reversed interval is a clean error")
