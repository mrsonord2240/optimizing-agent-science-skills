#!/bin/bash
# Re-runs the whole re-audit inside WSL `science` (env alignment-files). From Git Bash:
#   F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-indexing/run/run_all.sh'
# skill/ is a COPY of alignment-files/alignment-indexing at commit 68a47bf (worktree wt/af-index; never written to).
# data/ holds SYNTHETIC BAMs built by make_synth.py (big.bam, 1.2M reads, is deleted after the run and rebuilt here).
set -u
cd /mnt/openscience/audits/bio-alignment-indexing/run
mkdir -p data work out
[ -f data/big.bam ] || python scripts/make_synth.py data
for t in "$@"; do
  echo "=== $t ==="
  python scripts/$t.py > out/$t.stdout.txt 2>&1
  tail -1 out/$t.stdout.txt
done
