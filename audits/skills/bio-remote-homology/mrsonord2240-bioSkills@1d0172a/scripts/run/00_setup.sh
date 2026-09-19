#!/bin/bash
set -e
WORK=/tmp/reaudit_rh
rm -rf "$WORK"
mkdir -p "$WORK"
cp -r /mnt/openscience/wt/db-rh/database-access/remote-homology/examples "$WORK/examples"
cp /mnt/openscience/audit-envs/database-access/public-data/remote-homology/PF00069.hmm* "$WORK/"
cp /mnt/openscience/audit-envs/database-access/public-data/remote-homology/P17612.fasta "$WORK/"
ls -la "$WORK"
