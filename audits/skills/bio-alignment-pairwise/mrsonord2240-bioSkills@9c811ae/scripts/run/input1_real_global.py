"""Input 1 (canonical, REAL data): global protein alignment of human HBA (P69905) vs HBB (P68871), BLOSUM62,
Skill's protein config (open -11, extend -1) and the EMBOSS-style -10/-0.5.
Ground truth: (a) auditor's own Gotoh DP, (b) parasail, (c) EMBOSS needle (run separately in WSL, input1_needle.sh)."""
from common import *
import parasail
from ref_gotoh import load_matrix, gotoh_score
a, b = prot('P69905'), prot('P68871')
SeqIO.write([a, b], r'F:\OpenScience\audits\bio-alignment-pairwise\run\data\hba_hbb.fasta', 'fasta')
B62 = substitution_matrices.load('BLOSUM62'); Bd = load_matrix('BLOSUM62')
print(len(a.seq), len(b.seq))
for (o, e) in [(11, 1), (10, 0.5)]:
    al = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-o, extend_gap_score=-e)
    A = al.align(a.seq, b.seq)[0]
    ref = gotoh_score(str(a.seq), str(b.seq), Bd, o, e, 'global')
    check(f"global BLOSUM62 {o}/{e}: Biopython score == independent Gotoh", abs(A.score - ref) < 1e-9, f"{A.score} vs {ref}")
    if e == int(e):
        p = parasail.nw_trace_scan_16(str(a.seq), str(b.seq), o, int(e), parasail.blosum62)
        check(f"  == parasail nw (open={o}, ext={int(e)})", A.score == p.score, f"{A.score} vs {p.score}")
    # counts vs manual recount from aligned strings
    s0, s1 = A[0, :], A[1, :]
    ident = sum(1 for x, y in zip(s0, s1) if x == y and x != '-')
    mism = sum(1 for x, y in zip(s0, s1) if x != y and x != '-' and y != '-')
    gaps = sum(1 for x, y in zip(s0, s1) if x == '-' or y == '-')
    c = A.counts()
    check("  counts() identities/mismatches/gaps == manual recount", (c.identities, c.mismatches, c.gaps) == (ident, mism, gaps), f"{(c.identities, c.mismatches, c.gaps)} vs {(ident, mism, gaps)}")
    pid2 = c.identities / (c.identities + c.mismatches) * 100
    print(f"  identities={c.identities} mism={c.mismatches} gaps={c.gaps}  PID2={pid2:.1f}%  aln_len={len(s0)}  PID1(cols)={ident/len(s0)*100:.1f}%")
    # rescore the alignment strings independently: sum of substitution scores + gap costs
    sc = 0; ingap = None
    for x, y in zip(s0, s1):
        if x == '-' or y == '-':
            g = 'x' if x == '-' else 'y'
            sc -= (e if ingap == g else o); ingap = g
        else:
            sc += Bd[(x, y)]; ingap = None
    check("  re-score of returned alignment strings == reported score", abs(sc - A.score) < 1e-9, f"{sc} vs {A.score}")
    if (o, e) == (10, 0.5):
        print(A)
# Skill's DNA-style claim: score() == align().score
al = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)
check("aligner.score() == align()[0].score", al.score(a.seq, b.seq) == al.align(a.seq, b.seq)[0].score)
check("Biopython score is deterministic across 3 runs", len({al.align(a.seq, b.seq)[0].score for _ in range(3)}) == 1)
print("n optimal alignments:", len(al.align(a.seq, b.seq)))
# --- new checks for the 2026-09-19 fix: Skill's "Gap Penalties" section numbers
dflt = PairwiseAligner(mode='global', substitution_matrix=B62)
d0 = PairwiseAligner()
check("Skill: PairwiseAligner() defaults are match 1 / mismatch 0 / open -1 / extend -1", (d0.match_score, d0.mismatch_score, d0.open_gap_score, d0.extend_gap_score) == (1.0, 0.0, -1.0, -1.0), (d0.match_score, d0.mismatch_score, d0.open_gap_score, d0.extend_gap_score))
def frag(A):
    return sum(str(A[0, :]).count('-') + str(A[1, :]).count('-') for _ in [0]), len(A.aligned[0])
g0, b0 = frag(dflt.align(a.seq, b.seq)[0])
g1, b1 = frag(PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1).align(a.seq, b.seq)[0])
print("default gaps: gap positions", g0, "aligned blocks", b0, "| -11/-1: gap positions", g1, "aligned blocks", b1)
check("Skill: '55 gap positions in 37 aligned blocks with defaults, 9 in 5 at -11/-1'", (g0, b0, g1, b1) == (55, 37, 9, 5), (g0, b0, g1, b1))
summary()
