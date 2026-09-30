#!/bin/bash
D=/mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run
for c in "$@"; do bash $D/scripts/run_cli.sh $c > $D/logs/$c.log 2>&1; echo "$c $(tail -1 $D/logs/$c.log)"; done
