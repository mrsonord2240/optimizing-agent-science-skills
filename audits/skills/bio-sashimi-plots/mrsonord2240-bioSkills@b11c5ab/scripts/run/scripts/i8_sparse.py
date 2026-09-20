#!/usr/bin/env python3
"""Input 8 (NEW, edge): low-junction-count real region (DMD SE event on chrX, minus strand, per-sample counts 0-3 reads).
The Skill recommends raising -M to declutter (5-10) and documents that --shrink crashes when no junction passes -M.
(a) -M 1 --shrink: labels vs pysam (half-to-even rounding of .5 means). (b) -M 5 --shrink: crash documented? (c) -M 5 without --shrink.
(d) examples/plot_sashimi.py plot_specific_event (its hard-coded min_junc=5) on the same event. (e) -s SENSE on paired-end BAMs? skipped (MATE*_SENSE run in Input 4 style)."""
import os, pathlib, shutil, subprocess, sys
RUN = pathlib.Path('/mnt/openscience/audits/bio-sashimi-plots/run')
PUB = pathlib.Path('/mnt/openscience/audit-envs/alternative-splicing/public-data')
W = RUN / 'out' / 'i8'
shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True); os.chdir(W)
rb = [f'{PUB}/rnasplice/bam/{s}.Aligned.out.bam' for s in ('ERR188383', 'ERR188428', 'ERR188454', 'ERR204916')]
open('groups.tsv', 'w', newline='\n').write(''.join(f'{n}\t{b}\t{g}\n' for n, b, g in zip(('g1', 'g2', 'y1', 'y2'), rb, ('GBR', 'GBR', 'YRI', 'YRI'))))
open('palette.txt', 'w', newline='\n').write('#1f77b4\n#ff7f0e\n')
gtf = str(PUB / 'rnasplice/reference/genes_chrX.gtf')
region = 'X:31136844-31152811'   # DMD SE event 31137344-31152311 +/- 500 (Skill recipe)


def gg(name, M, shrink, fmt='svg'):
    cmd = ['ggsashimi.py', '-b', 'groups.tsv', '-c', region, '-o', name, '-M', str(M), '-O', '3', '-C', '3', '-P', 'palette.txt', '-A', 'mean_j', '-g', gtf, '-F', fmt, '--fix-y-scale']
    if shrink:
        cmd.append('--shrink')
    if fmt == 'png':
        cmd += ['-R', '60', '--width', '8']
    r = subprocess.run(cmd, capture_output=True, text=True)
    f = pathlib.Path(f'{name}.{fmt}')
    err = [l for l in r.stderr.splitlines() if 'StopIteration' in l or 'RuntimeError' in l][:1]
    print(f'{name}: M={M} shrink={shrink} rc={r.returncode} file={"%d B" % f.stat().st_size if f.exists() else "NONE"} {err}')
    return f


def truth(svg, M):
    v = subprocess.run(['micromamba', 'run', '-n', 'as-core', 'python', str(RUN / 'scripts/jtruth.py'), region, 'groups.tsv', '--M', str(M), '--svg', svg],
                       capture_output=True, text=True)
    print(v.stdout.strip() or v.stderr[-300:])


gg('a_M1', 1, True); truth('a_M1.svg', 1)
gg('a_M1_png', 1, True, 'png')
gg('b_M5_shrink', 5, True)
gg('c_M5_noshrink', 5, False); truth('c_M5_noshrink.svg', 5)
gg('c_M5_noshrink_png', 5, False, 'png')
# (d) the example's plot_specific_event (min_junc 5)
sys.path.insert(0, str(RUN / 'skill/examples')); sys.dont_write_bytecode = True
import plot_sashimi as ps
try:
    out = ps.plot_specific_event('groups.tsv', gtf, 'chrX', 31137344, 31152311, 'd_specific', flank=500)
    print('plot_specific_event ->', out, [os.path.getsize(o) for o in out])
except Exception as e:
    print('plot_specific_event RAISED', type(e).__name__, e)
for f in pathlib.Path('.').glob('*.svg'):
    f.unlink()
