r"""Input 5 (Stress): the Skill's 'Pairwise Library Selection' claims re-measured. All DNA SYNTHETIC (seeds 5/9/3), injected edits known.
Run on Windows venv (timing claims are 'Windows, score only') and in WSL env alignment (pywfa/mappy). Assertions on values, not exit codes."""
import random, time, sys, warnings; warnings.simplefilter('ignore')
from Bio.Align import PairwiseAligner
import parasail, edlib
F = []
def check(n, c, o=""):
    print(("PASS  " if c else "FAIL  ") + n + " | " + str(o)); (None if c else F.append(n))
random.seed(5)
def rnd(n): return ''.join(random.choice('ACGT') for _ in range(n))
def mutate(s, rate):
    out, edits = [], 0
    for ch in s:
        r = random.random()
        if r < rate / 3: out.append(random.choice([c for c in 'ACGT' if c != ch])); edits += 1
        elif r < 2 * rate / 3: edits += 1
        elif r < rate: out.append(ch); out.append(random.choice('ACGT')); edits += 1
        else: out.append(ch)
    return ''.join(out), edits
T = rnd(4000); Q, inj = mutate(T, 0.03)
mat = parasail.matrix_create('ACGT', 2, -1)
aff = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
loc = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-1)
lev = PairwiseAligner(mode='global', match_score=0, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1)
print(f"SYNTHETIC target {len(T)} nt, query {len(Q)} nt, injected edits {inj}; platform {sys.platform}; parasail {parasail.__version__ if hasattr(parasail,'__version__') else ''}")
# correctness
check("Skill snippet: parasail nw_striped_sat(query, target, 10, 1, mat) == Biopython affine global (score(target, query))", parasail.nw_striped_sat(Q, T, 10, 1, mat).score == aff.score(T, Q), (parasail.nw_striped_sat(Q, T, 10, 1, mat).score, aff.score(T, Q)))
check("Skill: sw_striped_sat for local == Biopython local", parasail.sw_striped_sat(Q, T, 10, 1, mat).score == loc.score(T, Q), (parasail.sw_striped_sat(Q, T, 10, 1, mat).score, loc.score(T, Q)))
ed = edlib.align(Q, T, mode='NW', task='distance')['editDistance']
check("Skill: edlib NW distance == -Levenshtein (Biopython match 0, mismatch -1, gaps -1)", ed == -lev.score(T, Q) and ed <= inj, (ed, -lev.score(T, Q), inj))
# edlib HW = query anywhere in target (semi-global with free target ends) -> compare with Biopython Levenshtein with free end gaps on target
frag = T[1500:1560]; fm, fe = mutate(frag, 0.05)
hw = edlib.align(fm, T, mode='HW', task='distance')['editDistance']
sg = PairwiseAligner(mode='global', match_score=0, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1)
sg.open_left_deletion_score = sg.extend_left_deletion_score = sg.open_right_deletion_score = sg.extend_right_deletion_score = 0   # free unaligned target ends (align(target, query): deletion = target base vs gap): query aligns completely, anywhere in target
check("Skill: edlib mode 'HW' = query anywhere in target == Biopython Levenshtein with free target ends (deletion end gaps = 0)", hw == -sg.score(T, fm) and hw <= fe, (hw, -sg.score(T, fm), fe))
# protein through edlib ('any alphabet' claim)
p1, p2 = 'MVLSPADKTNVKAAWGKVGAHAGEYGAEAL', 'MVHLTPEEKSAVTALWGKVNVDEVGGEAL'
ep = edlib.align(p1, p2, mode='NW', task='distance')['editDistance']
lp = PairwiseAligner(mode='global', match_score=0, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1).score(p1, p2)
check("Skill table: edlib works on any alphabet (protein NW distance == -Levenshtein)", ep == -lp, (ep, -lp))
# pywfa / mappy (WSL only)
if sys.platform.startswith('linux'):
    from pywfa import WavefrontAligner
    x, o, e = 4, 6, 2
    bio = PairwiseAligner(mode='global', match_score=0, mismatch_score=-x, open_gap_score=-(o + e), extend_gap_score=-e)
    r = WavefrontAligner(T, span='end-to-end', mismatch=x, gap_opening=o, gap_extension=e)(Q)
    check("Skill: pywfa score == Biopython(match 0, mismatch -x, open -(o+e), extend -e)", r.score == bio.score(T, Q), (r.score, bio.score(T, Q)))
    import mappy, tempfile, os
    ref = rnd(3000) + T[:2000] + rnd(3000); read, _ = mutate(T[500:1500], 0.04)
    fa = tempfile.NamedTemporaryFile('w', suffix='.fa', delete=False); fa.write('>ref\n' + ref + '\n'); fa.close()
    hits = list(mappy.Aligner(fa.name, preset='map-ont').map(read)); os.unlink(fa.name)
    check("Skill: mappy hit fields ctg/r_st/r_en/mapq/cigar_str; locus within 30 nt of planted 3500", hits and abs(hits[0].r_st - 3500) < 30 and hits[0].cigar_str, [(h.ctg, h.r_st, h.r_en, h.mapq) for h in hits])
