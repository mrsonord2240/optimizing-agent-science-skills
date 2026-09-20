import subprocess
import pandas as pd
from pathlib import Path

# ggsashimi input: col1 = sample id, col2 = BAM path, col3 = group (used by -O overlay and -C colour)
groups = pd.DataFrame({
    'sample_id': ['ctrl1', 'ctrl2', 'ctrl3', 'trt1', 'trt2', 'trt3'],
    'bam': ['G1_rep1.bam', 'G1_rep2.bam', 'G1_rep3.bam', 'G2_rep1.bam', 'G2_rep2.bam', 'G2_rep3.bam'],
    'group': ['Control', 'Control', 'Control', 'Treatment', 'Treatment', 'Treatment']
})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)
Path('palette.txt').write_text('#1f77b4\n#ff7f0e\n')  # one colour per group, in order of first appearance

missing = [b for b in groups['bam'] if not Path(b).is_file()]
assert not missing, f'ggsashimi would drop these BAMs silently: {missing}'

subprocess.run([
    'ggsashimi.py',
    '-b', 'sashimi_groups.tsv',
    '-c', 'chrP:1-1200',   # contig spelled as in the BAM header
    '-o', 'blk02',
    '--alpha', '0.25',
    '--height', '3',
    '--width', '10',
    '--shrink',
    '--fix-y-scale',
    '--ann-height', '4',
    '-g', 'planted.gtf',
    '--base-size', '14',
    '-O', '3', '-C', '3', '-P', 'palette.txt',
    '-A', 'mean_j',
    '-F', 'pdf'
], check=True)
assert Path('blk02.pdf').is_file() and Path('blk02.pdf').stat().st_size > 0, 'no figure written (R error above?)'
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

diff = pd.read_csv('/mnt/openscience/audits/bio-sashimi-plots/run/data/rmats_planted/SE.MATS.JC.txt', sep='\t')
sig = diff[(diff['FDR'] < 0.05) & (diff['IncLevelDifference'].abs() > 0.10)]

Path('plots').mkdir(exist_ok=True)
failed = []
for _, ev in sig.head(25).iterrows():
    region = f'{bam_contig(ev["chr"])}:{max(1, ev["upstreamES"] - 500)}-{ev["downstreamEE"] + 500}'
    safe_name = re.sub(r'[^A-Za-z0-9._-]', '_', f'{ev["geneSymbol"]}_{ev["chr"]}_{ev["upstreamES"]}_{ev["ID"]}')
    out = Path(f'plots/{safe_name}.svg')
    subprocess.run([
        'ggsashimi.py', '-b', 'sashimi_groups.tsv', '-c', region,
        '-o', str(out.with_suffix('')), '-M', '1', '--shrink', '--fix-y-scale',
        '-O', '3', '-C', '3', '-P', 'palette.txt', '-A', 'mean_j', '-g', 'planted.gtf', '-F', 'svg'
    ])
    if not (out.is_file() and out.stat().st_size > 0):
        failed.append(region)
assert not failed, f'no figure for {failed}'
