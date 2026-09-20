#!/usr/bin/env python
"""SYNTHETIC planted-truth data for NEW inputs 6 and 7 (seed 7; NOT the pre-fix audit's data).
Reference planted.fa: ctgA 6000 bp (random uppercase + N run 1000-1029 + IUPAC R/Y at 2000/2001 + soft-masked 3000-3399),
ctgB 1500 bp (reads only in 200-699), ctgC 800 bp (no reads).  All coordinates 0-based below.
Sample haplotype on ctgA differs from the reference:
  HOM SNPs at 500, 2500, 3100 (inside the soft-mask) and 5999 (last base of the contig); het 50/50 at 700; het ~20% minor at 900
  2-bp deletion ref[4000:4002] carried by all reads; 3-bp insertion GTA after ref 4500 carried by all reads
  real bases (unknown to the reference) under the reference N run, A/C under the IUPAC R/Y
  coverage gap 1500..1799 (no reads); shallow zone 1800..1899 (depth 2); reads start at 0 and the last one ends at 6000
Decoys that a default pileup / samtools consensus must drop or down-weight: DUP- and SECONDARY-flagged reads with a wrong base at 500,
20 reads with a Q5 wrong base at 2700, 12 MAPQ-0 reads with a wrong base at 3700, soft-clipped garbage ends.
truth.json is computed here by walking each read's CIGAR in plain Python, not with pileup."""
import json, os, random, sys
from collections import Counter, defaultdict
import pysam
OUT = sys.argv[1] if len(sys.argv) > 1 else 'data/planted'
os.makedirs(OUT, exist_ok=True)
random.seed(7)
rnd = lambda n: ''.join(random.choice('ACGT') for _ in range(n))
A = list(rnd(6000)); B = rnd(1500); C = rnd(800)
for i in range(1000, 1030): A[i] = 'N'
A[2000], A[2001] = 'R', 'Y'
ref = ''.join(A)
nxt = {'A': 'C', 'C': 'G', 'G': 'T', 'T': 'A'}
sample = A[:]
sample[2000], sample[2001] = 'A', 'C'
for i in range(1000, 1030): sample[i] = random.choice('ACGT')
HOM = [500, 2500, 3100, 5999]
for p in HOM: sample[p] = nxt[ref[p]]
HET50, HET20 = 700, 900
DEL0, DELN, INS_AFTER, INS = 4000, 2, 4500, 'GTA'

def fa_text(name, s, w, mask=None):
    if mask: s = s[:mask[0]] + s[mask[0]:mask[1]].lower() + s[mask[1]:]
    return '>%s\n' % name + ''.join(s[i:i + w] + '\n' for i in range(0, len(s), w))
open(f'{OUT}/planted.fa', 'w', newline='\n').write(fa_text('ctgA', ref, 70, (3000, 3400)) + fa_text('ctgB', B, 60) + fa_text('ctgC', C, 80))
hdr = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'ctgA', 'LN': 6000}, {'SN': 'ctgB', 'LN': 1500}, {'SN': 'ctgC', 'LN': 800}]}

def make_read(start, qlen, tid=0):
    hap = sample if tid == 0 else list(B)
    seq, cig = [], []
    def push(op, n):
        if cig and cig[-1][0] == op: cig[-1] = (op, cig[-1][1] + n)
        else: cig.append((op, n))
    p = start
    while len(seq) < qlen and p < len(hap):
        if tid == 0 and p == DEL0 and start < DEL0:
            push(2, DELN); p += DELN; continue
        seq.append(hap[p]); push(0, 1)
        if tid == 0 and p == INS_AFTER and start <= INS_AFTER:
            if len(seq) + len(INS) < qlen:
                seq.extend(INS); push(1, len(INS))
            else:
                p += 1; break
        p += 1
    return dict(tid=tid, start=start, seq=''.join(seq), cig=cig, flag=0, mapq=60, quals=None, name=None)

reads = []
def add(r, name=None, flag=0, mapq=60, quals=None):
    r['name'] = name or 'r%05d' % len(reads); r['flag'] = flag; r['mapq'] = mapq; r['quals'] = quals; reads.append(r)

starts = list(range(0, 1401, 4)) + [s for s in range(1900, 5901, 4) if s not in (4000, 4001)] + [5900]
for s in starts:
    if s == 3996: pass
    add(make_read(s, 100))
add(make_read(1800, 100)); add(make_read(1801, 100))          # depth 2 in 1801..1899
# ---------------- het columns: replace the base in every 2nd / 5th read that covers the position with a fixed alt -------
def qpos(r, pos):
    p = r['start']; q = 0
    for op, ln in r['cig']:
        if op == 0:
            if p <= pos < p + ln: return q + pos - p
            p += ln; q += ln
        elif op == 1: q += ln
        elif op == 2: p += ln
        elif op == 4: q += ln
    return None
