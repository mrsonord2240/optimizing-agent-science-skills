import subprocess
import pandas as pd
from pathlib import Path
groups = pd.DataFrame({
    'sample_id': ['gbr1', 'gbr2', 'yri1', 'yri2'],
    'bam': ['/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188383.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188428.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR188454.Aligned.out.bam', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/bam/ERR204916.Aligned.out.bam'],
    'group': ['GBR', 'GBR', 'YRI', 'YRI']})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)
Path('palette.txt').write_text('#1f77b4\n#ff7f0e\n')
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

diff = pd.read_csv('/mnt/openscience/audits/bio-sashimi-plots/run/data/rmats_real/SE.MATS.JC.txt', sep='\t')
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
        '-O', '3', '-C', '3', '-P', 'palette.txt', '-A', 'mean_j', '-g', '/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf', '-F', 'svg'
    ])
    if not (out.is_file() and out.stat().st_size > 0):
        failed.append(region)
assert not failed, f'no figure for {failed}'
