#!/usr/bin/env bash
# Verifies the CLI flags SKILL.md documents for ITSxpress
# (itsxpress --fastq r1.fastq.gz --fastq2 r2.fastq.gz --region ITS2 --taxa Fungi
#  --outfile trimmed.fastq.gz --threads 4)
# actually exist in the installed tool. No ITS fixture data exists in this audit env
# (only the 16S V4 fixture, per TOOLS.md), so this checks flag/enum validity, not a full run.
MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc "micromamba run -n itsxpress itsxpress --help"
