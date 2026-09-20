"""INPUT 1 (canonical, REAL data): Pfam PF00042 seed (73 x 141, from InterPro), Skill code vs independent reference.
Prompt: "Here is the Pfam globin seed alignment. Give me the pairwise identity matrix, conservation per column,
Shannon entropy / information content, gap statistics, and the sum-of-pairs score."
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python s04_input1_seed.py"""
import os, sys, shutil, subprocess, itertools, json, math, io, contextlib, time
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
from Bio.Align import substitution_matrices
from Bio.Phylo.TreeConstruction import DistanceCalculator

FASTA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'seed_norm.fasta')
TAG = sys.argv[2] if len(sys.argv) > 2 else 'in1'
WORK = os.path.join(HERE, 'work_' + TAG)
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
shutil.copy(FASTA, os.path.join(WORK, 'alignment.fasta'))
for f in os.listdir(os.path.join(HERE, 'skill', 'examples')):
    shutil.copy(os.path.join(HERE, 'skill', 'examples', f), WORK)
os.chdir(WORK)
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail)
    print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

aln = AlignIO.read('alignment.fasta', 'fasta')
rows = ref.norm_rows([str(r.seq) for r in aln])
N, L = len(aln), aln.get_alignment_length()
print('alignment', N, 'x', L, 'file', FASTA)

# ---- A. run all 8 shipped examples as-is (copy) and record output size / exit ----
print('\n=== A. shipped examples/*.py (from a copy, alignment.fasta in cwd) ===')
EX = {}
for f in sorted(os.listdir(os.path.join(HERE, 'skill', 'examples'))):
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', f], capture_output=True, text=True, encoding='utf-8', timeout=600)
    EX[f] = dict(rc=p.returncode, nlines=len(p.stdout.splitlines()), err=p.stderr.strip()[-300:], secs=round(time.time() - t0, 1), out=p.stdout)
    print(f'{f:<28} rc={p.returncode} stdout_lines={EX[f]["nlines"]} secs={EX[f]["secs"]} stderr={EX[f]["err"][:120]!r}')
    open(f'out_{f}.txt', 'w', encoding='utf-8').write(p.stdout)

# ---- B. run SKILL.md python blocks verbatim ----
print('\n=== B. SKILL.md python blocks, verbatim ===')
import skill_blocks
ns, log = skill_blocks.run_all()
for i, first, st, out in log:
    if st == 'OK' and out.strip():
        print(f'  -- block {i} stdout: ' + out.strip().splitlines()[0][:100] + ('  (+%d lines)' % (len(out.strip().splitlines()) - 1)))

# ---- C. numeric checks vs independent reference ----
print('\n=== C. numeric checks vs independent reference ===')
import identity_matrix as IM, entropy_analysis as EA, capra_singh_jsd as CS, pssm as PS
import kimura_protein_distance as KP, substitution_counts as SC

# C1 identity matrix (Skill example = "any-nongap denominator") vs naive + vs Bio.Phylo identity distance (=1-PID2)
M = IM.identity_matrix_vectorized(aln)
i, j = 3, 40
naive = ns['pairwise_identity'](str(aln[i].seq), str(aln[j].seq), 'pid1')
check('C1a vectorized matrix == pairwise_identity(pid1)', abs(M[i, j] - naive) < 1e-12, f'{M[i,j]:.4f} vs {naive:.4f}')
dc = DistanceCalculator('identity').get_distance(AlignIO.read('alignment.fasta', 'fasta'))
maxd = 0; pid1_gap = []; d_pid1 = []
for a, b in itertools.combinations(range(N), 2):
    r = ref.pid_ref(rows[a], rows[b])
    # Skill pid2 vs 1 - Bio.Phylo identity distance
    s2 = ns['pairwise_identity'](str(aln[a].seq), str(aln[b].seq), 'pid2')
    # Bio.Phylo 'identity' = identities / ALIGNMENT LENGTH (a 5th denominator), so compare NUMERATORS: matches
    skill_matches = round(s2 * r['aligned'])
    # NOTE probed in s05: Bio.Phylo 'identity' (scoring_matrix=None) does NOT skip gaps, so '-'=='-' counts as a match:
    # it is not a valid second implementation. Use a numpy elementwise count instead.
    A_ = np.array(list(rows[a])); B_ = np.array(list(rows[b]))
    np_matches = int(((A_ == B_) & (A_ != '-')).sum())
    maxd = max(maxd, abs(skill_matches - np_matches))
    for m in ('pid3', 'pid4'):
        sv = ns['pairwise_identity'](str(aln[a].seq), str(aln[b].seq), m)
        assert abs(sv - r[m.upper()]) < 1e-9, (m, a, b, sv, r[m.upper()])
    d_pid1.append(M[a, b] - r['PID1'])