def het(pos, every):
    k = 0
    for r in reads:
        if r['tid'] != 0 or r['flag']: continue
        qi = qpos(r, pos)
        if qi is None: continue
        k += 1
        if k % every == 0:
            s = list(r['seq']); s[qi] = nxt[s[qi]]; r['seq'] = ''.join(s)
het(HET50, 2); het(HET20, 5)
# ---------------- decoys -----------------------------------------------------------------------------------------------
def decoy(pos, flag=0, mapq=60, q=40, count=1):
    for k in range(count):
        r = make_read(pos - 30, 100); qi = qpos(r, pos)
        s = list(r['seq']); s[qi] = {'A': 'T', 'C': 'A', 'G': 'C', 'T': 'G'}[s[qi]]; r['seq'] = ''.join(s)
        add(r, name='dec_%d_%d_%d_%d_%d' % (pos, flag, mapq, q, k), flag=flag, mapq=mapq, quals=[(q if i == qi else 40) for i in range(len(r['seq']))])
decoy(500, flag=1024, count=30); decoy(500, flag=256, count=30)
decoy(2700, q=5, count=20); decoy(3700, mapq=0, count=12)
for k in range(6):
    r = make_read(4990 + k, 80)
    r['seq'] = 'TTTTTTTTTT' + r['seq'] + 'GGGGGGGGGG'; r['cig'] = [(4, 10)] + r['cig'] + [(4, 10)]
    add(r, name='sc_%d' % k)
for s in range(200, 601, 5): add(make_read(s, 100, tid=1))
# ---------------- write ---------------------------------------------------------------------------------------------
with pysam.AlignmentFile(f'{OUT}/planted.unsorted.bam', 'wb', header=hdr) as out:
    for r in reads:
        a = pysam.AlignedSegment(out.header)
        a.query_name = r['name']; a.query_sequence = r['seq']; a.flag = r['flag']; a.reference_id = r['tid']
        a.reference_start = r['start']; a.mapping_quality = r['mapq']; a.cigartuples = r['cig']
        qs = r['quals'] or [40] * len(r['seq'])
        a.query_qualities = pysam.qualitystring_to_array(''.join(chr(33 + q) for q in qs)); out.write(a)
pysam.sort('-o', f'{OUT}/planted.bam', f'{OUT}/planted.unsorted.bam'); pysam.index(f'{OUT}/planted.bam'); os.remove(f'{OUT}/planted.unsorted.bam')
# ---------------- independent truth (cigar walk, what pysam.pileup() defaults keep) --------------------------------------
cnt = defaultdict(Counter)
for r in reads:
    if r['flag'] & (4 | 256 | 512 | 1024) or r['tid'] != 0: continue
    p = r['start']; qi = 0
    for op, ln in r['cig']:
        if op == 0:
            for j in range(ln):
                qv = r['quals'][qi + j] if r['quals'] else 40
                if qv >= 13: cnt[p + j][r['seq'][qi + j].upper()] += 1
            p += ln; qi += ln
        elif op in (1, 4): qi += ln
        elif op == 2: p += ln
MIN = 3
depth = [sum(cnt[i].values()) for i in range(6000)]
ties = [i for i in range(6000) if len(cnt[i]) > 1 and cnt[i].most_common(2)[0][1] == cnt[i].most_common(2)[1][1]]
pysam_truth = ''.join((cnt[i].most_common(1)[0][0] if depth[i] >= MIN else 'N') for i in range(6000))
json.dump({'ref': ref, 'sample': ''.join(sample), 'pysam_truth': pysam_truth, 'depth': depth, 'ties': ties, 'HOM': HOM, 'HET50': HET50, 'HET20': HET20,
           'DEL': [DEL0, DELN], 'INS_AFTER': INS_AFTER, 'INS': INS, 'B': B, 'C': C, 'nreads': len(reads),
           'counts': {str(i): dict(cnt[i]) for i in (500, 700, 900, 2500, 2700, 3700, 5999)}}, open(f'{OUT}/truth.json', 'w'))
print('reads', len(reads), 'ties', ties[:10])
print('depth at 0,500,700,900,1000,1499,1500,1750,1850,2700,3700,3999,4000,4002,5999:', [depth[i] for i in (0, 500, 700, 900, 1000, 1499, 1500, 1750, 1850, 2700, 3700, 3999, 4000, 4002, 5999)])
print('counts:', {i: dict(cnt[i]) for i in (500, 700, 900, 2700, 3700)})
