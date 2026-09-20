#!/usr/bin/env python3
"""SYNTHETIC genome + reads with known multiplicity, to test the SKILL.md aligner-aware MAPQ table
("Drop ambiguous" -q 1 / "High confidence" thresholds per aligner).
Genome: 60 kb random (seed 7) with four repeat families (300 bp elements):
  A x2 exact, B x3 with 1% divergence, C x5 with 2% divergence, D x8 exact.
Reads: SE 100 bp, 0.5% substitution errors, class from truth: u (unique, 2000), A2/D8 (exact repeats), B3/C5 (diverged repeats)."""
import random, sys, os
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
rnd = random.Random(7)
L = 60000
g = [rnd.choice('ACGT') for _ in range(L)]
def rand_seq(n): return [rnd.choice('ACGT') for _ in range(n)]
def mutate(seq, rate):
    s = list(seq)
    for i in range(len(s)):
        if rnd.random() < rate:
            s[i] = rnd.choice([b for b in 'ACGT' if b != s[i]])
    return s
fam = {'A': (2, 0.0), 'B': (3, 0.01), 'C': (5, 0.02), 'D': (8, 0.0)}
copies = {}   # family -> [start]
slots = list(range(2000, L - 2000, 2500))
rnd.shuffle(slots)
elem = {k: rand_seq(300) for k in fam}
for k, (n, div) in fam.items():
    copies[k] = []
    for _ in range(n):
        st = slots.pop()
        g[st:st + 300] = mutate(elem[k], div) if div else elem[k]
        copies[k].append(st)
gs = ''.join(g)
with open(f'{out}/g.fa', 'w') as f:
    f.write('>ref\n')
    for i in range(0, L, 80): f.write(gs[i:i + 80] + '\n')
occupied = [(s - 150, s + 450) for v in copies.values() for s in v]
def comp(s): return s.translate(str.maketrans('ACGT', 'TGCA'))[::-1]
def read_at(pos, err=0.005, rc=False):
    r = list(gs[pos:pos + 100])
    for i in range(100):
        if rnd.random() < err: r[i] = rnd.choice([b for b in 'ACGT' if b != r[i]])
    r = ''.join(r)
    return comp(r) if rc else r
reads = []
# unique reads: start away from any repeat element (>=150 bp margin)
n = 0
while n < 2000:
    p = rnd.randrange(0, L - 100)
    if any(a < p + 100 and p < b for a, b in occupied): continue
    reads.append((f'u_{n}', read_at(p, rc=rnd.random() < .5))); n += 1
# repeat reads: 40 per copy, fully inside the 300 bp element
for k, starts in copies.items():
    cls = f'{k}{fam[k][0]}'
    for ci, st in enumerate(starts):
        for j in range(40):
            p = st + rnd.randrange(0, 201)
            reads.append((f'{cls}_c{ci}_{j}', read_at(p, rc=rnd.random() < .5)))
with open(f'{out}/reads.fq', 'w') as f:
    for name, s in reads:
        f.write(f'@{name}\n{s}\n+\n{"I" * 100}\n')
print('genome', L, 'reads', len(reads), 'copies', copies)
