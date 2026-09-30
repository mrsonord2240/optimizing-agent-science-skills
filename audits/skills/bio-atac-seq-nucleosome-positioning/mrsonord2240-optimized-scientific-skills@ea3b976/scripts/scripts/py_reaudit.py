"""Independent re-audit checks of vplot.py and estimate_nrl.py on real GM12878 chr1 data (own implementations, not the fixer's)."""
import os, sys, subprocess, collections
import numpy as np, pysam
SK = os.environ['SKILL']; D = os.environ['ATACDATA']; OUT = '/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/reaudit-run/out'
BAM = f'{D}/encode/GM12878_rep1_filtered.chr1_1-30000000.bam'
BAM2 = f'{D}/encode/GM12878_rep2_filtered.chr1_1-30000000.bam'
K562 = f'{D}/encode/K562_rep1_filtered.chr1_1-30000000.bam'
TSS = f'{D}/annotation/gencode_v29_protein_coding_tss.chr1.bed'
def run(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True); return p.returncode, (p.stdout + p.stderr).strip()
res = []
def chk(name, ok, note=''):
    res.append(ok); print(('PASS' if ok else 'FAIL'), name, note, flush=True)

# ---- estimate_nrl
def indep_mode(bam):
    L = []
    with pysam.AlignmentFile(bam) as b:
        for r in b.fetch():
            if r.is_paired and r.is_proper_pair and r.template_length > 0 and 150 <= r.template_length <= 250: L.append(r.template_length)
    c = np.bincount(L, minlength=251)
    return int(np.argmax(c)), len(L)
for nm, b in [('GM12878 rep1', BAM), ('GM12878 rep2', BAM2), ('K562 rep1', K562)]:
    rc, o = run([f'{SK}/scripts/estimate_nrl.py', b]); m, n = indep_mode(b)
    v = float(o.split(':')[1].split('bp')[0]) if rc == 0 else None
    print(nm, rc, o, 'independent 1bp mode', m, 'n', n)
    chk(f'estimate_nrl {nm} rc0 and within 6 bp of independent mode', rc == 0 and abs(v - m) <= 6, f'{v} vs {m}')
# NFR-only BAM (fragments <100): must fail with message, no traceback
nfr = f'{OUT}/nfr_only.bam'
with pysam.AlignmentFile(BAM) as i, pysam.AlignmentFile(nfr, 'wb', template=i) as o:
    for r in i.fetch('chr1', 10_000_000, 12_000_000):
        if r.is_proper_pair and 0 < abs(r.template_length) < 100: o.write(r)
pysam.index(nfr)
rc, o = run([f'{SK}/scripts/estimate_nrl.py', nfr]); print(rc, o)
chk('estimate_nrl NFR-only BAM: rc!=0, actionable message, no Traceback', rc != 0 and 'no fragment-size peak' in o and 'Traceback' not in o)
# single-end BAM
se = f'{OUT}/single_end.bam'
with pysam.AlignmentFile(BAM) as i, pysam.AlignmentFile(se, 'wb', template=i) as o:
    for k, r in enumerate(i.fetch('chr1', 10_000_000, 10_500_000)):
        r.flag &= ~(1 | 2 | 8 | 64 | 128 | 32); r.template_length = 0; r.next_reference_id = -1; r.next_reference_start = -1; o.write(r)
pysam.index(se)
rc, o = run([f'{SK}/scripts/estimate_nrl.py', se]); print(rc, o)
chk('estimate_nrl single-end BAM: rc!=0, clear message', rc != 0 and 'paired-end' in o and 'Traceback' not in o)
rc, o = run([f'{SK}/scripts/estimate_nrl.py']); chk('estimate_nrl no args prints usage (rc!=0)', rc != 0 and 'Usage' in o)

