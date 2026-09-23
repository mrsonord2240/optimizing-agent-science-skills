"""Input 7 (Adversarial): user pushes on things the pre-fix Skill got wrong or that are easy to misread:
(i) 'just use pairwise2', (ii) 'set aligner.max_alignments as the guide says' + repetitive input, (iii) 'percent identity like EMBOSS 43.6%',
(iv) IUPAC DNA with NUC.4.4, (v) 'aligner.algorithm' names, (vi) SKILL.md's Alignment Output / Counts recipe, (vii) formats.
Real data: HBA_HUMAN vs HBB_HUMAN. Ground truth: EMBOSS needle 65/149 = 43.6%, pwalign pid(), hand sums."""
import itertools, warnings, re
from common import *
from Bio.Seq import Seq
txt = open(r'F:\OpenScience\audits\bio-alignment-pairwise\run\skill\SKILL.md', encoding='utf-8').read()
a, b = prot('P69905').seq, prot('P68871').seq
B62 = substitution_matrices.load('BLOSUM62')
# (i) pairwise2 (Skill: deprecated in 1.80; not yet removed)
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always')
    from Bio import pairwise2
    r = pairwise2.align.globalds(str(a), str(b), B62, -10, -0.5, one_alignment_only=True)
al = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-10, extend_gap_score=-0.5)
check("Skill: Bio.pairwise2 deprecated (warning emitted) but not removed; agrees with PairwiseAligner 292.5", any('deprecated' in str(w.message).lower() for w in W) and r[0].score == al.score(a, b) == 292.5, r[0].score)
# (ii) max_alignments
al2 = PairwiseAligner(mode='global', match_score=1, mismatch_score=0, open_gap_score=0, extend_gap_score=0)
try: al2.max_alignments = 100; ok = True
except AttributeError as e: ok = False; print("aligner.max_alignments = 100 ->", type(e).__name__, e)
check("Skill states 'PairwiseAligner has no max_alignments on 1.88 (assignment raises AttributeError)': confirmed", ok is False)
check("Skill no longer tells the agent to SET aligner.max_alignments (grep of SKILL.md + usage-guide.md)", 'max_alignments = ' not in txt and 'max_alignments' not in open(r'F:\OpenScience\audits\bio-alignment-pairwise\run\skill\usage-guide.md', encoding='utf-8').read().replace('no `max_alignments`', ''), "")
rep = al2.align('A' * 40 + 'C' * 40, 'A' * 20 + 'C' * 20 + 'A' * 20)
try: len(rep); ov = False
except OverflowError as e: ov = True; print("len(alignments) ->", type(e).__name__, str(e)[:80])
check("Skill: len(alignments) raises OverflowError for zero gap penalties on repetitive input", ov)
got = [x.score for x in itertools.islice(rep, 5)]
check("Skill: itertools.islice(alignments, 5) still works there", len(got) == 5, got)
# the Iterating snippet on the real pair
alignments = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1).align(a, b)
print("n optimal HBA/HBB alignments:", len(alignments))
# (iii) PID
A = al.align(a, b)[0]; c = A.counts(); L = len(A[0, :])
pid1 = 100 * c.identities / L; pid2 = 100 * c.identities / (c.identities + c.mismatches); pid3 = 100 * c.identities / min(len(a), len(b)); pid4 = 100 * c.identities / ((len(a) + len(b)) / 2)
print(f"PID1={pid1:.1f} PID2={pid2:.1f} PID3={pid3:.1f} PID4={pid4:.1f}")
check("Skill: four PID definitions: PID1 == EMBOSS needle 43.6% (65/149); PID2 highest; PID3 45.8, PID4 45.0 (Biostrings pid())", round(pid1, 1) == 43.6 and pid2 == max(pid1, pid2, pid3, pid4) and round(pid3, 1) == 45.8 and round(pid4, 1) == 45.0)
check("Skill: counts() recipe gives PID2 (46.4), not EMBOSS's 43.6, and the Skill says so ('similar to PID2')", round(pid2, 1) == 46.4 and 'similar to PID2' in txt, round(pid2, 1))
spread = max(pid1, pid2, pid3, pid4) - min(pid1, pid2, pid3, pid4)
print("PID spread on this alignment:", round(spread, 1), "(Skill: up to 11.5 points across methods, literature)")
# (iv) NUC.4.4
nuc = substitution_matrices.load('NUC.4.4')
nl = PairwiseAligner(mode='global', substitution_matrix=nuc, open_gap_score=-10, extend_gap_score=-0.5)
q, t = 'ACGTRYNACGT', 'ACGTAGCACGT'
hand = sum(nuc[x, y] for x, y in zip(q, t))
check("Skill: NUC.4.4 match +5 / mismatch -4, R vs A = +1; IUPAC alignment score == hand sum of cells", (nuc['A', 'A'], nuc['A', 'C'], nuc['R', 'A']) == (5, -4, 1) and nl.score(t, q) == hand, (nl.score(t, q), hand))
names = substitution_matrices.load()
check("Skill: substitution_matrices.load() lists 30 matrices; HOXD70 present", len(names) == 30 and 'HOXD70' in names, len(names))
# (v) aligner.algorithm names
def algo(**kw): return PairwiseAligner(**kw).algorithm
w = PairwiseAligner(mode='global'); w.gap_score = lambda pos, length: -2.0 - 0.5 * length   # callable gap function -> Waterman-Smith-Beyer
wl = PairwiseAligner(mode='local'); wl.gap_score = lambda pos, length: -2.0 - 0.5 * length
got = {algo(mode='global', open_gap_score=-1, extend_gap_score=-1), algo(mode='local', open_gap_score=-1, extend_gap_score=-1), algo(mode='global', open_gap_score=-10, extend_gap_score=-0.5), algo(mode='local', open_gap_score=-10, extend_gap_score=-0.5), w.algorithm, wl.algorithm}
print(sorted(got))
claimed = {'Needleman-Wunsch', 'Smith-Waterman', 'Gotoh global alignment algorithm', 'Gotoh local alignment algorithm', 'Waterman-Smith-Beyer global alignment algorithm', 'Waterman-Smith-Beyer local alignment algorithm'}
check("Skill: aligner.algorithm returns exactly the six names listed", got == claimed, got ^ claimed)
# (vi) Alignment Output block in SKILL.md
al3 = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
out = str(al3.align(Seq('ACCGGTAACGTAG'), Seq('ACCGTTAACGAAG'))[0]).strip().splitlines()
blk = re.search(r'## Alignment Output Format\s+```\n(.*?)```', txt, re.S).group(1).strip().splitlines()
check("Skill: the printed 'Alignment Output Format' block equals the real output line-for-line", [l.rstrip() for l in out] == [l.rstrip() for l in blk], (out[1], blk[1]))
# (vii) formats
x = al3.align(Seq('ACCGGTAACGTAG'), Seq('ACCGTTAACGAAG'))[0]
fm = {f: format(x, f) for f in ('fasta', 'clustal', 'psl', 'sam')}
check("Skill: format(alignment, 'fasta'|'clustal'|'psl'|'sam') all work and are non-empty", all(len(v) > 20 for v in fm.values()), {k: len(v) for k, v in fm.items()})
sub = x.substitutions
check("Skill: alignment.substitutions['G','T'] == 1 (one G aligned to T)", sub['G', 'T'] == 1, sub['G', 'T'])
summary()
