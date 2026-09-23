"""SYNTHETIC genome + paired reads for the MAPQ / tag checks (Input 5). Seeded, not real data.
Genome: 30 kb random + repeat families with 2, 3 and 6 identical copies (300 bp), so aligners must emit multimapper MAPQs.
Reads: 2500 pairs, 100 bp, insert ~300, 0.3% substitution errors, uniform over the genome."""
import os, random
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = RUN + '/data/aln'
os.makedirs(OUT, exist_ok=True)
rng = random.Random(7)
comp = str.maketrans('ACGT', 'TGCA')
rc = lambda s: s.translate(comp)[::-1]
rnd = lambda n: ''.join(rng.choice('ACGT') for _ in range(n))
fam = {k: rnd(300) for k in ('A', 'B', 'C')}
copies = {'A': 2, 'B': 3, 'C': 6}
parts = []
for k, n in copies.items():
    for _ in range(n):
        parts.append(fam[k])
unique = [rnd(2200) for _ in range(len(parts) + 1)]
g = unique[0]
for i, p in enumerate(parts):
    g += p + unique[i + 1]
g = g[:]
with open(OUT + '/g.fa', 'w') as fh:
    fh.write('>syn1\n' + '\n'.join(g[i:i + 60] for i in range(0, len(g), 60)) + '\n')
print('genome length', len(g))


def mut(s, rate=0.003):
    s = list(s)
    for i in range(len(s)):
        if rng.random() < rate:
            s[i] = rng.choice([b for b in 'ACGT' if b != s[i]])
    return ''.join(s)


n = 2500
with open(OUT + '/r1.fq', 'w') as f1, open(OUT + '/r2.fq', 'w') as f2:
    for i in range(n):
        ins = int(rng.gauss(300, 25))
        ins = max(ins, 120)
        st = rng.randint(0, len(g) - ins)
        frag = g[st:st + ins]
        if rng.random() < 0.5:
            frag = rc(frag)
        a, b = mut(frag[:100]), mut(rc(frag)[:100])
        f1.write(f'@p{i}/1\n{a}\n+\n{"I" * 100}\n')
        f2.write(f'@p{i}/2\n{b}\n+\n{"I" * 100}\n')
print('reads', n)
