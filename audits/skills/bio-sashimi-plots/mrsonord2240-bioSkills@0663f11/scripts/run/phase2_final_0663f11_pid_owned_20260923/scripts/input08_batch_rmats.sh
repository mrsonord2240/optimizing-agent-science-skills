#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
W=$R/outputs/input08
mkdir -p "$W"
asenv as-viz-gg34 python - <<'PY'
import sys
from pathlib import Path
r=Path('/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923'); p=Path('/mnt/openscience/audit-envs/alternative-splicing/public-data/planted')
sys.path.insert(0,str(r/'source_copy/examples'))
from plot_sashimi import create_grouping_file, write_palette, batch_plot_rmats_events
bams=[str(p/f'{g}_rep{i}.bam') for g in ('G1','G2') for i in range(1,4)]
g=create_grouping_file(bams,['G1']*3+['G2']*3,r/'outputs/input08/groups.tsv')
pal=write_palette(['#1f77b4','#ff7f0e'],r/'outputs/input08/palette.txt')
batch_plot_rmats_events('/mnt/openscience/audits/bio-sashimi-plots/run/data/rmats_planted/SE.MATS.JC.txt',str(g),str(p/'planted.gtf'),str(r/'outputs/input08/plots'),n_top=1,flank=50,palette=str(pal))
pdfs=list((r/'outputs/input08/plots').glob('*.pdf'))
assert len(pdfs)==1 and pdfs[0].stat().st_size>1000
print('ASSERT batch_rmats_one_pdf')
PY
