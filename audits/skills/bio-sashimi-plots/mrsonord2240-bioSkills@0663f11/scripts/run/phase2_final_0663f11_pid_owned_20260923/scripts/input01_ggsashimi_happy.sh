#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
W=$R/outputs/input01
mkdir -p "$W"
asenv as-viz-gg34 python - <<'PY'
import sys
from pathlib import Path
r=Path('/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923')
p=Path('/mnt/openscience/audit-envs/alternative-splicing/public-data/planted')
sys.path.insert(0,str(r/'source_copy/examples'))
from plot_sashimi import create_grouping_file, write_palette, plot_sashimi, junction_counts
bams=[str(p/f'{g}_rep{i}.bam') for g in ('G1','G2') for i in range(1,4)]
groups=['Control']*3+['Treatment']*3
g=create_grouping_file(bams,groups,r/'outputs/input01/groups.tsv')
pal=write_palette(['#1f77b4','#ff7f0e'],r/'outputs/input01/palette.txt')
assert junction_counts(bams[0],'chrP',1,1200)
out=plot_sashimi(str(g),'chrP:1-1200',str(r/'outputs/input01/happy'),str(p/'planted.gtf'),{'palette':str(pal),'format':'pdf','min_junc':1})
assert len(out)==1 and Path(out[0]).stat().st_size>1000
print('ASSERT happy_pdf_nonempty')
PY
