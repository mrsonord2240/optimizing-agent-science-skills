#!/usr/bin/env python3
"""Input 7 (NEW): mutually exclusive exons on real chrX data (minus- and plus-strand genes), 2 GBR v 2 YRI.
(a) SKILL.md claim: 'MXE files carry upstreamES/downstreamEE and that span already covers both alternative exons' - checked on every MXE row.
(b) ggsashimi on the top-4 MXE events with the batch recipe's region string (contig X vs rMATS chrX), SVG labels vs pysam counts.
(c) rmats2sashimiplot --event-type MXE with the flags of the Skill's block (04), figure-exists assert on 4 events.
The 4 events are the lowest-FDR MXE rows (only 2 of 17 pass FDR < 0.05 in a 2v2 set, so the block's FDR awk filter is replaced by 'top 4')."""
import pathlib, shutil, subprocess
import pandas as pd
RUN = pathlib.Path('/mnt/openscience/audits/bio-sashimi-plots/run')
PUB = pathlib.Path('/mnt/openscience/audit-envs/alternative-splicing/public-data')
W = RUN / 'out' / 'i7_mxe'
shutil.rmtree(W, ignore_errors=True)
W.mkdir(parents=True)
src = RUN / 'data/rmats_real/MXE.MATS.JC.txt'
raw = src.read_text().splitlines()
mxe = pd.read_csv(src, sep='\t')
cover = ((mxe['upstreamES'] < mxe['1stExonStart_0base']) & (mxe['1stExonEnd'] < mxe['downstreamEE']) &
         (mxe['upstreamES'] < mxe['2ndExonStart_0base']) & (mxe['2ndExonEnd'] < mxe['downstreamEE']))
print(f'(a) MXE rows {len(mxe)}: upstreamES..downstreamEE contains both alternative exons in {int(cover.sum())} of {len(mxe)} rows')
top_idx = list(mxe.sort_values('FDR').head(4).index)
top = mxe.loc[top_idx]
open(W / 'sig.MXE.MATS.JC.txt', 'w', newline='\n').write('\n'.join([raw[0]] + [raw[1 + i] for i in top_idx]) + '\n')
print('events:', list(zip(top.geneSymbol, top.chr, top.strand, top.FDR.round(4))))

rb = [f'{PUB}/rnasplice/bam/{s}.Aligned.out.bam' for s in ('ERR188383', 'ERR188428', 'ERR188454', 'ERR204916')]
tsv = W / 'groups.tsv'
open(tsv, 'w', newline='\n').write(''.join(f'{n}\t{b}\t{g}\n' for n, b, g in zip(('g1', 'g2', 'y1', 'y2'), rb, ('GBR', 'GBR', 'YRI', 'YRI'))))
open(W / 'palette.txt', 'w', newline='\n').write('#1f77b4\n#ff7f0e\n')
gtf = str(PUB / 'rnasplice/reference/genes_chrX.gtf')
for _, ev in top.iterrows():
    region = f'X:{max(1, ev["upstreamES"] - 500)}-{ev["downstreamEE"] + 500}'
    name = f'{ev["geneSymbol"]}_{ev["ID"]}'
    for fmt in ('svg', 'png'):
        cmd = ['ggsashimi.py', '-b', str(tsv), '-c', region, '-o', str(W / name), '-M', '1', '--shrink', '--fix-y-scale', '-O', '3', '-C', '3',
               '-P', str(W / 'palette.txt'), '-A', 'mean_j', '-g', gtf, '-F', fmt] + (['-R', '60', '--width', '8'] if fmt == 'png' else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        f = W / f'{name}.{fmt}'
        print(f'ggsashimi {name} {region} {fmt} rc={r.returncode} size={f.stat().st_size if f.exists() else "NONE"}')
    v = subprocess.run(['micromamba', 'run', '-n', 'as-core', 'python', str(RUN / 'scripts/jtruth.py'), region, str(tsv), '--M', '1', '--svg', str(W / f'{name}.svg')],
                       capture_output=True, text=True)
    print('   labels:', v.stdout.strip().splitlines()[-1] if v.stdout.strip() else v.stderr[-200:])
    (W / f'{name}.svg').unlink()

open(W / 'grouping.gf', 'w', newline='\n').write('GBR: 1-2\nYRI: 3-4\n')
r = subprocess.run(['rmats2sashimiplot', '--b1', f'{rb[0]},{rb[1]}', '--b2', f'{rb[2]},{rb[3]}', '--event-type', 'MXE', '-e', 'sig.MXE.MATS.JC.txt',
                    '--l1', 'GBR', '--l2', 'YRI', '-o', 'sashimi_rmats', '--exon_s', '1', '--intron_s', '5', '--group-info', 'grouping.gf',
                    '--color', '#1f77b4,#ff7f0e'], cwd=W, capture_output=True, text=True)
pdfs = sorted((W / 'sashimi_rmats/Sashimi_plot').glob('*.pdf')) if (W / 'sashimi_rmats/Sashimi_plot').exists() else []
print(f'rmats2sashimiplot MXE rc={r.returncode}; PDFs {len(pdfs)} of 4 (assert: {"OK" if len(pdfs) == 4 else "FAIL"})')
for p in pdfs:
    print('  pdf', p.stat().st_size, p.name[:80])
