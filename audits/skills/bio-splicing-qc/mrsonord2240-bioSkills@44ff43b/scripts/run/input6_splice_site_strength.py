#!/usr/bin/env python
"""
Input 6 (scope boundary): splice-site strength with MaxEntScan (SKILL.md + examples/splicing_qc.py::score_splice_sites) on
REAL annotated chrX splice sites (Ensembl GRCh37 GTF + X.fa) vs GT/AG decoys, plus input-validation behaviour.
Run: asenv as-maxent python input6_splice_site_strength.py
"""
import sys, os, json, random, math
from collections import defaultdict
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
W = f'{RUN}/work/in6'
os.makedirs(W, exist_ok=True)
sys.path.insert(0, f'{RUN}/skill_copy/examples')
import splicing_qc as sq
import pysam
from maxentpy.maxent import score5, score3
import numpy as np
random.seed(20260920)

fa = pysam.FastaFile(f'{AS}/derived/X.fa')
COMP = str.maketrans('ACGTacgtN', 'TGCAtgcaN')
def rc(s): return s.translate(COMP)[::-1]

# ---- annotated introns from GTF (transcript order, strand-aware)
tx = defaultdict(list); strand = {}
for l in open(f'{AS}/rnasplice/reference/genes_chrX.gtf'):
    f = l.rstrip('\n').split('\t')
    if len(f) < 9 or f[2] != 'exon': continue
    tid = f[8].split('transcript_id "')[1].split('"')[0]
    tx[tid].append((int(f[3]) - 1, int(f[4]))); strand[tid] = f[6]
donors, acceptors = {}, {}
for tid, ex in tx.items():
    ex.sort()
    for (s1, e1), (s2, e2) in zip(ex[:-1], ex[1:]):
        i_s, i_e = e1, s2                       # intron 0-based half-open [i_s, i_e)
        if i_e - i_s < 50: continue
        if strand[tid] == '+':
            d = fa.fetch('X', i_s - 3, i_s + 6).upper(); a = fa.fetch('X', i_e - 20, i_e + 3).upper()
            donors[('+', i_s)] = d; acceptors[('+', i_e)] = a
        else:
            d = rc(fa.fetch('X', i_e - 6, i_e + 3).upper()); a = rc(fa.fetch('X', i_s - 3, i_s + 20).upper())
            donors[('-', i_e)] = d; acceptors[('-', i_s)] = a
print('unique annotated donors', len(donors), 'acceptors', len(acceptors))
d_can = {k: v for k, v in donors.items() if v[3:5] == 'GT'}
a_can = {k: v for k, v in acceptors.items() if v[18:20] == 'AG'}
print('GT donors', len(d_can), 'AG acceptors', len(a_can))

def ok(s, n): return len(s) == n and set(s) <= set('ACGT')
sd = [score5(v) for v in d_can.values() if ok(v, 9)]
sa = [score3(v) for v in a_can.values() if ok(v, 23)]
sd_nc = [score5(v) for v in donors.values() if ok(v, 9) and v[3:5] != 'GT']
def bins(x, lo=5, hi=8):
    x = np.array(x); return dict(n=len(x), lt5=float((x < lo).mean()), b5_8=float(((x >= lo) & (x <= hi)).mean()), gt8=float((x > hi).mean()), median=float(np.median(x)))
print('annotated GT donors  :', bins(sd))
print('annotated AG acc.    :', bins(sa))
print('annotated NON-GT donors (n=%d):' % len(sd_nc), bins(sd_nc) if sd_nc else None)

# ---- decoys: unannotated GT dinucleotides / AG dinucleotides inside annotated introns
intron_regions = []
for tid, ex in tx.items():
    ex.sort()
    for (s1, e1), (s2, e2) in zip(ex[:-1], ex[1:]):
        if e1 + 100 < s2 - 100: intron_regions.append((strand[tid], e1 + 50, s2 - 50))
random.shuffle(intron_regions)
dec_d, dec_a = [], []
ann_d_pos = {k[1] for k in donors}; ann_a_pos = {k[1] for k in acceptors}
for st, a, b in intron_regions[:3000]:
    p = random.randint(a, b - 30)
    if st == '+':
        if fa.fetch('X', p, p + 2).upper() == 'GT' and p not in ann_d_pos: dec_d.append(fa.fetch('X', p - 3, p + 6).upper())
        q = p + 2
        if fa.fetch('X', q - 2, q).upper() == 'AG' and q not in ann_a_pos: dec_a.append(fa.fetch('X', q - 20, q + 3).upper())
    else:
        pass
