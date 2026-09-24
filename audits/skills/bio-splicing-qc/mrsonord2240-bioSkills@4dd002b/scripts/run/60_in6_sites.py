"""Input 6a: MaxEntScan on REAL annotated chrX (GRCh37) donors/acceptors vs decoys, via the Skill's helper score_splice_sites.
Independent of the fixer's script (written from scratch). Usage (as-maxent): python 60_in6_sites.py <examples dir> <gtf> <fasta>"""
import sys, random, math, collections
sys.path.insert(0, sys.argv[1]); import splicing_qc as sq
import pysam
gtf, fa = sys.argv[2], sys.argv[3]
g = pysam.FastaFile(fa)
tx = collections.defaultdict(list); strand = {}
for line in open(gtf):
    f = line.rstrip('\n').split('\t')
    if len(f) < 9 or f[2] != 'exon': continue
    tid = f[8].split('transcript_id "')[1].split('"')[0]
    tx[tid].append((f[0], int(f[3]) - 1, int(f[4]))); strand[tid] = f[6]
comp = str.maketrans('ACGTacgt', 'TGCAtgca')
def rc(s): return s.translate(comp)[::-1]
don, acc, seen = [], [], set()
for tid, ex in tx.items():
    ex.sort(); c = ex[0][0]
    for (c1, s1, e1), (c2, s2, e2) in zip(ex, ex[1:]):
        # intron = [e1, s2). + strand: donor at e1 (exon3 + intron6), acceptor at s2 (intron20 + exon3)
        if (c, e1, s2) in seen: continue
        seen.add((c, e1, s2))
        if strand[tid] == '+':
            d = g.fetch(c, e1 - 3, e1 + 6); a = g.fetch(c, s2 - 20, s2 + 3)
        else:
            d = rc(g.fetch(c, s2 - 6, s2 + 3)); a = rc(g.fetch(c, e1 - 3, e1 + 20))
        don.append(d.upper()); acc.append(a.upper())
print('unique annotated introns:', len(don))
gt = [i for i, d in enumerate(don) if d[3:5] == 'GT']; nongt = [i for i, d in enumerate(don) if d[3:5] != 'GT']
ag = [i for i, a in enumerate(acc) if a[18:20] == 'AG']
s5, _ = sq.score_splice_sites(don, [])
_, s3 = sq.score_splice_sites([], acc)
import numpy as np
s5 = np.array(s5); s3 = np.array(s3)
gtv = s5[gt]; gtv = gtv[~np.isnan(gtv)]
print('annotated GT donors n=%d  >8: %.1f%%  5-8: %.1f%%  <5: %.1f%%  median %.2f' % (len(gtv), 100 * (gtv > 8).mean(), 100 * ((gtv >= 5) & (gtv <= 8)).mean(), 100 * (gtv < 5).mean(), np.median(gtv)))
ngv = s5[nongt]; ngv = ngv[~np.isnan(ngv)]
print('annotated non-GT donors n=%d  <5: %.1f%%' % (len(ngv), 100 * (ngv < 5).mean()))
agv = s3[ag]; agv = agv[~np.isnan(agv)]
print('annotated AG acceptors n=%d  >8: %.1f%%  <5: %.1f%%  median %.2f' % (len(agv), 100 * (agv > 8).mean(), 100 * (agv < 5).mean(), np.median(agv)))
# decoys: random intronic GT / AG (>= 30 nt from any annotated splice site), plus-strand sequence, 88 donors like the fixer? use 2000 of each
random.seed(20260920)
sites = set()
for tid, ex in tx.items():
    for (c1, s1, e1), (c2, s2, e2) in zip(sorted(ex), sorted(ex)[1:]): sites.add(e1); sites.add(s2)
sites = sorted(sites)
import bisect
def far(p): i = bisect.bisect(sites, p); return all(abs(sites[j] - p) > 30 for j in (i - 1, i) if 0 <= j < len(sites))
dd, da = [], []
first = min(e[0][1] for e in tx.values()); last = max(e[-1][2] for e in tx.values())
while len(dd) < 2000 or len(da) < 2000:
    p = random.randint(first + 100, last - 100)
    if not far(p): continue
    w = g.fetch('X', p - 3, p + 6).upper()
    if w[3:5] == 'GT' and len(dd) < 2000: dd.append(w)
    w2 = g.fetch('X', p - 20, p + 3).upper()
    if w2[18:20] == 'AG' and len(da) < 2000: da.append(w2)
sd5, _ = sq.score_splice_sites(dd, []); _, sd3 = sq.score_splice_sites([], da)
def auc(pos, neg):
    pos, neg = np.array(pos), np.array(neg)
    allv = np.concatenate([pos, neg]); ranks = allv.argsort().argsort() + 1
    return (ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
print('decoy GT donors n=%d  <5: %.1f%%  ; AUC annotated vs decoy donor %.3f' % (len(dd), 100 * (np.array(sd5) < 5).mean(), auc(gtv, sd5)))
print('decoy AG acceptors n=%d  <5: %.1f%% ; AUC annotated vs decoy acceptor %.3f' % (len(da), 100 * (np.array(sd3) < 5).mean(), auc(agv, sd3)))
# helper edge cases
print('helper alignment:', sq.score_splice_sites(['CAGGTAAGT', 'CAGGTAA', 'NAGGTAAGT', 'cagataagt'], ['TTTTTTTTTTTTTTCCTTAGGAG', 'T' * 20 + 'CAG', 'x' * 23]))
