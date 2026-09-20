"""INPUT 7 (adversarial, regression + new edges): the collaborator's messy alignment (mixed case, '.' gaps, X/B/Z/U/'*', an
all-gap row) [synthetic, from the first audit], degenerate alignments, and probes of the NEW behaviours the fix introduced:
min_occupancy NaN default, is_nucleotide() auto-detection, average_conservation (mean, n) return type.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b07_input7_messy_and_edges.py"""
import os, sys, json, shutil, io, contextlib, itertools, math, subprocess, warnings
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks, ref, numpy as np
import msa_utils, identity_matrix as IM, entropy_analysis as EA, conservation_profile as CP, capra_singh_jsd as CS, pssm as PS
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment, substitution_matrices
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
W = os.path.join(HERE, 'work_b07'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)

# ---------- A. messy collaborator alignment ----------
messy = ['MKV.LAAGXW', 'mkvALAAGVw', 'MKVBLAZGVW', 'MKVULAA*VW', '----------', 'MKV-LAAGVW']
ids = ['r0_dot_X', 'r1_lower', 'r2_BZ', 'r3_U_star', 'r4_allgap', 'r5_clean']
fa = os.path.join(W, 'messy.fasta')
open(fa, 'w').write(''.join(f'>{i}\n{s}\n' for i, s in zip(ids, messy)))
exp = ref.norm_rows(messy)
aln = msa_utils.load_alignment(fa)
rows = [str(r.seq) for r in aln]
check('A: normalisation gives the independent rows', rows == exp, str(rows))
m2 = IM.identity_matrix_vectorized(aln, 'pid2'); m4 = IM.identity_matrix_vectorized(aln, 'pid4')
check('A: r0 vs r1 PID2 = 8/9 = 88.9% (first-audit reference; pre-fix 40.0%)', abs(m2[0, 1] - 8 / 9) < 1e-12, f'{m2[0,1]*100:.2f}%')
check('A: all-gap row: identity to every other row is NaN, diagonal NaN, not 0', np.isnan(m2[4]).all() and np.isnan(m2[:, 4]).all() and np.isnan(m4[4, 4]), f'row {m2[4]}')
avg, und = IM.average_identity(m4)
ref_vals = [ref.pid_ref(exp[a], exp[b])['PID4'] for a, b in itertools.combinations(range(6), 2) if a != 4 and b != 4]
check('A: average_identity ignores NaN and counts undefined pairs (5 pairs x 2 orders = 10)', abs(avg - np.mean(ref_vals * 2)) < 1e-12 and und == 10, f'avg {avg*100:.2f}% undefined {und}')
cols = [''.join(c) for c in zip(*rows)]
icr = [ref.ic_ref(c, ref.ROB_TRUE)[0] for c in cols]
ic = [EA.information_content(c, msa_utils.ROBINSON_BACKGROUND) for c in cols]
check('A: IC per column == reference (drop & renormalise); max within bound (pre-fix 21.3 bits)', max(abs(a - b) for a, b in zip(ic, icr)) < 1e-12 and max(ic) < 6.24, f'{[round(x, 2) for x in ic]}')
err = io.StringIO()
with contextlib.redirect_stderr(err):
    outside = msa_utils.check_alphabet(aln, msa_utils.ROBINSON_BACKGROUND)
check('A: check_alphabet reports exactly the letters outside the background (X,B,Z,U,*)', set(outside) == set('XBZU*'), err.getvalue().strip()[:200])
# SKILL.md blocks on the messy alignment
os.chdir(W); shutil.copy(fa, os.path.join(W, 'alignment.fasta'))
ns, log = skill_blocks.run_all(verbose=False)
errs = [(i, st) for i, f, st, o in log if st.startswith('ERROR')]
cm = open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read()
documented = "`ValueError: Bad letter` from `DistanceCalculator`" in cm       # Common Errors row for exactly this failure
unexpected = [(i, st) for i, st in errs if not (i == 16 and 'Bad letter' in st and documented)]
check('A: SKILL.md blocks run on the messy alignment; only the DistanceCalculator block raises, and SKILL.md documents that exact error', not unexpected, f'errors {errs}; documented in Common Errors: {documented}; block0: {[o for i,f,s,o in log if i==0][0].strip()[:100]!r}')
a2 = ns['alignment']
e2 = io.StringIO()
with contextlib.redirect_stderr(e2):
    sp = ns['sum_of_pairs'](a2)
BL = substitution_matrices.load('BLOSUM62'); spr, skipped = ref.sp_ref(exp, BL)
check('A: sum_of_pairs == reference and warns with the skipped-pair count', abs(sp - spr) < 1e-9 and f'{skipped} residue pairs' in e2.getvalue(), f'{sp} vs {spr}; skipped {skipped}; warning {e2.getvalue().strip()!r}')
asc = ns['alignment_score'](a2)
check('A: alignment_score with an all-gap row has gap/gap = 0 (== textbook)', asc == ref.sp_simple_ref(exp, gapgap=0), f'{asc}')
from Bio.Phylo.TreeConstruction import DistanceCalculator
try:
    DistanceCalculator('blosum62').get_distance(a2); r = 'ran'