dec_d = [s for s in dec_d if ok(s, 9)]; dec_a = [s for s in dec_a if ok(s, 23)]
# ensure decoy has GT/AG at the expected place
dec_d = [s for s in dec_d if s[3:5] == 'GT']; dec_a = [s for s in dec_a if s[18:20] == 'AG']
sdd = [score5(s) for s in dec_d]; sda = [score3(s) for s in dec_a]
print('decoy GT donors (n=%d):' % len(sdd), bins(sdd)); print('decoy AG acceptors (n=%d):' % len(sda), bins(sda))
def auc(pos, neg):
    pos, neg = np.array(pos), np.array(neg)
    return float(np.mean([(p > neg).mean() + 0.5 * (p == neg).mean() for p in pos]))
print('AUC annotated vs decoy: donor %.3f acceptor %.3f' % (auc(sd, sdd), auc(sa, sda)))

# ---- SKILL.md example values
don, acc = 'CAGGTAAGT', 'TTTTTTTTTTTTTTTTTTTTCAG'
print("SKILL.md example: score5(%s)=%.2f  score3(%s)=%.2f" % (don, score5(don), acc, score3(acc)))
print("   (the SKILL.md acceptor example ends in 'CAG' not 'AG|G': last 3 are exon bases; positions 19-20 = %r)" % acc[18:20])

# ---- input validation
def tryit(label, f, *a):
    try:
        v = f(*a); print(f'   {label}: -> {v!r}')
        return repr(v)
    except BaseException as e:   # maxentpy calls sys.exit() on a wrong-length sequence
        print(f'   {label}: EXC {type(e).__name__}: {str(e)[:100]}'); return f'EXC {type(e).__name__}: {str(e)[:60]}'
res = {}
print('input validation of maxentpy 0.0.2 (SKILL.md: "ValueError or silently incorrect score"):')
res['N_in_donor'] = tryit('score5("CAGGTNAGT")', score5, 'CAGGTNAGT')
res['lower'] = tryit('score5("caggtaagt") lower-case', score5, 'caggtaagt')
res['short8'] = tryit('score5 8-mer', score5, 'CAGGTAAG')
res['long10'] = tryit('score5 10-mer', score5, 'CAGGTAAGTT')
res['acc_22'] = tryit('score3 22-mer', score3, 'TTTTTTTTTTTTTTTTTTTCAG')
res['nonACGT'] = tryit('score5("CAGGTXAGT")', score5, 'CAGGTXAGT')
res['U_in_RNA'] = tryit('score5("CAGGUAAGU") RNA alphabet', score5, 'CAGGUAAGU')
print('example score_splice_sites with a mixed list (one 8-mer, one lower-case, one N):')
s5, s3 = sq.score_splice_sites(['CAGGTAAGT', 'CAGGTAAG', 'caggtaagt', 'CAGGTNAGT'], [acc, acc[:-1]])
print('   5ss inputs 4 -> outputs', s5, '; 3ss inputs 2 ->', s3)
res['example_misalign'] = dict(n_in5=4, out5=[None if v is None else round(v, 2) for v in s5], n_in3=2, out3=[None if v is None else round(v, 2) for v in s3])
try:
    print('   printing f"{scores_5[i]:.2f}" for None ->', f'{s5[3]:.2f}')
except Exception as e:
    print('   formatting a None score (as in the __main__ hint) raises', type(e).__name__)

# ---- SpliceAI CLI claim check (variant scoring, run in another env by input6b.sh)
json.dump(dict(donors=bins(sd), acceptors=bins(sa), nonGT_donors=bins(sd_nc) if sd_nc else None, decoy_donors=bins(sdd), decoy_acceptors=bins(sda),
               auc_donor=auc(sd, sdd), auc_acceptor=auc(sa, sda), validation=res, n_annot_donors=len(donors), n_annot_acceptors=len(acceptors),
               example=dict(score5=score5(don), score3=score3(acc))), open(f'{RUN}/work/input6_result.json', 'w'), indent=1)
# write the VCF for the SpliceAI check: the 2 bases of the canonical donor of ENST... choose first + strand annotated GT donor and mutate G>A at intron +1
k = sorted(k for k in d_can if k[0] == '+')[200]
pos0 = k[1]                       # intron start (0-based) -> first intron base (G of GT) at 0-based pos0
ref = fa.fetch('X', pos0, pos0 + 1).upper()
open(f'{W}/donor.vcf', 'w').write('##fileformat=VCFv4.2\n##contig=<ID=X,length=155270560>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
                                 f'X\t{pos0+1}\t.\t{ref}\tA\t.\t.\t.\n' if ref != 'A' else f'X\t{pos0+1}\t.\t{ref}\tC\t.\t.\t.\n')
print('SpliceAI test variant at X:%d %s (canonical donor +1) ' % (pos0 + 1, ref))
