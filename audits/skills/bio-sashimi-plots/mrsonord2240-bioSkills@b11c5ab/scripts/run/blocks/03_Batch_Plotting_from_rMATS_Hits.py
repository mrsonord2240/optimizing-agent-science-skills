import re
import subprocess
import pandas as pd
import pysam
from pathlib import Path

contigs = set(pysam.AlignmentFile(groups['bam'][0]).references)  # groups = the TSV above

def bam_contig(name):
    for cand in (name, name.removeprefix('chr'), 'chr' + name.removeprefix('chr')):
        if cand in contigs:
            return cand
    raise ValueError(f'contig {name} not in the BAM header')

diff = pd.read_csv('rmats_output/SE.MATS.JC.txt', sep='\t')
sig = diff[(diff['FDR'] < 0.05) & (diff['IncLevelDifference'].abs() > 0.10)]

Path('sashimi_plots').mkdir(exist_ok=True)
failed = []
for _, ev in sig.head(25).iterrows():
    region = f'{bam_contig(ev["chr"])}:{max(1, ev["upstreamES"] - 500)}-{ev["downstreamEE"] + 500}'
    safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', f'{ev["geneSymbol"]}_{ev["chr"]}_{ev["upstreamES"]}_{ev["ID"]}')
    out = Path(f'sashimi_plots/{safe_name}.pdf')
    subprocess.run([
        'ggsashimi.py', '-b', 'sashimi_groups.tsv', '-c', region,
        '-o', str(out.with_suffix('')), '-M', '1', '--shrink', '--fix-y-scale',
        '-O', '3', '-C', '3', '-P', 'palette.txt', '-A', 'mean_j', '-g', 'annotation.gtf', '-F', 'pdf'
    ])
    if not (out.is_file() and out.stat().st_size > 0):
        failed.append(region)
assert not failed, f'no figure for {failed}'
