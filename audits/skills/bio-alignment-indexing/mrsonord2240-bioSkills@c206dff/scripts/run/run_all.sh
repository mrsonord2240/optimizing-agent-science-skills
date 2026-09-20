#!/bin/bash
# Re-runs the whole audit inside WSL `science` (env alignment-files). From Git Bash:
#   F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-indexing/run/run_all.sh'
# skill/ is a COPY of alignment-files/alignment-indexing at commit c206dff (the clone under external/ is never written to).
# data/ holds SYNTHETIC BAMs; big.bam / big.positions.txt were deleted after the run to save space and are rebuilt here (seeded).
set -u
cd /mnt/openscience/audits/bio-alignment-indexing/run
mkdir -p data work out
[ -f data/big.bam ] || python scripts/make_synth.py data
for t in t1_canonical t1b_snippets t2_cram_faidx t2b_cram_probe t3_edge t4_large_genome t5_stress; do
  echo "=== $t ==="
  python scripts/$t.py > out/$t.stdout.txt 2>&1
  tail -1 out/$t.stdout.txt
done
