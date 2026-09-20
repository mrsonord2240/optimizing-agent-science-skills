#!/usr/bin/env python3
"""Input 4b: SKILL.md pysam 'Subsample (Pair-Consistent)' recipe (verbatim logic) vs claims
(seed = independent samples; realised fraction; mates together)."""
import os, sys, zlib, collections
import pysam

AFD = os.environ['AFDATA']
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
inp = f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'
fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond: fails.append(name)

full = collections.Counter(r.query_name for r in pysam.AlignmentFile(inp))
print('records', sum(full.values()), 'templates', len(full), 'templates with 2 records', sum(1 for v in full.values() if v == 2))

def subsample(seed, fraction, out):
    threshold = int(0xffffffff * fraction)
    def template_hash(qname, seed):
        return zlib.crc32(qname.encode()) ^ seed
    with pysam.AlignmentFile(inp, 'rb') as infile:
        with pysam.AlignmentFile(out, 'wb', header=infile.header) as outfile:
            for read in infile:
                if template_hash(read.query_name, seed) <= threshold:
                    outfile.write(read)
    return collections.Counter(r.query_name for r in pysam.AlignmentFile(out))

sets = {}
for seed in (42, 1, 7, 100, 12345):
    c = subsample(seed, 0.1, f'{W}/py_seed{seed}.bam')
    sets[seed] = set(c)
    consistent = all(c[q] == full[q] for q in c)
    frac = len(c) / len(full)
    check(f'seed {seed}: mates kept together', consistent)
    check(f'seed {seed}: realised template fraction ~0.10 (0.08-0.12)', 0.08 <= frac <= 0.12, f'{frac:.4f} ({len(c)} templates)')
def jac(a, b): return len(a & b) / len(a | b)
print('Jaccard overlap of kept-template sets between seeds (independent 10% samples would share ~5%):')
for a, b in [(42, 1), (42, 7), (42, 100), (42, 12345), (1, 7), (100, 12345)]:
    print(f'  seed {a} vs {b}: Jaccard {jac(sets[a], sets[b]):.3f}')
check('different small seeds give (near-)independent samples (SKILL.md: "use different integer seeds for independent samples" applies to CLI; pysam recipe shares the seed arg)',
      jac(sets[42], sets[1]) < 0.3, f'Jaccard 42 vs 1 = {jac(sets[42], sets[1]):.3f}')
# reproducibility
c2 = subsample(42, 0.1, f'{W}/py_seed42_b.bam')
check('seed 42 reproducible', set(c2) == sets[42])
# fraction 1.0 edge & fraction 0.5
c = subsample(42, 0.5, f'{W}/py_half.bam'); print('fraction 0.5 realised', round(len(c) / len(full), 4))
print('\nFAILS:', fails)
