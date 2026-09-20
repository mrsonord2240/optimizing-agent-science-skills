"""INPUT 7 prep (NEW input). Build the alignment files that downstream tools (RAxML-NG, PhyML, IQ-TREE, MrBayes, codeml) will read.
REAL Pfam PF00042 (73x141) protein alignment + REAL HBB CDS alignment; variants inject the exact hazards the SKILL's dialect table names."""
import os, re
from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from common import *
d = DATA/'tools'; d.mkdir(exist_ok=True); os.chdir(d)
ref = AlignIO.read(str(PFAM), 'stockholm')
# clean short-id protein alignment: 12 taxa from the real seed, ids GLB_nn
sub = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).replace('.', '-')), id=r.id) for r in ref[:12]])
AlignIO.write(sub, 'pf12_relaxed.phy', 'phylip-relaxed')
print('pf12 ids sample', [r.id for r in sub][:3])
# (1) '*' hazard: stop-codon star in one protein row
star = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq)), id=r.id) for r in sub])
s = str(star[0].seq); i = [k for k, c in enumerate(s) if c != '-'][20]
star[0].seq = Seq(s[:i] + '*' + s[i+1:]); AlignIO.write(star, 'pf12_star.phy', 'phylip-relaxed')
fixed = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).replace('*', 'X')), id=r.id) for r in star]); AlignIO.write(fixed, 'pf12_starX.phy', 'phylip-relaxed')
# (2) long names: 150-char unique names (SYNTHETIC decoration of the real ids)
def longname(k, r): return f'{"seqname_"+str(k).zfill(2)}_' + 'x' * 120 + f'_{k:02d}_END'
lng = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq)), id=longname(k, r)) for k, r in enumerate(sub)]); AlignIO.write(lng, 'pf12_longnames.phy', 'phylip-relaxed')
print('long id len', len(lng[0].id))
# (3) names with colon / parentheses written by hand (Biopython's writer would rewrite them), to imitate a FOREIGN file
lines = open('pf12_relaxed.phy').read().splitlines()   # interleaved: only the first block's rows carry names
hdr, rows = lines[0], lines[1:]
bad = list(rows); nm, rest = bad[0].split(' ', 1); bad[0] = f'GLB:colon(1) {rest}'
open('pf12_foreign_colon.phy', 'w').write(hdr + '\n' + '\n'.join(bad) + '\n')
# (4) wrong sequence length foreign file: header says 141; delete 5 residues from the last non-empty line
rows2 = list(rows); k = max(i for i, l in enumerate(rows2) if l.strip()); rows2[k] = rows2[k][:-5]
open('pf12_wronglen.phy', 'w').write(hdr + '\n' + '\n'.join(rows2) + '\n')
# (5) NEXUS from AlignIO with molecule_type protein (MrBayes) and DNA
AlignIO.convert('pf12_relaxed.phy', 'phylip-relaxed', 'pf12.nex', 'nexus', molecule_type='protein')
recs = list(SeqIO.parse(PUB/'msa'/'hbb_cds_mammals.fasta', 'fasta'))[:6]
names = ['human','chimp','cow','pig','macaque','horse']
print('hbb lens', [len(r.seq) for r in recs])
SeqIO.write([SeqRecord(r.seq, id=n, description='') for r, n in zip(recs, names)], 'hbb6_short.fa', 'fasta')
print('wrote', sorted(os.listdir('.')))
