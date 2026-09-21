"""NEW input data (auditor-made, SYNTHETIC): 4000 single-end reads, 25% from a random 5 kb 'rRNA' reference (1% substitution errors),
75% from unrelated random sequence; plus the rRNA reference FASTA. Usage: python 70_in7_make_fq.py <out dir>"""
import sys, random, gzip
out = sys.argv[1]; rng = random.Random(20260920)
rnd = lambda n: ''.join(rng.choice('ACGT') for _ in range(n))
rrna = rnd(5000); open(f'{out}/rrna_ref.fa', 'w').write('>rRNA_synth\n' + rrna + '\n')
with gzip.open(f'{out}/rrna_ref.fa.gz', 'wt') as fh: fh.write('>rRNA_synth\n' + rrna + '\n')
with open(f'{out}/sample_R1.fq', 'w') as fq:
    for i in range(4000):
        if i % 4 == 0:
            p = rng.randrange(0, 4900); s = list(rrna[p:p + 100])
            for j in range(100):
                if rng.random() < 0.01: s[j] = rng.choice('ACGT')
            s = ''.join(s)
        else: s = rnd(100)
        fq.write(f'@r{i}\n{s}\n+\n{"I" * 100}\n')
print('4000 reads, 1000 from rRNA (25%)')
