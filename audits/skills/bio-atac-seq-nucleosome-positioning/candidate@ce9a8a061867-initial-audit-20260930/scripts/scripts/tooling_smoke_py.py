"""Smoke: vplot.py + estimate_nrl.py on real GM12878 rep1 (chr1:1-30Mb) + GENCODE v29 chr1 TSS. Asserts values."""
import importlib.util, os, sys, collections
import numpy as np, pysam
S = os.environ['SKILL']; D = os.environ['ATACDATA']; OUT = os.environ['OUT']
bam = f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam'
def load(n):
    sp = importlib.util.spec_from_file_location(n, f'{S}/scripts/{n}.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
res = []
def chk(name, ok, info=''):
    res.append(ok); print(('PASS' if ok else 'FAIL'), name, info, flush=True)

# TSS subset: first 300 protein-coding TSS in chr1:1.2-29Mb (BED start = TSS, strand column kept)
tss = [l.rstrip('\n').split('\t') for l in open(f'{D}/annotation/gencode_v29_protein_coding_tss.chr1.bed')]
tss = [t for t in tss if 1_200_000 < int(t[1]) < 29_000_000][:300]
print('TSS rows', len(tss), tss[0])
os.makedirs(OUT, exist_ok=True)
bed = f'{OUT}/tss300.bed'; open(bed, 'w').write('\n'.join('\t'.join(t) for t in tss) + '\n')

v = load('vplot')
g = v.vplot(bam, bed)
chk('vplot grid shape (600,2000)', g.shape == (600, 2000), str(g.shape))
# independent recount with the same definition
bf = pysam.AlignmentFile(bam, 'rb'); tot = 0
for t in tss:
    c = int(t[1])
    for r in bf.fetch(t[0], max(0, c - 1000), c + 1000):
        if r.is_proper_pair and r.is_read1 and 0 < abs(r.template_length) < 600:
            x = r.reference_start + abs(r.template_length) // 2 - c + 1000
            if 0 <= x < 2000: tot += 1
chk('vplot total == independent recount', int(g.sum()) == tot, f'{int(g.sum())} vs {tot}')
sizes = g.sum(axis=1)
chk('vplot has NFR (<100) and mono (180-247) mass', sizes[:100].sum() > 0 and sizes[180:248].sum() > 0, f'nfr={sizes[:100].sum():.0f} mono={sizes[180:248].sum():.0f}')
# TSS enrichment of NFR fragments: centre +-100 vs flank 800-1000
nfr = g[30:100].sum(axis=0); cen = nfr[900:1100].mean(); fl = np.r_[nfr[:200], nfr[1800:]].mean()
chk('NFR fragments enriched at TSS centre vs flanks', cen / fl > 2, f'{cen/fl:.2f}')
# strand caveat: how many rows are minus strand (script ignores strand)
minus = sum(1 for t in tss if t[5] == '-') if len(tss[0]) > 5 else -1
print('INFO minus-strand TSS in set (vplot.py ignores strand):', minus, 'of', len(tss))
# minus-strand asymmetry check: mono signal downstream (+) vs upstream (-) for plus vs minus TSS separately
def half(strand):
    sub = [t for t in tss if t[5] == strand]
    gg = v.vplot(bam, '/dev/stdin' if False else bed)  # placeholder not used
    return None
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.imshow(g, aspect='auto', origin='lower', cmap='magma', extent=[-1000, 1000, 0, 600]); plt.xlabel('Distance from feature (bp)'); plt.ylabel('Fragment size (bp)')
plt.savefig(f'{OUT}/vplot_tss300.png', dpi=200, bbox_inches='tight')
chk('png written', os.path.getsize(f'{OUT}/vplot_tss300.png') > 10000)
# CLI form
import subprocess
p = subprocess.run([sys.executable, f'{S}/scripts/vplot.py', bam, bed, f'{OUT}/vplot_cli.png'], capture_output=True, text=True)
chk('vplot.py CLI rc0 + png', p.returncode == 0 and os.path.getsize(f'{OUT}/vplot_cli.png') > 10000, p.stderr[-200:])
p = subprocess.run([sys.executable, f'{S}/scripts/vplot.py'], capture_output=True, text=True)
chk('vplot.py no-arg usage exit nonzero', p.returncode != 0)

n = load('estimate_nrl')
try:
    nrl = n.estimate_nrl(bam)
except IndexError as e:
    nrl = float('nan'); print('FAIL estimate_nrl() raised IndexError on real GM12878 chr1 slice (no peak in 150-250 with 5%-of-max prominence); see probe_nrl.py')
    res.append(False)
# independent: mode of 150-250 fragment lengths, smoothed
L = np.array([abs(r.template_length) for r in pysam.AlignmentFile(bam, 'rb').fetch('chr1', 1_000_000, 8_000_000) if r.is_proper_pair and r.is_read1 and 0 < abs(r.template_length) < 1500])
h = np.bincount(L, minlength=1500)[:1500]
sm = np.convolve(h, np.ones(9) / 9, mode='same'); mono_mode = 150 + int(np.argmax(sm[150:250]))
chk('NRL estimate in 150-250 and within 20 bp of independent mono mode', (not np.isnan(nrl)) and 150 < nrl < 250 and abs(nrl - mono_mode) < 20, f'nrl={nrl:.0f} mode={mono_mode}')
p = subprocess.run([sys.executable, f'{S}/scripts/estimate_nrl.py', bam], capture_output=True, text=True)
print(p.stdout.strip(), p.stderr[-200:]); chk('estimate_nrl.py CLI', p.returncode == 0 and 'Estimated NRL' in p.stdout)
# failure guard: planted BAM (uniform, no periodicity) -> documented behaviour?
p = subprocess.run([sys.executable, f'{S}/scripts/estimate_nrl.py', f'{D}/derived/planted_peaks.bam'], capture_output=True, text=True)
print('planted BAM rc', p.returncode, (p.stderr.strip().splitlines() or [''])[-1])
print('INFO planted-BAM failure is an IndexError traceback, not a message' if 'IndexError' in p.stderr else 'INFO planted: ' + p.stdout.strip())
print('SUMMARY', sum(res), '/', len(res))
