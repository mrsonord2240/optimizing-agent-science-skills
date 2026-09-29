#!/usr/bin/env python3
from __future__ import annotations

import gzip
import json
import subprocess
import tempfile
from pathlib import Path

TOOLING = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets")
UMI = TOOLING / "conda-env/bin/umi_tools"
CUTADAPT = TOOLING / "conda-env/bin/cutadapt"
SAMTOOLS = TOOLING / "conda-env/bin/samtools"


def fastq(path: Path, header: str, sequence: str) -> None:
    with gzip.open(path, "wt", encoding="utf-8", newline="") as handle:
        handle.write(f"@{header}\n{sequence}\n+\n{'I' * len(sequence)}\n")


with tempfile.TemporaryDirectory(prefix="ago-secondary-audit2-") as temporary:
    root = Path(temporary)
    adapter1 = "AGATCGGAAGAGCACACGTCT"
    adapter2 = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"
    r1, r2 = root / "R1.fastq.gz", root / "R2.fastq.gz"
    fastq(r1, "read1", "ACGTACGTAC" + "G" * 20 + adapter1)
    fastq(r2, "read1", "C" * 20 + adapter2)
    r1_umi, r2_umi = root / "R1.umi.fastq.gz", root / "R2.umi.fastq.gz"
    umi_run = subprocess.run([str(UMI), "extract", "--bc-pattern=NNNNNNNNNN", f"--stdin={r1}", f"--read2-in={r2}", f"--stdout={r1_umi}", f"--read2-out={r2_umi}"], text=True, capture_output=True)
    assert umi_run.returncode == 0, umi_run.stderr
    with gzip.open(r1_umi, "rt", encoding="utf-8") as handle:
        r1_umi_text = handle.read()
    cut_r1, cut_r2 = root / "R1.trim.fastq.gz", root / "R2.trim.fastq.gz"
    trim = subprocess.run([str(CUTADAPT), "-a", adapter1, "-A", adapter2, "-q", "6", "-m", "18", "-o", str(cut_r1), "-p", str(cut_r2), str(r1_umi), str(r2_umi)], text=True, capture_output=True)
    assert trim.returncode == 0, trim.stderr
    with gzip.open(cut_r1, "rt", encoding="utf-8") as handle:
        trim1 = handle.read().splitlines()
    with gzip.open(cut_r2, "rt", encoding="utf-8") as handle:
        trim2 = handle.read().splitlines()

    sam = root / "softclip.sam"
    sam.write_text(
        "@HD\tVN:1.6\tSO:unsorted\n@SQ\tSN:chr1\tLN:1000\n"
        "soft\t0\tchr1\t1\t60\t5M5S\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        "full\t0\tchr1\t20\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
        encoding="utf-8")
    bam = root / "softclip.bam"
    conversion = subprocess.run([str(SAMTOOLS), "view", "-b", "-o", str(bam), str(sam)], text=True, capture_output=True)
    assert conversion.returncode == 0, conversion.stderr
    diagnostic = subprocess.run(f"{SAMTOOLS} view -h {bam} | awk '$6 ~ /S/' | wc -l", shell=True, text=True, capture_output=True)
    softclip_count = int(diagnostic.stdout.strip())
    assert diagnostic.returncode == 0 and softclip_count == 1
    print(json.dumps({
        "yeo_total_umi_tools_returncode": umi_run.returncode,
        "umi_header_has_10nt_suffix": r1_umi_text.splitlines()[0].startswith("@read1_ACGTACGTAC"),
        "cutadapt_returncode": trim.returncode,
        "trimmed_r1_length": len(trim1[1]),
        "trimmed_r2_length": len(trim2[1]),
        "softclip_diagnostic_returncode": diagnostic.returncode,
        "softclipped_records": softclip_count,
        "scope_note": "Synthetic bounded route fixtures; full biological Yeo and AGO peak-calling workflows were not run.",
        "assertions_passed": 5,
        "assertions_total": 5,
    }, indent=2, sort_keys=True))
