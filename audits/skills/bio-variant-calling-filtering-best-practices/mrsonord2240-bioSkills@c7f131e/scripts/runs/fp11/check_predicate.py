"""Execute the current SKILL.md cyvcf2 loop body with an in-memory VCF-shaped stub.

The prior WSL cyvcf2 environment is absent on 2026-09-24.  This does not claim
an integration test; it directly executes the documented predicate to verify
the repaired zero-versus-missing semantics.
"""
from pathlib import Path
import re
import sys

skill = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(r"for variant in vcf:\n(?P<body>.*?)writer\.close\(\); vcf\.close\(\)", skill, re.S)
assert match, "could not find the documented cyvcf2 loop"
predicate = "for variant in vcf:\n" + match.group("body")

class Info:
    def __init__(self, values):
        self.values = values
    def get(self, key):
        return self.values.get(key)

class Variant:
    def __init__(self, pos, values):
        self.POS = pos
        self.QUAL = 50
        self.INFO = Info(values)

class Writer:
    def __init__(self):
        self.kept = []
    def write_record(self, variant):
        self.kept.append(variant.POS)

writer = Writer()
vcf = [
    Variant(1, {"DP": 20, "FS": 0, "MQ": 60, "QD": 10, "SOR": 1}),
    Variant(2, {"DP": 0, "FS": 0, "MQ": 60, "QD": 10, "SOR": 1}),
    Variant(3, {"DP": 20, "FS": 0, "MQ": 0, "QD": 10, "SOR": 1}),
    Variant(4, {"FS": 0, "QD": 10, "SOR": 1}),
    Variant(5, {"DP": 20, "FS": 0, "MQ": 60, "QD": 10, "SOR": 1}),
]
exec(predicate, {"vcf": vcf, "writer": writer})
assert writer.kept == [1, 4, 5], writer.kept
print("PASS: exact-current cyvcf2 predicate keeps normal/missing/rank-sum-missing calls and rejects DP=0 and MQ=0.")
