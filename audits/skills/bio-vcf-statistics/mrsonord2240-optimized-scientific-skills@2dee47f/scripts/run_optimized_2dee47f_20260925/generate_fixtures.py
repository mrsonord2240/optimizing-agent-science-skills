#!/usr/bin/env python3
"""Build and copy the synthetic VCF fixtures used by this independent re-audit."""

from __future__ import annotations

import shutil
from pathlib import Path


BASE = Path("/mnt/openscience/audits/bio-vcf-statistics")
DEST = BASE / "reaudit-optimized-scientific-skills@2dee47f-20260925" / "data"
PRIOR = BASE / "data"


def write_text(name: str, text: str) -> None:
    (DEST / name).write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for name in ("cohort.vcf", "cohort.ped", "callerA.vcf", "callerB.vcf"):
        shutil.copyfile(PRIOR / name, DEST / name)

    common = """\
##fileformat=VCFv4.2
##contig=<ID=chr1,length=1000>
##FILTER=<ID=LowQual,Description="Low quality">
##INFO=<ID=AF,Number=A,Type=Float,Description="Alternate allele frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1
"""

    write_text(
        "core_regression.vcf",
        common
        + """\
chr1\t10\t.\tA\tG,C\t0\tPASS\tAF=0.1,0.2\tGT\t1/2
chr1\t20\t.\tC\tT,A\t20\tLowQual\tAF=0.2,0.1\tGT\t0/1
chr1\t30\t.\tAT\tA\t.\t.\tAF=0.1\tGT\t0/1
chr1\t40\t.\tA\t<DEL>\t40\tPASS\tAF=0.1\tGT\t0/1
""",
    )

    write_text(
        "filter_semantics.vcf",
        common
        + """\
chr1\t100\t.\tA\tG\t10\tPASS\tAF=0.1\tGT\t0/1
chr1\t110\t.\tC\tT\t20\t.\tAF=0.1\tGT\t0/1
chr1\t120\t.\tG\tT\t30\tLowQual\tAF=0.1\tGT\t0/1
""",
    )

    write_text("empty.vcf", common)

    write_text(
        "transitions_only.vcf",
        common
        + """\
chr1\t200\t.\tA\tG\t0\tPASS\tAF=0.1\tGT\t0/1
chr1\t210\t.\tC\tT\t10\tPASS\tAF=0.1\tGT\t0/1
""",
    )

    write_text("easy_regions.bed", "chr1\t0\t20000")
    write_text("difficult_regions.bed", "chr2\t0\t15000")
    write_text(
        "README.txt",
        "Synthetic fixtures only. cohort.vcf, cohort.ped, callerA.vcf, and callerB.vcf "
        "are copied from the prior canonical audit data solely so prior inputs can be rerun. "
        "The remaining VCF and BED files are new independent re-audit fixtures.",
    )


if __name__ == "__main__":
    main()
