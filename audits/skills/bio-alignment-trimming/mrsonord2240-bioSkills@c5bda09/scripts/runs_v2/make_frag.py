"""Input 9 data (SYNTHETIC): prot15 L-INS-i alignment with two sequences turned into fragments (only a central 30% /
45% window of residues kept, rest gaps) -- the partial transcriptome contigs a user would meet."""
from Bio import SeqIO
recs = list(SeqIO.parse('../../data/prot15_linsi.fasta', 'fasta'))
L = len(recs[0].seq)
out = []
for i, r in enumerate(recs):
    s = str(r.seq)
    if i in (3, 9):
        keep = 0.30 if i == 3 else 0.45
        a = int(L * (0.5 - keep / 2)); b = int(L * (0.5 + keep / 2))
        s = '-' * a + s[a:b] + '-' * (L - b)
        print(f'fragment: {r.id} residues kept {sum(c != "-" for c in s)} of {sum(c != "-" for c in str(r.seq))}')
    out.append(f'>{r.id}\n{s}\n')
open('frag17.fasta', 'w', newline='\n').write(''.join(out))
