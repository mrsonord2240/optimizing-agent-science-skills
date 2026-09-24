# Input 6: divergence gate from SKILL.md "Sequence Divergence Thresholds" before trusting the MSA
import itertools
from Bio import AlignIO
for f in ('twi8_linsi.fasta', 'twi8_muscle.afa'):
    aln = AlignIO.read(f, 'fasta')
    p = []
    for a, b in itertools.combinations(aln, 2):
        s1, s2 = str(a.seq), str(b.seq)
        m = sum(x == y and x != '-' for x, y in zip(s1, s2)); d = sum(x != '-' and y != '-' for x, y in zip(s1, s2))
        p.append(m / d)
    mean = sum(p) / len(p)
    band = ('>40% strong' if mean > .4 else '25-40% moderate' if mean > .25 else '20-25% weak' if mean > .2 else '<20% noise dominates -> structural alignment')
    print(f'{f}: mean PID2 {mean:.1%} (min {min(p):.1%}, max {max(p):.1%}) -> {band}')
