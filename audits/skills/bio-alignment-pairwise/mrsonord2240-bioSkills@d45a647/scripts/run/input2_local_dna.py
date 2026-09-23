"""Input 2 (Variant A): local DNA alignment. SYNTHETIC flanks (random, seed 7) + a REAL 150-nt segment of human HBB CDS
(NM_000518.5) planted with 5 known substitutions and one 3-nt deletion. Ground truth = planted coordinates + parasail SW + own Gotoh."""
import random
from common import *
import parasail
from ref_gotoh import gotoh_score
recs = list(SeqIO.parse(DATA + r'\hbb_cds_mammals.fasta', 'fasta'))
cds = str(recs[0].seq).upper()
random.seed(7)
rnd = lambda n: ''.join(random.choice('ACGT') for _ in range(n))
seg = cds[30:180]                       # real 150 nt
mut = list(seg)
subs = [20, 45, 70, 100, 130]           # 5 known substitutions
for p in subs: mut[p] = {'A': 'C', 'C': 'G', 'G': 'T', 'T': 'A'}[mut[p]]
del mut[85:88]                          # 3-nt deletion at 85..87 -> query length 147
query = ''.join(mut)
L, R = rnd(600), rnd(400)
target = L + seg + R                    # segment (unmutated) sits at target[600:750]
open('data/synthetic_local_target.txt', 'w').write(target); open('data/synthetic_local_query.txt', 'w').write(query)
print("SYNTHETIC: target", len(target), "query", len(query), "planted at target[600:750]")
al = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
A = al.align(target, query)[0]
print(A.aligned.tolist())
# ground truth
S = lambda a, b: 2 if a == b else -1
ref = gotoh_score(target, query, S, 10, 0.5, 'local')
ps = parasail.sw_trace_scan_16(query, target, 10, 1, parasail.matrix_create('ACGT', 2, -1))  # parasail integer penalties; compare below with 10/1
print("own Gotoh local 10/0.5:", ref, "| Biopython:", A.score)
check("Biopython local score == independent Gotoh local", abs(A.score - ref) < 1e-9, f"{A.score} vs {ref}")
# Expected by construction: 150-3-5 = 142 matches*2 = 284; 5 mismatches -5 ... alignment: 142 matches, 5 mismatches, one 3-gap (10+0.5*2=11)
exp = 142 * 2 - 5 * 1 - (10 + 0.5 * 2)
check("score equals hand-derived planted-alignment score (142 matches, 5 mm, one 3-nt gap)", A.score == exp, f"{A.score} vs {exp}")
t0, t1 = A.aligned[0][0][0], A.aligned[0][-1][1]
check("aligned target span == planted [600,750]", (t0, t1) == (600, 750), (int(t0), int(t1)))
c = A.counts()
check("counts: mismatches==5 identities==142 gaps==3", (c.mismatches, c.identities, c.gaps) == (5, 142, 3), (c.identities, c.mismatches, c.gaps))
# the example in the skill: alignment.aligned prints coordinates
print("aligned[0] (target):", A.aligned[0].tolist(), " aligned[1] (query):", A.aligned[1].tolist())
# parasail with integer gap 10/1 equivalent Biopython 10/1
al2 = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
pm = parasail.matrix_create('ACGT', 2, -1)
p = parasail.sw_trace_scan_16(target, query, 10, 1, pm)
check("Biopython local 10/1 == parasail sw 10/1", al2.score(target, query) == p.score, f"{al2.score(target, query)} vs {p.score}")
# reverse-complement query: SKILL never mentions strand
from Bio.Seq import Seq
rc = str(Seq(query).reverse_complement())
r2 = al.align(target, rc)
print("revcomp query best local score:", r2.score if len(r2) else 0, "(vs forward", A.score, ") -> skill gives no strand/orientation guidance")
# SKILL example local_alignment: NNNNN flank / exact substring
la = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
X = la.align('NNNNNACCGGTAACGTAGNNNNNNNN', 'ACCGGTAACGTAG')[0]
check("local_alignment.py example: score 26 & target span [5,18]", X.score == 26 and X.aligned[0].tolist() == [[5, 18]], (X.score, X.aligned[0].tolist()))
# --- new for the 2026-09-19 fix: Skill "Input Checks -> Strand": score both orientations, keep the higher
fwd = al.score(target, query); rcs = al.score(target, rc)
print("forward", fwd, "reverse-complement", rcs)
check("Skill: reverse-complemented query scores far lower than forward (alignment is strand-specific)", rcs < 0.3 * fwd, (fwd, rcs))
unknown = rc   # user hands us the read in unknown orientation
best = max([(al.score(target, unknown), 'as given'), (al.score(target, str(Seq(unknown).reverse_complement())), 'revcomp')])
check("Skill's recipe (score seq and its reverse complement, keep the higher) recovers the planted score 268 from the flipped read", best == (268.0, 'revcomp'), best)
# Skill: 30-nt exact match scored 60, reverse complement 0
ex = 'GATTACAGATTACCAGGCTAGGCATCGAT'  # 29 nt; extend to 30 by one base
ex = ex + 'C'
ref = 'TTTT' * 10 + ex + 'GGGG' * 10
sc_f = al.score(ref, ex); sc_r = al.score(ref, str(Seq(ex).reverse_complement()))
print("30-nt exact:", sc_f, "revcomp:", sc_r)
check("Skill: a 30-nt exact match scores 60 (2 x 30) in local 2/-1", sc_f == 60, sc_f)
summary()
