"""Input 2 (auditor implementation of the fixed Skill's instruction): ClipKIT smart-gap PER LOCUS, then concatenate and
rebuild charsets; also a PHYLIP copy with the Skill's '-of phylip' flag on one locus."""
import glob, os, subprocess
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

loci = sorted(glob.glob('../../data/dna_super/locus??.aln.fasta'))
os.makedirs('trimmed_loci', exist_ok=True)
rows, parts, start, tin, tout = {}, [], 1, 0, 0
for p in loci:
    name = os.path.basename(p).split('.')[0]
    out = f'trimmed_loci/{name}.sg.fasta'
    subprocess.run(['clipkit', p, '-m', 'smart-gap', '--log', '-o', out], check=True, capture_output=True)
    ai, a = AlignIO.read(p, 'fasta'), AlignIO.read(out, 'fasta')
    tin += ai.get_alignment_length(); tout += a.get_alignment_length()
    for r in a:
        rows.setdefault(r.id, []).append(str(r.seq))
    L = a.get_alignment_length(); parts.append((name, start, start + L - 1)); start += L
ids = sorted(rows)
SeqIO.write([SeqRecord(Seq(''.join(rows[i])), id=i, description='') for i in ids], 'super_sg.fasta', 'fasta')
with open('super_sg.nex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('#nexus\nbegin sets;\n' + ''.join(f'  charset {n} = {a}-{b};\n' for n, a, b in parts) + 'end;\n')
print(f'per-locus smart-gap: {tout}/{tin} = {tout/tin:.1%} retained; {len(parts)} charsets rebuilt')
