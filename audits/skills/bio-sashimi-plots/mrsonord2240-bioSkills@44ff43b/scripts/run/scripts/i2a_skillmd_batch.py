#!/usr/bin/env python3
"""Input 2a: SKILL.md 'Batch Plotting from rMATS Hits' block VERBATIM (only paths differ: rmats file, and cwd=run/data so
sashimi_groups.tsv / annotation.gtf resolve). Real chrX data (GBR v YRI, 2v2)."""
import subprocess
import pandas as pd
from pathlib import Path

diff = pd.read_csv('rmats_real/SE.MATS.JC.txt', sep='\t')
sig = diff[(diff['FDR'] < 0.05) & (diff['IncLevelDifference'].abs() > 0.10)]
print('significant events:', len(sig))

Path('../out/sashimi_plots').mkdir(exist_ok=True)
for idx, ev in sig.head(25).iterrows():
    region = f'{ev["chr"]}:{ev["upstreamES"] - 500}-{ev["downstreamEE"] + 500}'
    safe_name = f'{ev["geneSymbol"]}_{ev["chr"]}_{ev["upstreamES"]}'
    print('region', region)
    subprocess.run([
        'ggsashimi.py',
        '-b', 'sashimi_groups.tsv',
        '-c', region,
        '-o', f'../out/sashimi_plots/{safe_name}',
        '-M', '5',
        '--shrink',
        '--fix-y-scale',
        '-O', '3',
        '-A', 'mean_j',
        '-g', 'annotation.gtf',
        '-F', 'pdf'
    ], check=True)
