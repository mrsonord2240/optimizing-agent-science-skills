#!/usr/bin/env python3
"""Input 1: SKILL.md 'ggsashimi for Publication Overlays' block, verbatim except (a) sample/BAM names -> planted synthetic BAMs,
(b) region/GTF/output prefix, (c) called once with -F pdf (as the Skill) and once with -F svg (so labels can be parsed) and png (to look at).
Run from run/data/planted so the relative BAM names in the TSV resolve."""
import subprocess
import pandas as pd

groups = pd.DataFrame({
    'sample_id': ['ctrl1', 'ctrl2', 'ctrl3', 'trt1', 'trt2', 'trt3'],
    'bam': ['G1_rep1.bam', 'G1_rep2.bam', 'G1_rep3.bam', 'G2_rep1.bam', 'G2_rep2.bam', 'G2_rep3.bam'],
    'group': ['Control', 'Control', 'Control', 'Treatment', 'Treatment', 'Treatment']
})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)

for fmt in ('pdf', 'svg', 'png'):
    subprocess.run([
        'ggsashimi.py',
        '-b', 'sashimi_groups.tsv',
        '-c', 'chrP:1-1200',
        '-o', '../../out/i1_G1_sashimi',
        '-M', '10',
        '--alpha', '0.25',
        '--height', '3',
        '--width', '10',
        '--shrink',
        '--fix-y-scale',
        '--ann-height', '4',
        '-g', 'planted.gtf',
        '--base-size', '14',
        '-O', '3',
        '-A', 'mean_j',
        '-F', fmt
    ], check=True)
