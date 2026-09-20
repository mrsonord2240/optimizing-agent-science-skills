#!/usr/bin/env python3
"""Auditor patcher: apply cumulative fixes to a COPY of examples/longread_splicing_pipeline.sh, one failure class per stage.
stage 1: isoquant.py -> isoquant (entry point of pip/conda install)
stage 2: drop 'flair correct --genome' (option does not exist in FLAIR 3.0.1)
stage 3: SQANTI3 output prefix must not contain a directory: use --output <prefix> --dir <dir>; fix classification path; skip R report
"""
import sys
src, dst, stage = sys.argv[1], sys.argv[2], int(sys.argv[3])
s = open(src, encoding="utf-8").read()
if stage >= 1:
    s = s.replace("\nisoquant.py \\\n", "\nisoquant \\\n")
if stage >= 2:
    s = s.replace("    --query ${OUTPUT_DIR}/${SAMPLE}.bed \\\n    --genome ${REFERENCE} \\\n", "    --query ${OUTPUT_DIR}/${SAMPLE}.bed \\\n")
if stage >= 3:
    s = s.replace("    --output ${OUTPUT_DIR}/sqanti3 \\\n", "    --output sqanti3 --dir ${OUTPUT_DIR}/sqanti3 --report skip \\\n")
    s = s.replace("--sqanti_class ${OUTPUT_DIR}/sqanti3/${SAMPLE}_classification.txt", "--sqanti_class ${OUTPUT_DIR}/sqanti3/sqanti3_classification.txt")
    s = s.replace("    --output ${OUTPUT_DIR}/sqanti3_filtered\n", "    --output sqanti3_filtered --dir ${OUTPUT_DIR}/sqanti3_filtered --skip_report\n")
open(dst, "w", encoding="utf-8", newline="\n").write(s)
