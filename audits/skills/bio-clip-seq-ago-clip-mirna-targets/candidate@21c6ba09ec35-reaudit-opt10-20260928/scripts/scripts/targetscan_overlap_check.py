#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
BEDTOOLS = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/bedtools")
PYTHON = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python")

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    sites = root / "sites.tsv"
    maps = root / "maps.tsv"
    bed = root / "sites.bed12"
    manifest = root / "manifest.json"
    sites.write_text(
        "transcript_id\tutr_start_1\tutr_end_1\tmirna_family\tsite_type\n"
        "txPlus\t8\t14\tmiR-1\t8mer\n"
        "txMinus\t8\t14\tmiR-1\t8mer\n",
        encoding="utf-8",
    )
    maps.write_text(
        "transcript_id\tchrom\tstrand\tutr_exon_starts_0\tutr_exon_ends_0\tassembly\tannotation_release\ttargetscan_release\n"
        "txPlus\tchr1\t+\t100,200\t110,210\tGRCh38\tGENCODEv49\t8.0\n"
        "txMinus\tchr2\t-\t300,400\t310,410\tGRCh38\tGENCODEv49\t8.0\n",
        encoding="utf-8",
    )
    good = subprocess.run(
        [str(PYTHON), str(CANDIDATE / "scripts/targetscan_sites_to_bed12.py"), "--sites", str(sites), "--utr-map", str(maps), "--output", str(bed), "--manifest", str(manifest), "--assembly", "GRCh38", "--annotation-release", "GENCODEv49", "--targetscan-release", "8.0"],
        text=True, capture_output=True,
    )
    bed_rows = [line.split("\t") for line in bed.read_text(encoding="utf-8").splitlines()]
    peaks = root / "peaks.bed"
    peaks.write_text(
        "chr1\t107\t205\tplus-good\t1\t+\n"
        "chr1\t107\t205\tplus-wrong-strand\t1\t-\n"
        "chr2\t305\t405\tminus-good\t1\t-\n",
        encoding="utf-8",
    )
    overlap = subprocess.run([str(BEDTOOLS), "intersect", "-split", "-s", "-wa", "-wb", "-a", str(peaks), "-b", str(bed)], text=True, capture_output=True)
    wrong_release = subprocess.run(
        [str(PYTHON), str(CANDIDATE / "scripts/targetscan_sites_to_bed12.py"), "--sites", str(sites), "--utr-map", str(maps), "--output", str(root / "bad.bed"), "--manifest", str(root / "bad.json"), "--assembly", "GRCh38", "--annotation-release", "GENCODEv49", "--targetscan-release", "7.2"],
        text=True, capture_output=True,
    )
    out_of_range_sites = root / "out-of-range.tsv"
    out_of_range_sites.write_text("transcript_id\tutr_start_1\tutr_end_1\tmirna_family\tsite_type\ntxPlus\t1\t99\tmiR-1\t8mer\n", encoding="utf-8")
    out_of_range = subprocess.run(
        [str(PYTHON), str(CANDIDATE / "scripts/targetscan_sites_to_bed12.py"), "--sites", str(out_of_range_sites), "--utr-map", str(maps), "--output", str(root / "range.bed"), "--manifest", str(root / "range.json"), "--assembly", "GRCh38", "--annotation-release", "GENCODEv49", "--targetscan-release", "8.0"],
        text=True, capture_output=True,
    )
    payload = {
        "conversion_returncode": good.returncode,
        "bed_rows": bed_rows,
        "plus_and_minus_multiblock": len(bed_rows) == 2 and all(row[9] == "2" for row in bed_rows) and {row[5] for row in bed_rows} == {"+", "-"},
        "overlap_returncode": overlap.returncode,
        "overlap_rows": overlap.stdout.splitlines(),
        "same_strand_only": "plus-wrong-strand" not in overlap.stdout and "plus-good" in overlap.stdout and "minus-good" in overlap.stdout,
        "wrong_release_rejected": wrong_release.returncode != 0 and "release metadata" in wrong_release.stderr,
        "out_of_range_rejected": out_of_range.returncode != 0 and "exceeds mapped UTR length" in out_of_range.stderr,
        "manifest": json.loads(manifest.read_text(encoding="utf-8")),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
