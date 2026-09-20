#!/usr/bin/env python
"""SYNTHETIC reads for the fastq_screen rRNA test: 4000 reads, 25% from a synthetic 5-kb 'rRNA' reference, 75% from a random genome."""
import random, sys
random.seed(5)
B = 'ACGT'
rrna = ''.join(random.choice(B) for _ in range(5000))
gen = ''.join(random.choice(B) for _ in range(200000))
open('rrna.fa', 'w').write('>rRNA_synth\n' + rrna + '\n')
open('genome.fa', 'w').write('>chrS\n' + gen + '\n')
n = 4000; nr = int(0.25 * n)
with open('sample_R1.fq', 'w') as f:
    for i in range(n):
        if i < nr:
            p = random.randint(0, len(rrna) - 100); s = rrna[p:p + 100]
        else:
            p = random.randint(0, len(gen) - 100); s = gen[p:p + 100]
        f.write(f'@r{i}\n{s}\n+\n' + 'I' * 100 + '\n')
print('wrote 4000 reads, 25% from the synthetic rRNA reference')
