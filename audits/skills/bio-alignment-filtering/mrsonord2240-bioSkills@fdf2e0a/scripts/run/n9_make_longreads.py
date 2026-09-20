#!/usr/bin/env python3
"""SYNTHETIC long-read fixture for the pbmm2 / minimap2 long-read MAPQ rows (nothing in public-data has real PacBio reads).
Genome: 300 kb random (seed 11). Repeat families (4 kb elements): A x2 exact, B x3 at 1% divergence, C x2 at 8% divergence.
Reads (2 kb): 300 unique, 40 per repeat copy fully inside an element. Two error profiles from the same positions:
HiFi-like (0.1% substitution) and ONT-like (2% sub + 1.5% ins + 1.5% del). Class is in the read name; truth = class."""
import os, random, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
rnd = random.Random(11)
L = 300_000; E = 4000; RL = 2000
g = [rnd.choice('ACGT') for _ in range(L)]
def rs(n): return [rnd.choice('ACGT') for _ in range(n)]
def mutate(seq, rate):
    s = list(seq)
    for i in range(len(s)):
        if rnd.random() < rate: s[i] = rnd.choice([b for b in 'ACGT' if b != s[i]])
    return s
fam = {'A': (2, 0.0), 'B': (3, 0.01), 'C': (2, 0.08)}
slots = list(range(10000, L - 10000, 20000)); rnd.shuffle(slots)
elem = {k: rs(E) for k in fam}; copies = {}
for k, (n, div) in fam.items():
    copies[k] = []
    for _ in range(n):
        st = slots.pop(); g[st:st + E] = mutate(elem[k], div) if div else elem[k]; copies[k].append(st)
gs = ''.join(g)
with open(f'{out}/g.fa', 'w') as f:
    f.write('>ref\n')
    for i in range(0, L, 80): f.write(gs[i:i + 80] + '\n')
def comp(s): return s.translate(str.maketrans('ACGT', 'TGCA'))[::-1]
def errs(seq, sub, ins, dele):
    o = []
    for b in seq:
        r = rnd.random()
        if r < dele: continue
        if r < dele + sub: o.append(rnd.choice([x for x in 'ACGT' if x != b]))
        else: o.append(b)
        if rnd.random() < ins: o.append(rnd.choice('ACGT'))
    return ''.join(o)
occupied = [(s - RL, s + E + RL) for v in copies.values() for s in v]
reads = []
n = 0
while n < 300:
    p = rnd.randrange(0, L - RL)
    if any(a < p + RL and p < b for a, b in occupied): continue
    reads.append((f'u_{n}', p, rnd.random() < .5)); n += 1
for k, starts in copies.items():
    for ci, st in enumerate(starts):
        for j in range(40):
            reads.append((f'{k}{fam[k][0]}_c{ci}_{j}', st + rnd.randrange(0, E - RL), rnd.random() < .5))
for prof, (sub, ins, dele) in {'hifi': (0.001, 0.0, 0.0), 'ont': (0.02, 0.015, 0.015)}.items():
    with open(f'{out}/{prof}.fq', 'w') as f:
        for name, p, rc in reads:
            s = errs(gs[p:p + RL], sub, ins, dele)
            if rc: s = comp(s)
            f.write(f'@{name}\n{s}\n+\n{"I" * len(s)}\n')
print('genome', L, 'reads', len(reads), 'copies', copies)
