"""Input 4 (Variant B): 'In my globin alignment, which alignment column is the proximal histidine of sperm-whale myoglobin (PDB 1MBN, His93),
and what residue does every other globin have there? Also map columns back to residue numbers.'
REAL data: 8 UniProt globins aligned with MAFFT L-INS-i (in4_mafft.sh, WSL) + REAL PDB 1MBN coordinates (Bio.PDB) as ground truth."""
import os, warnings
import numpy as np
from Bio import AlignIO, SeqIO
from Bio.PDB import PDBParser, PPBuilder
from Bio.PDB.Polypeptide import three_to_index, index_to_one
from common import *
import skill_md_funcs as F
warnings.simplefilter('ignore')

aln = AlignIO.read(os.path.join(HERE, 'data', 'globins8_mafft_linsi.fasta'), 'fasta')
ids = [r.id.split('|')[2] for r in aln]
print(ids, aln.get_alignment_length())
raw = {r.id.split('|')[2]: str(r.seq) for r in SeqIO.parse(os.path.join(PUB, 'globins_uniprot.fasta'), 'fasta')}
myg = [r for r in aln if 'MYG_PHYMC' in r.id][0]

# 1. skill coordinate_map round-trips (property test on every record)
for r in aln:
    s2a, a2s = F.coordinate_map(r)
    ung = str(r.seq).replace('-', '')
    key = r.id.split('|')[2]
    ok = (ung == raw[key]) and len(s2a) == len(ung) and all(a2s[s2a[i]] == i for i in range(len(ung))) and all(str(r.seq)[s2a[i]] == ung[i] for i in range(len(ung)))
    check(f'{key}: ungapped == original UniProt seq; seq->aln->seq round-trips; gap cols == -1', ok and (a2s == -1).sum() == len(r.seq) - len(ung))

# 2. independent slow walk (SKILL: "for single lookups walk the sequence tracking a counter")
def walk(rec):
    m = {}; k = 0
    for c, ch in enumerate(str(rec.seq)):
        if ch != '-': m[k] = c; k += 1
    return m
s2a, a2s = F.coordinate_map(myg)
w = walk(myg)
check('vectorised seq_to_aln == loop-based walk for MYG_PHYMC', all(s2a[i] == w[i] for i in w) and len(w) == len(s2a))

# 3. GROUND TRUTH from PDB 1MBN: proximal His is residue number 93 in PDB numbering
st = PDBParser(QUIET=True).get_structure('1MBN', os.path.join(HERE, '..', '..', '..', 'audit-envs', 'alignment', 'public-data', 'structures', '1MBN.pdb')) if False else PDBParser(QUIET=True).get_structure('1MBN', r'F:\OpenScience\audit-envs\alignment\public-data\structures\1MBN.pdb')
chain = st[0]['A']
res93 = chain[93]
print('1MBN residue 93:', res93.get_resname(), '| first PDB residue number:', next(iter(chain)).id[1], next(iter(chain)).get_resname())
check('PDB ground truth: 1MBN residue 93 is HIS (proximal His F8)', res93.get_resname() == 'HIS')
pdb_seq = ''.join(index_to_one(three_to_index(r.get_resname())) for r in chain if r.id[0] == ' ')
uni = raw['MYG_PHYMC']
print('PDB seq len', len(pdb_seq), 'UniProt len', len(uni))
off = uni.find(pdb_seq[:20])
print('PDB numbering offset vs UniProt (0-based find):', off)
check('SEQRES-vs-UniProt offset: PDB 1MBN starts at UniProt residue 2 (initiator Met absent), i.e. PDB n == 0-based UniProt index n', off == 1)
mism = [i for i in range(len(pdb_seq)) if uni[i + off] != pdb_seq[i]]
print('PDB vs UniProt mismatches (PDB idx):', mism)
# 4. Map: PDB residue 93 -> UniProt 0-based index 93 -> alignment column
col = int(s2a[93])
print('alignment column of PDB His93 (0-based):', col, '| myoglobin residue at UniProt idx 93:', uni[93])
check('correct route (PDB n -> 0-based UniProt index n via +1 offset, then seq_to_aln) lands on His', uni[93] == 'H' and str(myg.seq)[col] == 'H')
naive = int(s2a[92])   # user follows "residue 93 -> index 92 (1-based-to-0-based)" and forgets the Met offset
print('naive 1-based->0-based (index 92) residue:', uni[92], '| column', naive)
check('the naive route (ignoring SEQRES/ATOM offset) does NOT land on His -> the offset trap is real (docs only point elsewhere)', uni[92] != 'H')
colres = {r.id.split('|')[2]: str(r.seq)[col] for r in aln}
print('residue in column', col, 'for all 8:', colres)
check('all 8 globins have His at the proximal-His column (biological ground truth: F8 His invariant)', set(colres.values()) == {'H'})
# 5. reverse mapping for another known residue: distal His64 (E7) in PDB numbering -> UniProt idx 64
cold = int(s2a[64]); dres = {r.id.split('|')[2]: str(r.seq)[cold] for r in aln}
print('distal His (PDB 64) column', cold, dres)
check('distal His E7: PDB 1MBN residue 64 is HIS and maps to column where the myoglobins have His', chain[64].get_resname() == 'HIS' and dres['MYG_PHYMC'] == 'H' and dres['MYG_HUMAN'] == 'H')
# 6. 'aln_to_seq[100]' gap semantic: choose a column where MYG has a gap
gapcols = [c for c in range(aln.get_alignment_length()) if str(myg.seq)[c] == '-']
print('MYG gap columns:', gapcols[:10])
check('aln_to_seq is -1 at gap columns and equals number of residues before the column otherwise', all(a2s[c] == -1 for c in gapcols) and a2s[col] == 93)
# 7. Skill's own doc example variable name
print("SKILL.md names `seq_to_aln[42]` 'column_for_residue_42' -> that is the 43rd residue (0-based index). residue 43 =", uni[42], '(1-based 42 would be', uni[41] + ')')
# 8. the 'fully conserved in the alignment' cross-check with SKILL find_conserved_positions
cons = F.find_conserved_positions(aln, 1.0)
print('fully conserved columns in the 8-globin alignment:', cons)
check('proximal His column is among the fully conserved columns of the 8-globin alignment (skill function agrees with structure)', (col, 'H') in cons)
summary()
