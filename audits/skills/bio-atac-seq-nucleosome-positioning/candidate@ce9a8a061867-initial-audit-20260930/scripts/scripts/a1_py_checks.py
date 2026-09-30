"""Audit checks for vplot.py and estimate_nrl.py on real ENCODE GM12878 rep1 chr1:1-30Mb (ENCFF415FEC) + GENCODE v29 chr1 TSS.
Independent expectations are computed here; the Skill scripts are imported unmodified (PYTHONDONTWRITEBYTECODE=1)."""
import importlib.util, os, sys
import numpy as np, pysam
from scipy.signal import find_peaks

S = os.environ['SKILL']; D = os.environ['ATACDATA']
OUT = '/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930/out'
bam = f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam'
res = []


def chk(name, ok, info=''):
    res.append(bool(ok)); print(('PASS' if ok else 'FAIL'), name, info, flush=True)


def load(n):
    sp = importlib.util.spec_from_file_location(n, f'{S}/scripts/{n}.py'); m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m); return m


# ---------------- estimate_nrl.py ----------------
nrl = load('estimate_nrl')
try:
    v = nrl.estimate_nrl(bam); ok = 150 < v < 250
    info = f'{v}'
except Exception as e:
    ok = False; info = repr(e)
chk('estimate_nrl returns a 150-250 bp NRL on real ATAC', ok, info)
L = np.array([abs(r.template_length) for r in pysam.AlignmentFile(bam, 'rb').fetch() if r.is_proper_pair and r.is_read1 and 0 < abs(r.template_length) < 1500])
h, e = np.histogram(L, bins=300, range=(0, 1500))
ctr = e[:-1] + 2.5
print('histogram bin width 5 bp; max bin', ctr[h.argmax()], 'count', h.max())
# Root-cause probe: find_peaks(distance=50) is in BINS (=250 bp), not bp
for dist, prom in [(50, 0.05), (10, 0.05), (10, 0.02), (10, 0.0)]:
    p, _ = find_peaks(h, distance=dist, prominence=h.max() * prom)
    print(f'distance={dist} bins ({dist*5} bp) prominence={prom}: peaks(bp)', (ctr[p]).tolist())
p, _ = find_peaks(h, distance=10, prominence=h.max() * 0.05)
pk = ctr[p]; mono = pk[(pk > 150) & (pk < 250)]
chk('with distance=10 bins (50 bp) a 150-250 bp peak is found (same data, same prominence)', len(mono) == 1, str(mono.tolist()))
sm = np.convolve(np.bincount(L, minlength=1500)[:1500], np.ones(9) / 9, mode='same'); mode = 150 + int(np.argmax(sm[150:250]))
print('independent smoothed mono mode', mode)
chk('distance=10 estimate within 15 bp of independent mono mode', len(mono) == 1 and abs(mono[0] - mode) < 15, f'{mono.tolist()} vs {mode}')
# di-nucleosome peak exists (2x NRL relation from the Skill text)
print('INFO di-nucleosome peak (315-473) at 5%% prominence:', ((pk > 315) & (pk < 473)).any(), '(informational, not an assertion; visible at prominence 0)')

# ---------------- vplot.py ----------------
vp = load('vplot')
tss = [l.rstrip('\n').split('\t') for l in open(f'{D}/annotation/gencode_v29_protein_coding_tss.chr1.bed')]
tss = [t for t in tss if 1_200_000 < int(t[1]) < 29_000_000][:300]
plus = [t for t in tss if t[5] == '+']; minus = [t for t in tss if t[5] == '-']
print('TSS', len(tss), 'plus', len(plus), 'minus', len(minus))
os.makedirs(OUT, exist_ok=True)
bed = f'{OUT}/a1_tss300.bed'; open(bed, 'w').write('\n'.join('\t'.join(t) for t in tss) + '\n')
g = vp.vplot(bam, bed)