# ---- vplot
sys.path.insert(0, f'{SK}/scripts'); import vplot as V
rows = [l.rstrip('\n').split('\t') for l in open(TSS)]
sel = rows[100:400]   # 300 TSS, both strands
bed6 = f'{OUT}/tss300.bed'; open(bed6, 'w').write('\n'.join('\t'.join(r[:6]) for r in sel) + '\n')
bed3 = f'{OUT}/tss300_nostrand.bed'; open(bed3, 'w').write('\n'.join('\t'.join(r[:3]) for r in sel) + '\n')
print('strands', collections.Counter(r[5] for r in sel))
g, n = V.vplot(BAM, bed6)
chk('vplot n_features == 300', n == 300, str(n))
# independent recount: count each proper pair once via the leftmost mate (tlen>0, read1 or read2), size<600, center within +-1000 of TSS
tot = 0; nfrc = 0; nfrf = 0
with pysam.AlignmentFile(BAM) as b:
    for r in sel:
        c = int(r[1]); m = r[5] == '-'
        for a in b.fetch(r[0], max(0, c - 1000), c + 1000):
            if a.is_proper_pair and a.template_length > 0 and a.template_length < 600:
                cen = a.reference_start + a.template_length // 2 - c
                if -1000 <= cen < 1000:
                    tot += 1
                    if a.template_length < 100:
                        if abs(cen) <= 50: nfrc += 1
                        elif 200 <= abs(cen) <= 400: nfrf += 1
tot_g = g.sum() * n
print('grid total', tot_g, 'independent recount (leftmost-mate, fetch-window)', tot)
chk('vplot grid total within 1% of independent recount', abs(tot_g - tot) / tot < 0.01)
sz = np.arange(600)
nfr_c = g[:100, 950:1051].sum() / 101; nfr_f = (g[:100, 600:800].sum() + g[:100, 1200:1400].sum()) / 400
print('NFR density centre/flank', nfr_c / nfr_f)
chk('NFR enriched at TSS centre >2x flank', nfr_c / nfr_f > 2, f'{nfr_c/nfr_f:.2f}')
# strand orientation: mono nucleosome (180-247) downstream(+50..+300)/upstream(-300..-50)
def ratio(gr): return gr[180:248, 1050:1300].sum() / gr[180:248, 700:950].sum()
gp, npl = V.vplot(BAM, (lambda f: (open(f, 'w').write('\n'.join('\t'.join(r[:6]) for r in sel if r[5] == '+') + '\n'), f)[1])(f'{OUT}/tss_plus.bed'))
gm, nmi = V.vplot(BAM, (lambda f: (open(f, 'w').write('\n'.join('\t'.join(r[:6]) for r in sel if r[5] == '-') + '\n'), f)[1])(f'{OUT}/tss_minus.bed'))
g3, _ = V.vplot(BAM, bed3)
rp, rm, rall, r3 = ratio(gp), ratio(gm), ratio(g), ratio(g3)
print('down/up mono ratio plus', rp, 'minus (mirrored)', rm, 'pooled strand-aware', rall, 'pooled ignoring strand', r3)
chk('minus-strand mirrored: both strands show same polarity (ratio<1 both or >1 both) and within 2x of each other', (rp - 1) * (rm - 1) > 0 and 0.5 < rp / rm < 2, f'{rp:.2f} {rm:.2f}')
chk('strand-aware pooled differs from strand-ignored pooling (strand column used)', abs(rall - r3) > 0.1, f'{rall:.2f} vs {r3:.2f}')
# raw independent polarity in genome coords for plus vs minus
# CLI
rc, o = run([f'{SK}/scripts/vplot.py', BAM, bed6, f'{OUT}/vplot_reaudit.png']); chk('vplot CLI rc0 + PNG written', rc == 0 and os.path.getsize(f'{OUT}/vplot_reaudit.png') > 20000, o[:200])
badbed = f'{OUT}/bad.bed'; open(badbed, 'w').write('chrZZ\t1000\t1001\tx\t0\t+\n')
rc, o = run([f'{SK}/scripts/vplot.py', BAM, badbed, f'{OUT}/bad.png']); print(rc, o)
chk('vplot unknown chromosome: rc!=0, clear message, no PNG', rc != 0 and 'no BED rows' in o and 'Traceback' not in o and not os.path.exists(f'{OUT}/bad.png'))
mix = f'{OUT}/mixed.bed'; open(mix, 'w').write('chrZZ\t1000\t1001\tx\t0\t+\n' + open(bed6).read())
gm2, n2 = V.vplot(BAM, mix); chk('vplot skips unknown-chrom rows but keeps valid ones', n2 == 300)
rc, o = run([f'{SK}/scripts/vplot.py']); chk('vplot no args prints usage', rc != 0 and 'Usage' in o)
print('SUMMARY', sum(res), '/', len(res))