check('C1b Skill identical-residue count == numpy elementwise count (all 2628 pairs)', maxd == 0, f'max|diff| in matches={maxd}')
check('C1c Skill PID3, PID4 == independent definitional (all pairs)', True, 'asserted inside loop')
d_pid1 = np.array(d_pid1)
check('C1d Skill PID1 == Doolittle/Raghava-Barton PID1 (aligned+INTERNAL gaps)', np.abs(d_pid1).max() < 1e-9,
      f'mean diff {100*d_pid1.mean():+.2f} pts, max |diff| {100*np.abs(d_pid1).max():.2f} pts (Skill lower: terminal-overhang columns counted)')
avg_sk = (M.sum() - N) / (N * (N - 1))
avg_ref = np.mean([ref.pid_ref(rows[a], rows[b])['PID4'] for a, b in itertools.combinations(range(N), 2)])
print(f'   avg pairwise identity: Skill example (PID1-style) {avg_sk*100:.1f}%  vs reference PID4 {avg_ref*100:.1f}%  (SKILL text recommends PID4)')

# C2 conservation
cols = [''.join(c) for c in zip(*rows)]
cons_sk = np.array([ns['column_conservation'](aln, k) for k in range(L)])
cons_rf = np.array([ref.conservation_ref(c) for c in cols])
check('C2a per-column conservation == reference', np.abs(cons_sk - cons_rf).max() < 1e-12, f'max diff {np.abs(cons_sk-cons_rf).max():.1e}')
gapfrac = np.array([c.count('-') / N for c in cols])
sparse = gapfrac > 0.5
print(f'   columns with >50% gaps: {sparse.sum()}; their mean Skill conservation {cons_sk[sparse].mean()*100:.1f}% (n residues per col: {[N-c.count("-") for c in np.array(cols)[sparse][:6]]})')
sparse_full = [k for k in range(L) if gapfrac[k] > 0.5 and cons_sk[k] == 1.0]
avg_all = cons_sk.mean(); avg_dense = cons_sk[~sparse].mean()
print(f'   average conservation all columns {avg_all*100:.1f}% ; excluding >50%-gap columns {avg_dense*100:.1f}% ; columns >50% gapped but reported 100% conserved: {len(sparse_full)}')
prof = ns['conservation_profile'](aln, window=10)
k = 60
exp = np.mean([cons_rf[j] for j in range(max(0, k - 5), min(L, k + 5))])
check('C2b conservation_profile == mean over cols [i-5,i+4] (window=10, half-open, NOT centred)', abs(prof[k] - exp) < 1e-9, f'skill {prof[k]:.4f}; [i-5,i+4] = {exp:.4f}; centred [i-5,i+5] = {np.mean(cons_rf[k-5:k+6]):.4f}')

# C3 entropy / IC
ent_sk = np.array([EA.shannon_entropy(c) for c in cols]); ent_rf = np.array([ref.entropy_ref(c) for c in cols])
check('C3a Shannon entropy == scipy.stats.entropy(base 2)', np.abs(ent_sk - ent_rf).max() < 1e-9, f'max diff {np.abs(ent_sk-ent_rf).max():.1e}')
ic_sk = np.array([EA.information_content(c, EA.ROBINSON_BACKGROUND) for c in cols])
ic_true_bg = np.array([ref.ic_ref(c, ref.ROB_TRUE)[0] for c in cols])
ic_same_bg = np.array([ref.ic_ref(c, EA.ROBINSON_BACKGROUND)[0] for c in cols])
dropped = sum(ref.ic_ref(c, EA.ROBINSON_BACKGROUND)[1] for c in cols)
print(f'   non-20-letter residues in seed (B/Z): {dropped}')
sk_bg_sum = sum(EA.ROBINSON_BACKGROUND.values())
print(f'   sum(Skill ROBINSON_BACKGROUND)={sk_bg_sum:.4f}; max |Skill bg - published Robinson (NCBI)| = {max(abs(EA.ROBINSON_BACKGROUND[a]-ref.ROB_TRUE[a]) for a in ref.AA20):.4f} (N .0427 vs .04487, K .0596 vs .05744)')
print(f'   IC max |Skill - KL with same bg (scipy-free ref, B/Z dropped)| = {np.abs(ic_sk - ic_same_bg).max():.3f} bits; IC(Skill bg) vs IC(published Robinson bg): max diff {np.abs(ic_sk-ic_true_bg).max():.3f}, Spearman-ish rank corr {np.corrcoef(np.argsort(np.argsort(ic_sk)), np.argsort(np.argsort(ic_true_bg)))[0,1]:.4f}')
bz_cols = [k for k in range(L) if any(x in 'BZX' for x in cols[k])]
print(f'   columns containing B/Z: {bz_cols}; Skill IC there {[round(ic_sk[k],2) for k in bz_cols]} vs ref {[round(ic_same_bg[k],2) for k in bz_cols]}')
check('C3b Skill IC == reference KL (same bg)', np.abs(ic_sk - ic_same_bg).max() < 1e-3, f'max diff {np.abs(ic_sk-ic_same_bg).max():.3f} bits')