def corrected(tss_rows, flank=1000, max_size=600, strand_aware=False):
    """Independent V-plot: true fragment centre (leftmost mate start + size/2), optional TSS strand flip."""
    bf = pysam.AlignmentFile(bam, 'rb'); grid = np.zeros((max_size, 2 * flank))
    for t in tss_rows:
        c = int(t[1]); sgn = -1 if (strand_aware and t[5] == '-') else 1
        for r in bf.fetch(t[0], max(0, c - flank - 300), c + flank + 300):
            if not (r.is_proper_pair and r.is_read1): continue
            size = abs(r.template_length)
            if not 0 < size < max_size: continue
            left = min(r.reference_start, r.next_reference_start)
            x = sgn * (left + size // 2 - c) + flank
            if 0 <= x < 2 * flank: grid[size, int(x)] += 1
    return grid


# (1) read1-only centring: how many read1 are reverse-strand (their reference_start is the fragment's right end - read length)
bf = pysam.AlignmentFile(bam, 'rb'); rev = tot = 0
for r in bf.fetch('chr1', 1_000_000, 3_000_000):
    if r.is_proper_pair and r.is_read1 and 0 < abs(r.template_length) < 600:
        tot += 1; rev += r.is_reverse
print(f'read1 reverse fraction {rev/tot:.3f} of {tot}')
gc = corrected(tss)
print('script grid total', int(g.sum()), 'corrected-centre grid total', int(gc.sum()))
# Positional shift of the size-190 (mono) band: mean |offset| between script centre and true centre for reverse read1
offs = []
for r in bf.fetch('chr1', 1_000_000, 2_000_000):
    if r.is_proper_pair and r.is_read1 and 180 <= abs(r.template_length) < 250:
        size = abs(r.template_length); script_c = r.reference_start + size // 2; true_c = min(r.reference_start, r.next_reference_start) + size // 2
        offs.append(script_c - true_c)
offs = np.array(offs)
print(f'mono read1: fraction with centre error != 0 = {np.mean(offs != 0):.3f}; median |error| among those = {np.median(np.abs(offs[offs != 0])):.0f} bp')
chk('vplot.py fragment centre equals true fragment centre for >=99% of mono read1', np.mean(offs == 0) >= 0.99, f'{np.mean(offs == 0):.3f} exact')
# (2) how much of the mass sits in the wrong place: NFR TSS enrichment with true centre vs script
def enrich(gr):
    nfr = gr[30:100].sum(axis=0); return nfr[900:1100].mean() / np.r_[nfr[:200], nfr[1800:]].mean()
print('NFR centre/flank script %.2f corrected %.2f' % (enrich(g), enrich(gc)))
# (3) strand handling: +1 nucleosome (downstream) should appear on opposite sides for plus vs minus TSS
gp = corrected(plus); gm = corrected(minus)
def side(gr):
    mono = gr[180:248].sum(axis=0); return mono[1050:1300].sum() / max(1, mono[700:950].sum())  # downstream(+) / upstream(-)
print('mono downstream/upstream ratio: plus-strand TSS %.2f, minus-strand TSS %.2f' % (side(gp), side(gm)))
chk('plus and minus TSS show opposite mono asymmetry (so strand-unaware pooling blurs +1/-1)', (side(gp) - 1) * (side(gm) - 1) < 0, f'{side(gp):.2f} {side(gm):.2f}')
gsa = corrected(tss, strand_aware=True)
print('pooled(strand-unaware) ratio %.2f ; strand-aware ratio %.2f' % (side(corrected(tss)), side(gsa)))
chk('strand-unaware pooling cancels a strong gene-sense asymmetry (|log ratio| strand-aware > 2x unaware)', abs(np.log(side(gsa))) > 2 * abs(np.log(side(corrected(tss)))), f'{side(gsa):.2f} vs {side(corrected(tss)):.2f}')

# (4) backend
import subprocess
env = dict(os.environ); env.pop('MPLBACKEND', None); env['QT_QPA_PLATFORM'] = ''
p = subprocess.run([sys.executable, f'{S}/scripts/vplot.py', bam, bed, f'{OUT}/a1_vplot_scriptcli.png'], capture_output=True, text=True, env=env)
print('vplot.py CLI without MPLBACKEND rc', p.returncode, p.stderr.strip()[-200:])
# render the corrected strand-aware plot for visual comparison
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
for a, gr, t in zip(ax, [g, gsa], ['Skill vplot.py (read1 start, strand-unaware)', 'corrected centre + strand-aware']):
    a.imshow(np.log1p(gr), aspect='auto', origin='lower', cmap='magma', extent=[-1000, 1000, 0, 600]); a.set_title(t, fontsize=9); a.set_xlabel('Distance from TSS (bp)')
ax[0].set_ylabel('Fragment size (bp)'); plt.savefig(f'{OUT}/a1_vplot_compare.png', dpi=130, bbox_inches='tight')
print('SUMMARY', sum(res), '/', len(res))
