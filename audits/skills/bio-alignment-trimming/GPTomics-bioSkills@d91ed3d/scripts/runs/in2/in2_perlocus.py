# Input 2 (adapted step): trim each locus with ClipKIT kpic-smart-gap, then concatenate and rebuild the charsets.
# Trimming the concatenated matrix invalidates supermatrix.nex; the Skill gives no guidance on this.
import glob, os, subprocess
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

loci = sorted(glob.glob('../../data/dna_super/locus??.aln.fasta'))
os.makedirs('trimmed_loci', exist_ok=True)
rows, parts, start = {}, [], 1
tot_in = tot_out = 0
for p in loci:
    name = os.path.basename(p).split('.')[0]
    out = f'trimmed_loci/{name}.kpic.fasta'
    subprocess.run(['clipkit', p, '-m', 'kpic-smart-gap', '--log', '-o', out], check=True, capture_output=True)
    a_in, a = AlignIO.read(p, 'fasta'), AlignIO.read(out, 'fasta')
    tot_in += a_in.get_alignment_length(); tot_out += a.get_alignment_length()
    for r in a:
        rows.setdefault(r.id, []).append(str(r.seq))
    L = a.get_alignment_length(); parts.append((name, start, start + L - 1)); start += L
ids = sorted(rows)
SeqIO.write([SeqRecord(Seq(''.join(rows[i])), id=i, description='') for i in ids], 'super_perlocus_kpic.fasta', 'fasta')
with open('super_perlocus_kpic.nex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('#nexus\nbegin sets;\n' + ''.join(f'  charset {n} = {a}-{b};\n' for n, a, b in parts) + 'end;\n')
print(f'per-locus kpic-smart-gap: {tot_out}/{tot_in} columns retained = {tot_out/tot_in:.1%}; partitions rebuilt: {len(parts)}')
for f in ['super_kpic.fasta', 'super_bmge112.fasta', 'super_bmge200e.fasta']:
    if os.path.exists(f):
        L = AlignIO.read(f, 'fasta').get_alignment_length()
        print(f'{f}: {L}/{tot_in} = {L/tot_in:.1%} retained')
