"""Make MACSE-style test copies of the SYNTHETIC codon alignment: one '!' frameshift marker in Sp03 and an internal TGA
stop in Sp07 (macse_like.fasta); a copy with the frameshift only (macse_like_nostop.fasta) for the codeml check."""
from Bio import SeqIO

recs = list(SeqIO.parse('codon.fasta', 'fasta'))
def edit(r, pos, new):
    s = list(str(r.seq)); s[pos:pos + len(new)] = list(new); return ''.join(s)

def first_full_codon(seq, start):
    for i in range(start - start % 3, len(seq) - 3, 3):
        if '-' not in seq[i:i + 3]:
            return i
out, out2 = [], []
for r in recs:
    s = str(r.seq)
    s2 = s
    if r.id == 'Sp03':
        i = first_full_codon(s, 150); s = s[:i + 1] + '!' + s[i + 2:]; s2 = s
    if r.id == 'Sp07':
        i = first_full_codon(s, 300); s = s[:i] + 'TGA' + s[i + 3:]
    out.append(f'>{r.id}\n{s}\n'); out2.append(f'>{r.id}\n{s2}\n')
open('macse_like.fasta', 'w', newline='\n').write(''.join(out))
open('macse_like_nostop.fasta', 'w', newline='\n').write(''.join(out2))
print('wrote macse_like.fasta (1 "!" in Sp03, internal TGA in Sp07) and macse_like_nostop.fasta')
