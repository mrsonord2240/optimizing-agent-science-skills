import subprocess
import pandas as pd
from pathlib import Path

# ggsashimi input: col1 = sample id, col2 = BAM path, col3 = group (used by -O overlay and -C colour)
groups = pd.DataFrame({
    'sample_id': ['ctrl1', 'ctrl2', 'ctrl3', 'trt1', 'trt2', 'trt3'],
    'bam': ['ctrl1.bam', 'ctrl2.bam', 'ctrl3.bam', 'trt1.bam', 'trt2.bam', 'trt3.bam'],
    'group': ['Control', 'Control', 'Control', 'Treatment', 'Treatment', 'Treatment']
})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)
Path('palette.txt').write_text('#1f77b4\n#ff7f0e\n')  # one colour per group, in order of first appearance

missing = [b for b in groups['bam'] if not Path(b).is_file()]
assert not missing, f'ggsashimi would drop these BAMs silently: {missing}'

subprocess.run([
    'ggsashimi.py',
    '-b', 'sashimi_groups.tsv',
    '-c', 'chr17:43094000-43125000',   # contig spelled as in the BAM header
    '-o', 'BRCA1_sashimi',
    '--alpha', '0.25',
    '--height', '3',
    '--width', '10',
    '--shrink',
    '--fix-y-scale',
    '--ann-height', '4',
    '-g', 'gencode_v45.gtf',
    '--base-size', '14',
    '-O', '3', '-C', '3', '-P', 'palette.txt',
    '-A', 'mean_j',
    '-F', 'pdf'
], check=True)
assert Path('BRCA1_sashimi.pdf').is_file() and Path('BRCA1_sashimi.pdf').stat().st_size > 0, 'no figure written (R error above?)'
