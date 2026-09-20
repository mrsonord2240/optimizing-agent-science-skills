"""Input 9 (NEW, real DNA the fixer never used): orthologous HBB CDS from 6 mammals (RefSeq, public-data), run in WSL env alignment.
Task a researcher would send: 'score human HBB CDS against each ortholog, tell me the identity, and place a read of unknown orientation on the human CDS'.
(a) global NUC.4.4 -10/-0.5 == EMBOSS needle EDNAFULL 10/0.5 (end gaps penalised) for every pair; independent Gotoh DP for one pair;
(b) Skill's 'DNA vs protein' table on real orthologs: nucleotide vs protein identity; (c) strand recipe: 120-nt cow segment, reverse-complemented,
semiglobal placement on the human CDS via 'score seq and its reverse complement, keep the higher' ; ground truth = the same segment un-flipped (aligned coords)."""
import os, subprocess, sys, warnings; warnings.simplefilter('ignore')
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner, substitution_matrices
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'data'); os.chdir(D)
sys.path.insert(0, HERE)
from ref_gotoh import load_matrix, gotoh_score
F = []
def check(n, c, o=''):
    print(('PASS  ' if c else 'FAIL  ') + n + ' | ' + str(o)); (None if c else F.append(n))
recs = list(SeqIO.parse('hbb_cds_mammals.fasta', 'fasta'))
name = lambda r: r.id.split('_cds')[0].replace('lcl|', '')
human = recs[0]; others = recs[1:6]      # rabbit HBB2 (record 7, internal stop) excluded here; covered in input 6
NUC = substitution_matrices.load('NUC.4.4')
al = PairwiseAligner(mode='global', substitution_matrix=NUC, open_gap_score=-10, extend_gap_score=-0.5)
B62 = substitution_matrices.load('BLOSUM62')
pal = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)
open('h.fa', 'w').write('>h\n' + str(human.seq) + '\n')
ok_all = True; rows = []
for r in others:
    open('o.fa', 'w').write('>o\n' + str(r.seq) + '\n')
    p = subprocess.run(['needle', '-asequence', 'h.fa', '-bsequence', 'o.fa', '-gapopen', '10', '-gapextend', '0.5', '-endweight', 'Y', '-endopen', '10', '-endextend', '0.5', '-outfile', 'dna_needle.txt', '-auto'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    sc = [l for l in open('dna_needle.txt') if l.startswith('# Score')][0].split(':')[1].strip()
    ident = [l for l in open('dna_needle.txt') if l.startswith('# Identity')][0].split(':')[1].strip()
    A = al.align(str(human.seq).upper(), str(r.seq).upper())[0]; c = A.counts()
    pid1 = 100 * c.identities / len(A[0, :])
    hp, rp = str(Seq(str(human.seq)).translate()).rstrip('*'), str(Seq(str(r.seq)).translate()).rstrip('*')
    P = pal.align(hp, rp)[0]; cp = P.counts(); ppid = 100 * cp.identities / len(P[0, :])
    rows.append((name(r), float(sc), A.score, pid1, ppid))
    ok_all &= abs(float(sc) - A.score) < 1e-9
    print(f"   {name(r)}: needle {sc} ({ident}) | Biopython NUC.4.4 {A.score} | nt PID1 {pid1:.1f}% | protein PID1 {ppid:.1f}%")
check("(a) Biopython NUC.4.4 -10/-0.5 global score == EMBOSS needle EDNAFULL 10/0.5 for all 5 orthologs", ok_all)
B = load_matrix('NUC.4.4')
gt = gotoh_score(str(human.seq).upper(), str(others[1].seq).upper(), B, 10, 0.5, 'global')
check("(a) independent Gotoh DP == Biopython for human vs cow", abs(gt - al.score(str(human.seq).upper(), str(others[1].seq).upper())) < 1e-9, gt)
check("(b) Skill table: every ortholog pair is >70% nucleotide identity -> 'align as DNA' (min nt PID1 > 70)", min(r[3] for r in rows) > 70, round(min(r[3] for r in rows), 1))
# (c) strand recipe
cow = str(others[1].seq).upper(); hum = str(human.seq).upper()
seg = cow[120:240]; flipped = str(Seq(seg).reverse_complement())
semi = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5); semi.end_gap_score = 0.0
truth = semi.align(hum, seg)[0]                                        # ground truth: correct orientation
cands = [(semi.score(hum, flipped), 'as given'), (semi.score(hum, str(Seq(flipped).reverse_complement())), 'revcomp')]
best = max(cands)
print("   candidates:", cands, "| truth (unflipped) score", truth.score, "span", truth.aligned[0][0][0], "..", truth.aligned[0][-1][1])
check("(c) Skill's recipe (score seq and seq.reverse_complement(), keep the higher) picks the reverse complement and reproduces the un-flipped score", best[1] == 'revcomp' and best[0] == truth.score, best)
check("(c) 'as given' orientation scores far lower (strand-specific)", cands[0][0] < 0.5 * truth.score, cands[0][0])
la = semi.align(hum, str(Seq(flipped).reverse_complement()))[0]
check("(c) placed coordinates: the segment lands at the same human span as the un-flipped alignment (cow 120..240 ~ human 120..240 +-15)", abs(la.aligned[0][0][0] - 120) <= 15 and abs(la.aligned[0][-1][1] - 240) <= 15, (int(la.aligned[0][0][0]), int(la.aligned[0][-1][1])))
import edlib
hw = edlib.align(str(Seq(flipped).reverse_complement()), hum, mode='HW', task='locations')
check("(c) cross-check with edlib HW: same locus (start within 15 of Biopython's)", abs(hw['locations'][0][0] - la.aligned[0][0][0]) <= 15, (hw['editDistance'], hw['locations'][:1]))
print('FAILED:', F if F else 'none')