except Exception as e:
    r = f'{type(e).__name__}: {str(e)[:70]}'
print('   DistanceCalculator on messy normalised alignment:', r, '(Common Errors row: ValueError Bad letter -> drop or mask ambiguity codes)')

# ---------- B. degenerate inputs ----------
print('\n--- degenerate alignments ---')
def mk(*seqs): return MultipleSeqAlignment([SeqRecord(Seq(s), id=f's{i}') for i, s in enumerate(seqs)])
one = mk('ACDEF')
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter('always'); mi = IM.identity_matrix_vectorized(one); av = IM.average_identity(mi)
check('B: 1 sequence: average identity NaN, 0 undefined pairs, no exception, no numpy warning', math.isnan(av[0]) and av[1] == 0 and not wl, f'{av}, warnings {[str(w.message)[:60] for w in wl]}')
two = mk('ACDEF', 'ACDEF'); check('B: 2 identical sequences PID1-4 = 1.0', all(abs(IM.identity_matrix_vectorized(two, m)[0, 1] - 1) < 1e-15 for m in IM.METHODS), '')
try:
    mk('ACD', 'AC'); r = 'accepted'
except Exception as e:
    r = f'{type(e).__name__}: {e}'
check('B: unequal lengths rejected by Biopython with a clear message', 'same length' in r, r)
allgapcols = mk('AC--D', 'AC--D', 'AC--E')
print('   avg identity with 1 all-gap column:', IM.average_identity(IM.identity_matrix_vectorized(allgapcols, 'pid4')))
c = [CP.column_conservation(allgapcols, i) for i in range(5)]
check('B: all-gap columns -> NaN conservation (not 0)', math.isnan(c[2]) and math.isnan(c[3]) and c[0] == 1.0, str(c))

# ---------- C. new-behaviour probes ----------
print("\n--- probes of the fix's new behaviours ---")
sparse = mk('AAAA------------', '----CCCC--------', '--------GGGG----', '------------TTTT')     # 4 fragments, every column 25% occupied
cols_ = [CP.column_conservation(sparse, i) for i in range(16)]
check('C1: every column of a 4-fragment alignment is below min_occupancy 0.5 -> all NaN (was 100% before the fix)', all(math.isnan(x) for x in cols_), f'{sum(math.isnan(x) for x in cols_)}/16 NaN')
os.chdir(W)
open('alignment.fasta', 'w').write(''.join(f'>s{i}\n{r.seq}\n' for i, r in enumerate(sparse)))
ns2, log2 = skill_blocks.run_all(verbose=False)
b4 = [l for l in log2 if l[0] == 4][0]
print('   SKILL.md block 4 (average_conservation) on the all-NaN alignment:', b4[2])
try:
    ns2['average_conservation'](sparse); r = 'returned'
except Exception as e:
    r = f'{type(e).__name__}: {e}'
zd = 'ZeroDivisionError' in r
print('   direct call:', r)
p = subprocess.run([sys.executable, '-B', 'conservation_profile.py', os.path.join(W, 'alignment.fasta')], cwd=B.EX, capture_output=True, text=True, encoding='utf-8')
print('   conservation_profile.py on the same file: rc', p.returncode, '|', [l for l in p.stdout.splitlines() if 'Average' in l], '| stderr:', p.stderr.strip()[:160])
check('C2: SKILL.md average_conservation does not crash when no column reaches min_occupancy', not zd, r)
pr = CP.conservation_profile(sparse); check('C3: conservation_profile returns NaN (not crash) when all columns are NaN', all(math.isnan(x) for x in pr), '')
# is_nucleotide auto-detection edge: IUPAC-rich DNA [synthetic spice of real HBB alignment]
rng = np.random.default_rng(20260920)
dna = B.read_fasta(os.path.join(HERE, 'data', 'hbb6_mafft_upper.fa'))
def spice(s, frac):
    return ''.join(ch if ch == '-' or rng.random() > frac else str(rng.choice(list('RYSWKM'))) for ch in s)
for frac in (0.05, 0.12):
    a = mk(*[spice(s, frac) for _, s in dna]); nuc = msa_utils.is_nucleotide(a)
    bgd, bgL = msa_utils.pick_background(a)
    icx = max(EA.information_content(a[:, i], bgd) for i in range(a.get_alignment_length()))
    e = io.StringIO()
    with contextlib.redirect_stderr(e):
        msa_utils.check_alphabet(a, bgd)
    print(f'   DNA with {frac*100:.0f}% IUPAC R/Y/S/W/K/M [synthetic]: is_nucleotide={nuc}, background "{bgL}", IC max {icx:.2f}; check_alphabet: {e.getvalue().strip()[:100]!r}')
    RES[f'C4 IUPAC {frac}'] = (nuc, bgL)
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b07.json'), 'w'), indent=1)
os.chdir(HERE); shutil.rmtree(W, ignore_errors=True)
print('\nSUMMARY', sum(1 for k, v in RES.items() if k[:2] != 'C4' and v[0]), 'of', sum(1 for k in RES if k[:2] != 'C4'), 'checks PASS')
