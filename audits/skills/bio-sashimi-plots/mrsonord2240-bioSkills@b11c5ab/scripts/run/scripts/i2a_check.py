#!/usr/bin/env python3
"""Verify batch-block SVG labels against independent pysam counts, event by event (recomputes the block's region string)."""
import subprocess, pandas as pd, pysam, re, pathlib, sys
RUN = pathlib.Path('/mnt/openscience/audits/bio-sashimi-plots/run')
for st, rm in (('planted', 'rmats_planted'), ('real', 'rmats_real')):
    W = RUN / 'out' / f'i2a_{st}' / 'svg'
    tsv = W / 'sashimi_groups.tsv'
    first_bam = tsv.read_text().splitlines()[0].split('\t')[1]
    first_bam = first_bam if first_bam.startswith('/') else str(W / first_bam)
    contigs = set(pysam.AlignmentFile(first_bam).references)
    d = pd.read_csv(RUN / 'data' / rm / 'SE.MATS.JC.txt', sep='\t')
    sig = d[(d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10)]
    for _, ev in sig.head(25).iterrows():
        c = next(x for x in (ev['chr'], ev['chr'].removeprefix('chr'), 'chr' + ev['chr'].removeprefix('chr')) if x in contigs)
        reg = f'{c}:{max(1, ev["upstreamES"] - 500)}-{ev["downstreamEE"] + 500}'
        name = re.sub(r'[^A-Za-z0-9._-]', '_', f'{ev["geneSymbol"]}_{ev["chr"]}_{ev["upstreamES"]}_{ev["ID"]}')
        svg = W / 'plots' / f'{name}.svg'
        r = subprocess.run(['micromamba', 'run', '-n', 'as-core', 'python', str(RUN / 'scripts/jtruth.py'), reg, str(tsv), '--M', '1', '--svg', str(svg)], capture_output=True, text=True, cwd=W)
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]
        print(st, ev['geneSymbol'], ev['strand'], reg, '->', last)
