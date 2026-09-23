"""Input 6 (Scope boundary): 'align human vs cow HBB CDS for a dN/dS analysis' (skill: protein first, then back-translate) -- REAL RefSeq CDS.
Checks the DNA-vs-protein table and that a protein-guided codon alignment is frame-consistent."""
from common import *
from Bio.Seq import Seq
recs = list(SeqIO.parse(DATA + r'\hbb_cds_mammals.fasta', 'fasta'))
human, cow, rabbit = recs[0], recs[2], recs[6]
h, c = str(human.seq).upper(), str(cow.seq).upper()
hp, cp = Seq(h).translate(), Seq(c).translate()
print(len(h), len(c), "protein", len(hp), len(cp), "stops in-frame:", str(hp).count('*'), str(cp).count('*'))
dna = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
pro = PairwiseAligner(mode='global', substitution_matrix=substitution_matrices.load('BLOSUM62'), open_gap_score=-11, extend_gap_score=-1)
A = dna.align(h, c)[0]; c1 = A.counts()
P = pro.align(str(hp).rstrip('*'), str(cp).rstrip('*'))[0]; c2 = P.counts()
ni = 100 * c1.identities / (c1.identities + c1.mismatches); pi = 100 * c2.identities / (c2.identities + c2.mismatches)
print(f"DNA-level pid2={ni:.1f}% (gaps {c1.gaps}) | protein-level pid2={pi:.1f}% (gaps {c2.gaps})")
check("nucleotide identity > 70% -> skill says align as DNA; consistent with real data", ni > 70, ni)
# back-translate protein alignment to a codon alignment, check frame integrity and that residues re-translate to the protein columns
ps, qs = P[0, :], P[1, :]
hi = ci = 0; hc, cc = [], []
for a_, b_ in zip(ps, qs):
    hc.append(h[3*hi:3*hi+3] if a_ != '-' else '---'); hi += a_ != '-'
    cc.append(c[3*ci:3*ci+3] if b_ != '-' else '---'); ci += b_ != '-'
hcod, ccod = ''.join(hc), ''.join(cc)
check("codon alignment equal length, multiple of 3", len(hcod) == len(ccod) and len(hcod) % 3 == 0, len(hcod))
check("back-translated human row re-translates to the protein-alignment row", str(Seq(hcod.replace('---', '')).translate()) == ps.replace('-', ''), "")
syn = sum(1 for i in range(0, len(hcod), 3) if '---' not in (hcod[i:i+3], ccod[i:i+3]) and hcod[i:i+3] != ccod[i:i+3])
print("codons differing (human vs cow):", syn, "of", len(hcod)//3)
# rabbit record has an internal stop (data trap) -- what does the skill workflow do?
rp = Seq(str(rabbit.seq).upper()).translate()
print("rabbit HBB2 CDS len", len(rabbit.seq), "translation stops:", str(rp).count('*'), "->", str(rp)[:60], "...")
try:
    print("aligning rabbit protein incl. internal '*' with BLOSUM62:", pro.score(str(hp), str(rp)))
except Exception as e:
    print("ERR", e)
summary()
