"""Input 3 (Edge): (a) semiglobal fragment-in-reference exactly as SKILL.md snippets, (b) length-mismatch global vs local trap,
(c) off-spec inputs the skill does not mention: lowercase, stop '*', 'U', empty sequence, SeqRecord instead of .seq, BLOSUM62 with default gaps."""
import random, warnings
from common import *
from Bio.Seq import Seq
from ref_gotoh import semiglobal_score, gotoh_score
random.seed(11)
rnd = lambda n: ''.join(random.choice('ACGT') for _ in range(n))
ref = rnd(300) + 'GATTACAGATTACCAGGCTA' + rnd(300)     # SYNTHETIC reference; 20-nt fragment at [300,320]
frag = 'GATTACAGATTACCAGGCTA'
# (a1) skill's 'free end gaps on query' snippet, taken literally (only end gaps set, scoring left at defaults + set match=2)
al = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
al.query_left_open_gap_score = 0; al.query_left_extend_gap_score = 0; al.query_right_open_gap_score = 0; al.query_right_extend_gap_score = 0
A = al.align(ref, frag)[0]                           # target=ref, query=frag (skill: 'fragment against full-length reference')
print(A.aligned.tolist())
check("(a1) free-QUERY-end-gaps, target=ref, query=fragment: score = 2*20 = 40", A.score == 40, A.score)
check("(a1) target span == [300,320]", A.aligned[0].tolist() == [[300, 320]], A.aligned[0].tolist())
# (a1') reversed argument order (align(fragment, ref)) with the same aligner -> what happens
B_ = al.align(frag, ref)[0]
print("(a1') align(fragment, ref) with query_* free: score", B_.score, "(fragment gapped against 300+300 flanks costs)")
check("(a1') snippet is orientation-dependent: swapping argument order does NOT give 40", B_.score != 40, B_.score)
# (a2) end_gap_score = 0 : free end gaps on both
al2 = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5); al2.end_gap_score = 0.0
check("(a2) end_gap_score=0: both orders give 40", al2.align(ref, frag).score == 40 and al2.align(frag, ref).score == 40, (al2.align(ref, frag).score, al2.align(frag, ref).score))
# ground truth: own semiglobal DP
S = lambda a, b: 2 if a == b else -1
# with a mutated fragment
fm = list(frag); fm[5] = 'T'; del fm[12]; fm = ''.join(fm)
g = semiglobal_score(ref, fm, S, 10, 0.5)
check("(a3) mutated fragment: Biopython end_gap_score=0 == independent semiglobal DP", al2.score(ref, fm) == g, (al2.score(ref, fm), g))
# (b) global vs local vs semiglobal on very different lengths
gl = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
lo = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
print(f"(b) 20-nt fragment vs 620-nt reference: global={gl.score(ref, frag)} local={lo.score(ref, frag)} semiglobal={al2.score(ref, frag)}")
check("(b) global < local == semiglobal (forced terminal gaps penalised)", gl.score(ref, frag) < lo.score(ref, frag) == al2.score(ref, frag), (gl.score(ref, frag), lo.score(ref, frag)))
# (c) off-spec inputs
B62 = substitution_matrices.load('BLOSUM62')
pa = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)
def tryit(label, f):
    try:
        r = f(); print(f"  [{label}] OK ->", r)
    except Exception as e:
        print(f"  [{label}] {type(e).__name__}: {str(e)[:110]}")
print("(c) off-spec inputs:")
tryit("lowercase protein", lambda: pa.score('mkvlaa', 'MKVLAA'))
tryit("stop codon '*'", lambda: pa.score('MKVL*', 'MKVLA'))
tryit("X / B / Z", lambda: pa.score('MKXBZ', 'MKVLA'))
tryit("selenocysteine U", lambda: pa.score('MKUL', 'MKCL'))
tryit("J (Leu/Ile)", lambda: pa.score('MKJL', 'MKLL'))
tryit("empty query", lambda: pa.align('MKVL', '').score)
tryit("empty both", lambda: pa.align('', '').score)
tryit("SeqRecord passed instead of .seq", lambda: pa.score(prot('P69905'), prot('P68871')))
tryit("SeqRecord.seq", lambda: pa.score(prot('P69905').seq, prot('P68871').seq))
tryit("protein w/ trailing newline/space", lambda: pa.score('MKVL\n', 'MKVL'))
tryit("DNA aligner (match/mismatch) with lowercase vs uppercase", lambda: (gl.score('acgt', 'ACGT'), 'lowercase treated as different letters'))
tryit("RNA vs DNA (U vs T) match/mismatch aligner", lambda: gl.score('ACGU', 'ACGT'))
nuc = substitution_matrices.load('NUC.4.4')
nl = PairwiseAligner(mode='global', substitution_matrix=nuc, open_gap_score=-10, extend_gap_score=-0.5)
tryit("NUC.4.4 with RNA 'U'", lambda: nl.score('ACGU', 'ACGU'))
tryit("NUC.4.4 lowercase", lambda: nl.score('acgt', 'acgt'))
tryit("NUC.4.4 IUPAC R vs A", lambda: nl.score('R', 'A'))
# (d) default-gap trap of the skill: BLOSUM62 with defaults
dflt = PairwiseAligner(mode='global', substitution_matrix=B62)
print("(d) defaults open/extend on 1.88:", dflt.open_gap_score, dflt.extend_gap_score)
check("(d) SKILL claim 'default gaps are 0' true on Biopython 1.88", dflt.open_gap_score == 0 and dflt.extend_gap_score == 0, (dflt.open_gap_score, dflt.extend_gap_score))
hba, hbb = prot('P69905').seq, prot('P68871').seq
Dg = dflt.align(hba, hbb)[0]; Pg = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1).align(hba, hbb)[0]
def ngapsegs(A):
    return sum(1 for s in (A[0, :], A[1, :]) for _ in __import__('re').finditer(r'-+', s))
print("    gap segments: default-gap aligner", ngapsegs(Dg), "score", Dg.score, "| -11/-1 aligner", ngapsegs(Pg), "score", Pg.score)
summary()
