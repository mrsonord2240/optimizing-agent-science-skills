#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
W=$R/outputs/input02
mkdir -p "$W"
asenv as-viz-gg34 python - <<'PY'
import sys
from pathlib import Path
r=Path('/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923')
p=Path('/mnt/openscience/audit-envs/alternative-splicing/public-data/planted')
sys.path.insert(0,str(r/'source_copy/examples'))
from plot_sashimi import plot_sashimi
g=r/'outputs/input02/missing.tsv'; g.write_text('bad\t/no/such.bam\tControl\n')
try: plot_sashimi(str(g),'chrP:1-1200',str(r/'outputs/input02/bad'),str(p/'planted.gtf'))
except FileNotFoundError: print('ASSERT missing_bam_guard')
else: raise AssertionError('missing BAM silently accepted')
g2=r/'outputs/input02/good.tsv'; g2.write_text(f'good\t{p}/G1_rep1.bam\tControl\n')
try: plot_sashimi(str(g2),'chrNotThere:1-1200',str(r/'outputs/input02/no_reads'),str(p/'planted.gtf'))
except ValueError: print('ASSERT contig_guard')
else: raise AssertionError('unknown contig silently accepted')
PY
