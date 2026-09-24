#!/usr/bin/env python3
"""Final-pass regression runner against the committed-source candidate.

Uses archived synthetic CIGAR and planted-SNV inputs plus new checks for the
read-N policy, a trailing deletion, and padded-CIGAR rejection.
"""

import json
import os
import subprocess
import sys

import pysam

SOURCE = "/mnt/f/OpenScience/worktrees/bio-pileup-generation-finalpass/alignment-files/pileup-generation"
DATA = "/mnt/f/OpenScience/audits/bio-pileup-generation/run/data"
sys.path.insert(0, SOURCE + "/examples")
from pileup_helpers import allele_counts, allele_frequency, find_variants, pileup_text


def check(label, condition, detail=""):
    if not condition:
        raise AssertionError(f"FAIL {label}: {detail}")
    print(f"PASS {label}" + (f" ({detail})" if detail else ""))


def mpileup_rows(reference, bam, flags):
    result = subprocess.run(
        ["samtools", "mpileup", "-f", reference, *flags, bam],
        text=True, capture_output=True, check=True,
    )
    return result.stdout.splitlines()


def helper_rows(reference, bam, flags):
    arguments = {
        "default": {},
        "-B": {"compute_baq": False},
        "-E": {"redo_baq": True},
        "-q20-Q20-x-A": {
            "min_mapping_quality": 20, "min_base_quality": 20,
            "ignore_overlaps": False, "ignore_orphans": False,
        },
        "--ff0-Q0-B": {"flag_filter": 0, "min_base_quality": 0,
                         "compute_baq": False},
    }[flags]
    with pysam.FastaFile(reference) as fasta:
        return [
            row for contig, length in zip(fasta.references, fasta.lengths)
            for row in pileup_text(bam, reference, contig, 0, length, **arguments)
        ]


truth = json.load(open(DATA + "/truth.json"))["truth"]["events"]
syn, syn_ref = DATA + "/syn.bam", DATA + "/syn.fa"
event = truth["snp"]
counts = allele_counts(syn, "synA", 99)
check("archived planted SNP counts", counts == {event["ref"]: 30, event["alt"]: 10}, counts)
check("archived planted SNP frequencies", allele_frequency(syn, "synA", 99) == {event["ref"]: .75, event["alt"]: .25})
calls = find_variants(syn, syn_ref, "synA", 0, 1000)
check("archived planted SNV call", [(v["pos"], v["alt_count"], v["depth"]) for v in calls] == [(100, 10, 40)], calls)

# Input 6 regression: 23 ordinary CIGAR templates against samtools across all
# previously tested option sets.
legal_bam, legal_ref = DATA + "/cg_legal.bam", DATA + "/cg_legal.fa"
sets = [
    ("default", [], {}),
    ("-B", ["-B"], {}),
    ("-E", ["-E"], {}),
    ("-q20-Q20-x-A", ["-q", "20", "-Q", "20", "-x", "-A"], {}),
    ("--ff0-Q0-B", ["--ff", "0", "-Q", "0", "-B"], {}),
]
for label, cli, _ in sets:
    expected = mpileup_rows(legal_ref, legal_bam, cli)
    actual = helper_rows(legal_ref, legal_bam, label)
    check(f"archived ordinary-CIGAR parity {label}", actual == expected,
          f"rows={len(actual)}")

# Fresh P2 checks: N is excluded consistently; a deletion after the final base
# has Q0 rather than an IndexError; padded CIGARs fail clearly instead of
# emitting incorrect pileup text.
pv_bam, pv_ref = DATA + "/pv.bam", DATA + "/pv.fa"
pv_counts = allele_counts(pv_bam, "pv1", 419)
check("fresh read-N exclusion in counts", "N" not in pv_counts and sum(pv_counts.values()) == 17, pv_counts)
check("fresh read-N exclusion in frequency", sum(allele_frequency(pv_bam, "pv1", 419).values()) == 1.0)

trailing_bam, trailing_ref = DATA + "/cw4.bam", DATA + "/cw4.fa"
expected = mpileup_rows(trailing_ref, trailing_bam, ["--ff", "0", "-Q", "0", "-B"])
actual = helper_rows(trailing_ref, trailing_bam, "--ff0-Q0-B")
check("fresh trailing-deletion parity", actual == expected, f"rows={len(actual)}")

try:
    next(pileup_text(DATA + "/cw9.bam", DATA + "/cw9.fa", "cg1", 0, 260))
except ValueError as error:
    check("fresh padded-CIGAR refusal", "padding" in str(error))
else:
    raise AssertionError("FAIL fresh padded-CIGAR refusal: no error")

run = subprocess.run([sys.executable, SOURCE + "/examples/self_test.py"], text=True,
                     capture_output=True, check=True)
check("fresh shipped self-test", "passed" in run.stdout, run.stdout.strip())
print("FINAL: 14/14 assertions passed")
