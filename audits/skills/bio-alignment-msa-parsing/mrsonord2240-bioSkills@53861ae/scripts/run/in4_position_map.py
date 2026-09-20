"""Input 4 (Variant B, regression of first-audit input 4): 'In my 8-globin alignment, which column is the proximal histidine of
sperm-whale myoglobin (PDB 1MBN, His93), what residue does every other globin have there, and how do I convert between column
numbers and residue numbers?'
REAL data: 8 UniProt globins aligned by MAFFT L-INS-i (wsl_tools.sh mafft_globins) + REAL PDB 1MBN coordinates (Bio.PDB) as the
ground truth. Code = SKILL.md blocks exec'd from the file (coordinate_map, find_conserved_positions) + the doc sentence about
PDB numbering is checked against the coordinates."""
import os, warnings
import numpy as np
from Bio import AlignIO, SeqIO
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import three_to_index, index_to_one
from common import *
import skillns
warnings.simplefilter('ignore')
ns, _ = skillns.load()

aln = AlignIO.read(os.path.join(DATA, 'globins8_mafft_linsi.fasta'), 'fasta')
key = lambda r: r.id.split('|')[2]
raw = {key(r): str(r.seq) for r in SeqIO.parse(GLOBINS_FA, 'fasta')}
myg = [r for r in aln if 'MYG_PHYMC' in r.id][0]
print([key(r) for r in aln], aln.get_alignment_length())

for r in aln:
    s2a, a2s = ns['coordinate_map'](r)
    ung = str(r.seq).replace('-', '')
    ok = ung == raw[key(r)] and len(s2a) == len(ung) and all(a2s[s2a[i]] == i for i in range(len(ung))) and all(str(r.seq)[s2a[i]] == ung[i] for i in range(len(ung))) and int((a2s == -1).sum()) == len(r.seq) - len(ung)
    check(f'{key(r)}: coordinate_map ungapped == original UniProt sequence, seq->aln->seq round-trips, gap columns == -1', ok)

def walk(rec):  # the single-lookup loop the SKILL says coordinate_map subsumes
    m, k = {}, 0
    for c, ch in enumerate(str(rec.seq)):
        if ch != '-': m[k] = c; k += 1
    return m
s2a, a2s = ns['coordinate_map'](myg)
w = walk(myg)
check('vectorised seq_to_aln == the loop-based walk for MYG_PHYMC', all(s2a[i] == w[i] for i in w) and len(w) == len(s2a))

# ground truth: PDB 1MBN
chain = PDBParser(QUIET=True).get_structure('1MBN', PDB_1MBN)[0]['A']
first = next(iter(chain))
print('1MBN first residue:', first.id[1], first.get_resname(), '| residue 93:', chain[93].get_resname(), '| residue 64:', chain[64].get_resname())
check('PDB ground truth: 1MBN numbers from 1 (VAL) and residue 93 is HIS (proximal His F8), residue 64 is HIS (distal E7)',
      first.id[1] == 1 and first.get_resname() == 'VAL' and chain[93].get_resname() == 'HIS' and chain[64].get_resname() == 'HIS')
pdb_seq = ''.join(index_to_one(three_to_index(r.get_resname())) for r in chain if r.id[0] == ' ')
uni = raw['MYG_PHYMC']
off = uni.find(pdb_seq[:20])
check('PDB 1MBN sequence is UniProt P02185 from residue 2 (offset 1) with zero mismatches', off == 1 and all(uni[i + off] == pdb_seq[i] for i in range(len(pdb_seq))), f'offset {off}')

# the SKILL.md sentence: "PDB 1MBN numbers residues from the first Val, so His93 is UniProt P02185 residue 94 (0-based index 93, checked)"
check('SKILL.md sentence verified: His93 (PDB) is UniProt residue 94 = 0-based index 93 and that residue is H; index 92 is not H', uni[93] == 'H' and uni[92] != 'H', f'idx92={uni[92]} idx93={uni[93]}')
col = int(s2a[93])
print('alignment column of PDB His93 (0-based):', col)
colres = {key(r): str(r.seq)[col] for r in aln}
print('residue in that column for all 8:', colres)
check('all 8 globins have His in the column reached by (PDB residue 93 -> 0-based UniProt index 93 -> seq_to_aln)', set(colres.values()) == {'H'})
cold = int(s2a[64]); dres = {key(r): str(r.seq)[cold] for r in aln}
check('distal His (PDB residue 64) column has His in both myoglobins', dres['MYG_PHYMC'] == 'H' and dres['MYG_HUMAN'] == 'H', str(dres))
cons = ns['find_conserved_positions'](aln, 1.0)
print('fully conserved columns:', [(c, a) for c, a, _ in cons][:12], '...')
check('find_conserved_positions(1.0) lists the proximal His column (structure and alignment agree)', (col, 'H') in [(c, a) for c, a, _ in cons])
gapcols = [c for c in range(aln.get_alignment_length()) if str(myg.seq)[c] == '-']
check('aln_to_seq is -1 exactly at the gap columns of MYG_PHYMC and equals the residue count before the column otherwise', all(a2s[c] == -1 for c in gapcols) and a2s[col] == 93 and len(gapcols) > 0, f'gap columns {gapcols}')
# renamed variable in the doc: column_of_residue_index_42 (0-based)
code = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
check('doc variable renamed to column_of_residue_index_42 with the 0-based comment; the residue at index 42 is the 43rd', 'column_of_residue_index_42 = seq_to_aln[42]   # 0-based index 42 is the 43rd residue' in code and 'seq_to_aln[42]' in code and len([r for r in str(myg.seq) if r != '-'][:43]) == 43)
summary()
