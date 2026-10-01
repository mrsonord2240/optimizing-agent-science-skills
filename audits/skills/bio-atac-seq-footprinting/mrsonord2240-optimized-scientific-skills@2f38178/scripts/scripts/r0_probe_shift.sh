#!/bin/bash
# Read scPrinter 1.2.0 source for how plus_shift/minus_shift are applied at fragment import.
f=/home/sci/micromamba/envs/bio-atac-seq-footprinting-scprinter/lib/python3.11/site-packages/scprinter
echo "pkg: $f"
grep -rn "plus_shift\|minus_shift\|shift_left\|shift_right\|auto_detect_shift" "$f" --include=*.py | head -60
