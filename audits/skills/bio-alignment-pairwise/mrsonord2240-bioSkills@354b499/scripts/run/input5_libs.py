"""Input 5 (Stress / multi-part): 'Skill's library-selection table': Biopython vs parasail vs edlib vs pywfa vs mappy on SYNTHETIC long DNA
(random seed 5) with a known number of injected edits. Run in WSL env alignment: wsl_run.sh 'python /mnt/openscience/audits/.../input5_libs.py'
Ground truth: injected-edit upper bound, own scoring identities between libraries, timing measured here."""
import random, time, sys, warnings; warnings.simplefilter('ignore')
import numpy as np
from Bio.Align import PairwiseAligner
import parasail, edlib
FAILS = []
def check(n, c, o=""):
    print(("PASS  " if c else "FAIL  ") + n + " | " + str(o)); (None if c else FAILS.append(n))
random.seed(5)
def rnd(n): return ''.join(random.choice('ACGT') for _ in range(n))
def mutate(s, rate):
    out, edits = [], 0
    for ch in s:
        r = random.random()
        if r < rate / 3: out.append(random.choice([c for c in 'ACGT' if c != ch])); edits += 1     # substitution
        elif r < 2 * rate / 3: edits += 1                                                        # deletion
        elif r < rate: out.append(ch); out.append(random.choice('ACGT')); edits += 1            # insertion
        else: out.append(ch)
    return ''.join(out), edits
T = rnd(4000); Q, inj = mutate(T, 0.03)
print(f"SYNTHETIC target {len(T)} nt, query {len(Q)} nt, injected edits {inj}")
# 1. Levenshtein: Biopython (match 0, mismatch -1, gaps -1) == -edlib distance
lev = PairwiseAligner(mode='global', match_score=0, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1)
print("algorithm:", lev.algorithm)
bp = lev.score(T, Q)
ed = edlib.align(Q, T, mode='NW')['editDistance']
check("Biopython Levenshtein score == -edlib NW editDistance", bp == -ed, (bp, ed))
check("edit distance <= injected edits", ed <= inj, (ed, inj))
# 2. affine DNA: Biopython == parasail
aff = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
mat = parasail.matrix_create('ACGT', 2, -1)
pa = parasail.nw_scan_16(Q, T, 10, 1, mat).score
check("Biopython affine global 2/-1 open10/ext1 == parasail nw", aff.score(T, Q) == pa, (aff.score(T, Q), pa))
loc = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
ps = parasail.sw_scan_16(Q, T, 10, 1, mat).score
check("Biopython local == parasail sw", loc.score(T, Q) == ps, (loc.score(T, Q), ps))
# 3. pywfa
try:
    from pywfa import WavefrontAligner
    # WFA2 gap-affine: gap of length L costs o + e*L ; Biopython open=-(o+e), extend=-e ; mismatch x ; match 0
    x, o, e = 4, 6, 2
    bio = PairwiseAligner(mode='global', match_score=0, mismatch_score=-x, open_gap_score=-(o + e), extend_gap_score=-e)
    A = WavefrontAligner(T, span='end-to-end', mismatch=x, gap_opening=o, gap_extension=e)
    r = A(Q)
    print("pywfa score:", r.score, "cigar head:", r.cigarstring[:60])
    check("Biopython gap-affine score == pywfa score (WFA2 cost model mapped)", abs(bio.score(T, Q) - r.score) < 1e-9 or abs(bio.score(T, Q) + abs(r.score)) < 1e-9, (bio.score(T, Q), r.score))
except Exception as ex:
    print("pywfa ERROR:", type(ex).__name__, ex)
# 4. mappy
try:
    import mappy, tempfile, os
    ref = rnd(3000) + T[:2000] + rnd(3000)
    read, _ = mutate(T[500:1500], 0.04)
    fa = tempfile.NamedTemporaryFile('w', suffix='.fa', delete=False); fa.write('>ref\n' + ref + '\n'); fa.close()
    a = mappy.Aligner(fa.name, preset='map-ont'); hits = list(a.map(read))
    print("mappy hits:", [(h.ctg, h.r_st, h.r_en, h.mapq, h.cigar_str[:40]) for h in hits])
    exp0 = 3000 + 500
    check("mappy locates read within 30 nt of planted position", hits and abs(hits[0].r_st - exp0) < 30, (hits[0].r_st if hits else None, exp0))
    os.unlink(fa.name)
except Exception as ex:
    print("mappy ERROR:", type(ex).__name__, ex)
# 5. speed claims: 1000 pairs, ~300 nt, ~5% divergence, score only
random.seed(9)
pairs = []
for _ in range(1000):
    a = rnd(300); b, _ = mutate(a, 0.05); pairs.append((a, b))
def bench(f, reps=1):
    t = time.perf_counter()
    for _ in range(reps): r = [f(a, b) for a, b in pairs]
    return (time.perf_counter() - t) / reps, r
t_bp, r_bp = bench(lambda a, b: aff.score(a, b))
t_ps, r_ps = bench(lambda a, b: parasail.nw_scan_16(b, a, 10, 1, mat).score)
t_ps2, r_ps2 = bench(lambda a, b: parasail.nw_striped_16(b, a, 10, 1, mat).score)
t_ed, r_ed = bench(lambda a, b: edlib.align(b, a, mode='NW', task='distance')['editDistance'])
t_bpl, r_bpl = bench(lambda a, b: lev.score(a, b))
check("1000 pairs: Biopython == parasail scores for every pair", r_bp == r_ps, sum(x == y for x, y in zip(r_bp, r_ps)))
check("1000 pairs: Levenshtein via Biopython == -edlib distance for every pair", r_bpl == [-d for d in r_ed], sum(x == -y for x, y in zip(r_bpl, r_ed)))
print(f"timing 1000 x 300nt (score only): Biopython affine {t_bp:.3f}s | parasail nw_scan {t_ps:.3f}s ({t_bp/t_ps:.1f}x) | parasail striped {t_ps2:.3f}s ({t_bp/t_ps2:.1f}x) | Biopython Levenshtein {t_bpl:.3f}s | edlib {t_ed:.4f}s ({t_bpl/t_ed:.0f}x vs Biopython Levenshtein, {t_bp/t_ed:.0f}x vs affine)")
# larger pair
random.seed(3); T2 = rnd(20000); Q2, _ = mutate(T2, 0.02)
t = time.perf_counter(); s_bp = aff.score(T2, Q2); tb = time.perf_counter() - t
t = time.perf_counter(); s_ps = parasail.nw_striped_16(Q2, T2, 10, 1, mat).score; tp = time.perf_counter() - t
t = time.perf_counter(); d = edlib.align(Q2, T2, mode='NW', task='distance')['editDistance']; te = time.perf_counter() - t
print(f"20 kb x 20 kb @2%: Biopython {tb:.2f}s  parasail {tp:.3f}s ({tb/tp:.0f}x)  edlib {te:.4f}s ({tb/te:.0f}x)")
res16 = parasail.nw_striped_16(Q2, T2, 10, 1, mat)
print("parasail 16-bit saturated flag:", res16.saturated, "(score returned", res16.score, ")")
s_ps32 = parasail.nw_striped_32(Q2, T2, 10, 1, mat).score
check("20 kb: Biopython == parasail 32-bit (16-bit variant saturates: skill gives no warning)", s_bp == s_ps32, (s_bp, s_ps32))
check("20 kb: parasail 16-bit silently returns wrong score unless flag is checked", s_ps != s_bp and res16.saturated, (s_ps, s_bp))
print("\nFAILED:", FAILS if FAILS else "none")