# speed table (Windows)
random.seed(9)
pairs = []
for _ in range(1000):
    a = rnd(300); b, _ = mutate(a, 0.05); pairs.append((a, b))
def bench(f, reps=3):
    best, res = 1e9, None
    for _ in range(reps):
        t = time.perf_counter(); res = [f(a, b) for a, b in pairs]; best = min(best, time.perf_counter() - t)
    return best, res
t_bp, r_bp = bench(lambda a, b: aff.score(a, b))
t_bl, r_bl = bench(lambda a, b: lev.score(a, b))
t_s, r_s = bench(lambda a, b: parasail.nw_striped_sat(b, a, 10, 1, mat).score)
t_c, r_c = bench(lambda a, b: parasail.nw_scan_sat(b, a, 10, 1, mat).score)
t_e, r_e = bench(lambda a, b: edlib.align(b, a, mode='NW', task='distance')['editDistance'])
check("1000 pairs: Biopython == parasail striped_sat == parasail scan_sat, every pair", r_bp == r_s == r_c, sum(x == y == z for x, y, z in zip(r_bp, r_s, r_c)))
check("1000 pairs: Levenshtein == -edlib, every pair", r_bl == [-d for d in r_e], sum(x == -y for x, y in zip(r_bl, r_e)))
sp_s, sp_c, ed_l, ed_a = t_bp / t_s, t_bp / t_c, t_bl / t_e, t_bp / t_e
print(f"300 nt x1000: Biopython affine {t_bp:.3f}s | parasail striped_sat {t_s:.3f}s ({sp_s:.1f}x) scan_sat {t_c:.3f}s ({sp_c:.1f}x) | Biopython Levenshtein {t_bl:.3f}s | edlib {t_e:.4f}s ({ed_l:.0f}x vs Levenshtein, {ed_a:.0f}x vs affine)")
check("Skill table: parasail 2-10x at 300 nt (allow >=1.5x; timings vary run to run)", 1.5 <= max(sp_s, sp_c) <= 15, (round(sp_s, 1), round(sp_c, 1)))
check("Skill: edlib 15x vs Levenshtein and 26x vs affine at 300 nt (accept >= 10x and >= 15x)", ed_l >= 10 and ed_a >= 15, (round(ed_l), round(ed_a)))
random.seed(3); T2 = rnd(20000); Q2, _ = mutate(T2, 0.03)
t = time.perf_counter(); s_bp = aff.score(T2, Q2); tb = time.perf_counter() - t
t = time.perf_counter(); s_ps = parasail.nw_striped_sat(Q2, T2, 10, 1, mat); tp = time.perf_counter() - t
t = time.perf_counter(); d = edlib.align(Q2, T2, mode='NW', task='distance')['editDistance']; te = time.perf_counter() - t
print(f"20 kb @3%: Biopython {tb:.2f}s  parasail striped_sat {tp:.3f}s ({tb/tp:.0f}x)  edlib {te:.4f}s ({tb/te:.0f}x); true affine score {s_bp}")
check("Skill: 20 kb parasail ~3-8x (accept 2-15x)", 2 <= tb / tp <= 15, round(tb / tp, 1))
check("Skill: 20 kb edlib 400x+ (accept >= 300x)", tb / te >= 300, round(tb / te))
check("20 kb: parasail nw_striped_sat == Biopython", s_ps.score == s_bp and not s_ps.saturated, (s_ps.score, s_bp))
r16 = parasail.nw_striped_16(Q2, T2, 10, 1, mat)
print("nw_striped_16 20 kb:", r16.score, "saturated", r16.saturated)
check("Skill: fixed-width nw_striped_16 on a 20 kb pair silently saturates (score 0/wrong, .saturated True); true score > 32767", r16.saturated and r16.score != s_bp and s_bp > 32767, (r16.score, r16.saturated, s_bp))
print("FAILED:", F if F else "none")
