#!/bin/bash
# Verbatim transcripts of both shipped validators on four representative inputs (for the viewer).
RUN=/mnt/openscience/audits/bio-alignment-validation/run; PD=/mnt/openscience/audit-envs/alignment-files/public-data
PY=$RUN/skill/examples/validate_alignment.py; SH=$RUN/skill/examples/validate_alignment.sh
for f in "$PD/human/test.paired_end.sorted.bam" "$RUN/data/lowmap_unplaced.bam" "$RUN/data/new/lad_warn_plus_fail.bam" "$RUN/data/trunc_tail.bam"; do
  echo "################ $(basename $f)"
  echo "---- python examples/validate_alignment.py"; python $PY $f; echo "[exit status $?]"
  echo "---- bash examples/validate_alignment.sh (flagstat block omitted)"; bash $SH $f 2>&1 | grep -v -E '^[0-9]+ \+ [0-9]+ ' ; echo "[exit status ${PIPESTATUS[0]}]"
done