# C4 JSD (Capra-Singh) raw + smoothing
raw_sk = []
for c in cols:
    col_nog = c.replace('-', '')
    if not col_nog: raw_sk.append(0.0); continue
    from collections import Counter
    cnt = Counter(col_nog); tot = len(col_nog)
    raw_sk.append(CS.js_divergence({k2: v / tot for k2, v in cnt.items()}, CS.ROBINSON_BACKGROUND) * (1 - c.count('-') / N))
jsd_rf = np.array([ref.jsd_ref(c, CS.ROBINSON_BACKGROUND) * (1 - c.count('-') / N) for c in cols])
# the seed has B/Z: scipy ref drops them & renormalises, Skill keeps them in p -> expect tiny diffs only there
print(f'   raw JSD max |Skill - scipy ref| = {np.abs(np.array(raw_sk)-jsd_rf).max():.4f}')
sm = CS.capra_singh_score(aln)
ref_sm = []
for k in range(L):
    nb = list(jsd_rf[max(0, k - 3):k]) + list(jsd_rf[k + 1:k + 4])
    ref_sm.append(0.5 * jsd_rf[k] + 0.5 * np.mean(nb))
check('C4 capra_singh_score == scipy-JSD + own smoothing', np.abs(np.array(sm) - np.array(ref_sm)).max() < 5e-3, f'max diff {np.abs(np.array(sm)-np.array(ref_sm)).max():.4f}')
top_sk = sorted(range(L), key=lambda k: -sm[k])[:10]
print('   top-10 JSD columns (Skill):', top_sk)
# gappy-column artifacts: Capra-Singh reference impl masks columns with >=30% gaps; Skill only down-weights
print('   top-10 cols gap fraction:', [round(gapfrac[k], 2) for k in top_sk])

# C5 gap stats
gs = EX['gap_statistics.py']['out']
tg = sum(c.count('-') for c in cols)
check('C5 gap_statistics total gaps', f'Total gaps: {tg}' in gs, f'ref {tg} ({tg/(N*L)*100:.1f}%)')
check('C5b gap-free column count', f'Gap-free columns: {sum(1 for c in cols if "-" not in c)} ' in gs, '')

# C6 SP scores
BL = substitution_matrices.load('BLOSUM62')
sp_s = ns['sum_of_pairs'](aln); sp_r, skipped = ref.sp_ref(rows, BL)
check('C6a sum_of_pairs (BLOSUM62) == reference', abs(sp_s - sp_r) < 1e-9, f'{sp_s} vs {sp_r}; pairs skipped (B/Z absent in matrix? ) = {skipped}')
asc = ns['alignment_score'](aln); asc_r0 = ref.sp_simple_ref(rows, gapgap=0); asc_r2 = ref.sp_simple_ref(rows, gapgap=-2)
check('C6b alignment_score == textbook SP (gap/gap pairs = 0)', asc == asc_r0, f'Skill {asc}; textbook(gapgap=0) {asc_r0}; if gap/gap scored as gap (-2): {asc_r2}')

# C7 PSSM, Kimura, substitution counts
ps = PS.pssm_with_pseudocounts(aln); psr = ref.pssm_ref(rows, PS.ROBINSON_BACKGROUND)
dmax = max(abs(ps[k][r] - psr[k][r]) for k in range(L) for r in PS.ROBINSON_BACKGROUND)
check('C7a PSSM == reference', dmax < 1e-9, f'max diff {dmax:.1e}')
kd = [KP.kimura_protein_distance(str(aln[a].seq), str(aln[b].seq)) for a, b in itertools.combinations(range(N), 2)]
kr = [ref.kimura_ref(rows[a], rows[b]) for a, b in itertools.combinations(range(N), 2)]
fin = [(x, y) for x, y in zip(kd, kr) if np.isfinite(x) and np.isfinite(y)]
mism = sum(1 for x, y in zip(kd, kr) if (np.isinf(x) != np.isinf(y)))
check('C7b Kimura == reference on finite pairs', max(abs(x - y) for x, y in fin) < 1e-9, f'{len(fin)} finite pairs; inf-status mismatches {mism}; saturated pairs (Skill) {sum(np.isinf(x) for x in kd)}')
subs = SC.substitution_counts(aln)
brute = 0
for c in cols:
    ch = [x for x in c if x != '-']
    brute += sum(1 for x, y in itertools.combinations(ch, 2) if x != y)
check('C7c substitution_counts total == brute force', sum(subs.values()) == brute, f'{sum(subs.values())} vs {brute}')
print('   substitution_counts.py Ti/Tv line on PROTEIN input:', [l for l in EX['substitution_counts.py']['out'].splitlines() if 'Ti/Tv' in l or 'Transitions' in l or 'Transversions' in l])

json.dump({k: v for k, v in RES.items()}, open(f'../results_{TAG}.json', 'w'), indent=1)
json.dump({k: dict(rc=v['rc'], nlines=v['nlines'], err=v['err']) for k, v in EX.items()}, open(f'../examples_{TAG}.json', 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
