#!/usr/bin/env python3
"""Independently compare raw VCF missing genotypes with VCFtools outputs."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


def read_truth(vcf_path: Path):
    samples = []
    sample_missing = []
    site_missing = {}
    n_sites = 0
    with vcf_path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#CHROM"):
                samples = line.rstrip("\n").split("\t")[9:]
                sample_missing = [0] * len(samples)
            elif not line.startswith("#"):
                fields = line.rstrip("\n").split("\t")
                gts = [value.split(":", 1)[0] for value in fields[9:]]
                missing = sum(allele == "." for gt in gts for allele in re.split(r"[/|]", gt))
                for i, gt in enumerate(gts):
                    sample_missing[i] += int("." in gt)
                site_missing[(fields[0], fields[1])] = missing
                n_sites += 1
    return samples, sample_missing, site_missing, n_sites


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: validate_missingness.py cohort.vcf sample.imiss site.lmiss")
    vcf_path, imiss_path, lmiss_path = map(Path, sys.argv[1:])
    samples, expected_sample, expected_site, n_sites = read_truth(vcf_path)

    observed_sample = {}
    with imiss_path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t", skipinitialspace=True):
            observed_sample[row["INDV"].strip()] = int(row["N_MISS"])

    observed_site = {}
    with lmiss_path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t", skipinitialspace=True):
            observed_site[(row["CHR"].strip(), row["POS"].strip())] = int(row["N_MISS"])

    expected_sample_map = dict(zip(samples, expected_sample))
    assert observed_sample == expected_sample_map, (observed_sample, expected_sample_map)
    assert observed_site == expected_site, "per-site missingness differs from raw VCF"
    assert len(observed_site) == n_sites == 361
    print(f"PASS missingness: {len(samples)} samples and {n_sites} sites match raw-Vcf truth")
    print("sample_missing=" + ",".join(f"{s}:{expected_sample_map[s]}" for s in samples))


if __name__ == "__main__":
    main()
