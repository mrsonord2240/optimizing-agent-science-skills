"""INPUT 1 (canonical, REAL data): Pfam PF00042 globin seed (73 x 141, InterPro), fixed Skill vs independent references.
Prompt: "Here is the Pfam globin seed alignment. Give me the pairwise identity matrix, conservation per column,
Shannon entropy / information content, gap statistics, and the sum-of-pairs score."
Runs on BOTH seed_norm.fasta ('-' gaps) and seed_dot.fasta ('.' gaps, as Pfam/hmmalign write them): the fix
claims they give identical numbers. SKILL.md python blocks run VERBATIM after the normalising import.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b01_input1_seed.py"""
import os, sys, shutil, itertools, json, math, subprocess, time
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
from scipy.special import rel_entr
from Bio import AlignIO
from Bio.Align import substitution_matrices

RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail)
    print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

WORK = os.path.join(HERE, 'work_b01')
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
for f in os.listdir(os.path.join(HERE, 'skill', 'examples')):
    if f.endswith('.py'):
        shutil.copy(os.path.join(HERE, 'skill', 'examples', f), WORK)
shutil.copytree(os.path.join(HERE, 'skill', 'examples', 'data'), os.path.join(WORK, 'data'))
os.chdir(WORK); sys.path.insert(0, WORK)
import msa_utils, identity_matrix as IM, entropy_analysis as EA, capra_singh_jsd as CS, pssm as PS
import kimura_protein_distance as KP, substitution_counts as SC, conservation_profile as CP
import skill_blocks  # from run/

variants = {}
for tag, fn in [('dash', 'seed_norm.fasta'), ('dot', 'seed_dot.fasta')]:
    variants[tag] = os.path.join(HERE, 'data', fn)
print('dot file has "." gaps:', open(variants['dot']).read().count('.'), ' dash file has "." gaps:', open(variants['dash']).read().count('.'))

results = {}
for tag, path in variants.items():
    print(f'\n################ variant {tag}: {path}')
    shutil.copy(path, os.path.join(WORK, 'alignment.fasta'))
    ns, log = skill_blocks.run_all(verbose=False)
    for i, first, st, out in log:
        print(f'[block {i:2d}] {st:<28} {first[:50]:<50} ' + (out.strip().splitlines()[0][:70] if st == 'OK' and out.strip() else ''))
    aln = ns['alignment']                       # what the SKILL.md normalising import produced
    N, L = len(aln), aln.get_alignment_length()
    rows = [str(r.seq) for r in aln]
    raw_rows = ref.norm_rows([str(r.seq) for r in AlignIO.read(path, 'fasta')])   # independent normalisation
    check(f'{tag}: SKILL.md normalize_alignment == independent normalisation', rows == raw_rows, f'{N}x{L}; alphabet {sorted(set("".join(rows)))}')
    results[tag] = {}

    # --- identity (all four methods) vs two independent PID1 definitions and definitional PID2-4
    cols = [''.join(c) for c in zip(*rows)]
    Ms = {m: IM.identity_matrix_vectorized(aln, m) for m in IM.METHODS}
    dif = {m: 0.0 for m in IM.METHODS}; d_span_vs_perseq = 0
    A = np.array([list(r) for r in rows])
    for a, b in itertools.combinations(range(N), 2):
        r = ref.pid_ref(rows[a], rows[b])
        both = (A[a] != '-') & (A[b] != '-')
        idx = np.where(both)[0]
        span = (A[a, idx[0]:idx[-1] + 1] != '-') | (A[b, idx[0]:idx[-1] + 1] != '-')
        pid1_span = (A[a] == A[b])[both].sum() / span.sum()          # numpy re-derivation of the span definition
        d_span_vs_perseq += abs(pid1_span - r['PID1']) > 1e-12
        for m, key in zip(IM.METHODS, ['PID1', 'PID2', 'PID3', 'PID4']):
            dif[m] = max(dif[m], abs(Ms[m][a, b] - (pid1_span if m == 'pid1' else r[key])),
                         abs(IM.pairwise_identity(rows[a], rows[b], m) - (pid1_span if m == 'pid1' else r[key])))
    check(f'{tag}: identity PID1-4 (vectorized AND per-pair function) == independent, all 2628 pairs', max(dif.values()) < 1e-12, f'max diff {dif}')
    check(f'{tag}: PID1 span definition == per-sequence-internal-gap definition on this alignment', d_span_vs_perseq == 0, f'{d_span_vs_perseq} of 2628 pairs differ')
    avg, undef = IM.average_identity(Ms['pid1'])
    avg4, _ = IM.average_identity(Ms['pid4'])
    print(f'   mean PID1 {avg*100:.2f}%  mean PID4 {avg4*100:.2f}%  undefined {undef}')
    results[tag]['mean_pid1'] = avg
    # --- conservation
    cons0 = np.array([CP.column_conservation(aln, k, min_occupancy=0.0) for k in range(L)])
    cons_rf = np.array([ref.conservation_ref(c) for c in cols])
    occ = np.array([1 - c.count('-') / N for c in cols])
    check(f'{tag}: column_conservation(min_occupancy=0) == reference on occupied columns', np.nanmax(np.abs(np.where(occ > 0, cons0 - cons_rf, 0))) < 1e-12, '')
    cons5 = np.array([CP.column_conservation(aln, k) for k in range(L)])
    check(f'{tag}: default min_occupancy=0.5 -> NaN exactly where residues/N < 0.5', np.array_equal(np.isnan(cons5), occ < 0.5), f'{np.isnan(cons5).sum()} NaN columns')
    n_used = int((~np.isnan(cons5)).sum()); mean5 = np.nanmean(cons5)
    avg_blk, n_blk = ns['average_conservation'](aln)
    check(f'{tag}: SKILL.md average_conservation == mean of reference over occupancy>=0.5 columns', abs(avg_blk - cons_rf[occ >= 0.5].mean()) < 1e-12 and n_blk == (occ >= 0.5).sum(),
          f'{avg_blk*100:.2f}% over {n_blk} columns (SKILL text: 34.3%; old all-columns mean {ns["average_conservation"](aln, min_occupancy=0.0)[0]*100:.2f}%)')
    prof = ns['conservation_profile'](aln, window=10)
    k = 60; exp = np.nanmean(cons5[k - 5:k + 6])
    check(f'{tag}: conservation_profile centred window i-5..i+5 (independent numpy)', abs(prof[k] - exp) < 1e-12, f'{prof[k]:.4f} vs {exp:.4f}')
    # --- entropy / IC with an independent KL (scipy.special.rel_entr), B/Z dropped and renormalised
    ent_sk = np.array([EA.shannon_entropy(c) for c in cols]); ent_rf = np.array([ref.entropy_ref(c) for c in cols])
    check(f'{tag}: Shannon entropy == scipy entropy', np.abs(ent_sk - ent_rf).max() < 1e-12, '')
    def ic_scipy(col, bg):
        c = [x for x in col if x in bg]
        if not c: return 0.0
        keys = sorted(bg); cnt = Counter(c); p = np.array([cnt[k] for k in keys], float); p /= p.sum()
        q = np.array([bg[k] for k in keys])
        return float(rel_entr(p, q).sum() / math.log(2))
    ic_sk = np.array([EA.information_content(c, msa_utils.ROBINSON_BACKGROUND) for c in cols])
    ic_ref = np.array([ic_scipy(c, ref.ROB_TRUE) for c in cols])
    ic_blk = np.array([ns['information_content'](c, ns['ROBINSON_BACKGROUND']) for c in cols])
    check(f'{tag}: information_content (example AND SKILL.md block) == scipy rel_entr KL with published Robinson', max(np.abs(ic_sk - ic_ref).max(), np.abs(ic_blk - ic_ref).max()) < 1e-12, f'max diff {np.abs(ic_sk-ic_ref).max():.1e}; max IC {ic_sk.max():.3f} bits (bound 6.23)')
    bz = sum(1 for c in cols for x in c if x in 'BZX')
    print(f'   B/Z/X residues dropped by IC: {bz}; bg sum {sum(msa_utils.ROBINSON_BACKGROUND.values()):.5f}; Skill bg == published Robinson: {msa_utils.ROBINSON_BACKGROUND == ref.ROB_TRUE}')
    # --- JSD
    jsd_rf = np.array([ref.jsd_ref(c, msa_utils.ROBINSON_BACKGROUND) * occ[k] for k, c in enumerate(cols)])
    sm = CS.capra_singh_score(aln)
    ref_sm = []
    for k in range(L):
        nb = list(jsd_rf[max(0, k - 3):k]) + list(jsd_rf[k + 1:k + 4])
        ref_sm.append(0.5 * jsd_rf[k] + 0.5 * np.mean(nb))
    check(f'{tag}: capra_singh_score == scipy JSD x occupancy + own smoothing', np.abs(np.array(sm) - np.array(ref_sm)).max() < 1e-9, f'max diff {np.abs(np.array(sm)-np.array(ref_sm)).max():.1e}')
    # --- gaps
    gs = subprocess.run([sys.executable, '-B', 'gap_statistics.py', 'alignment.fasta'], capture_output=True, text=True, encoding='utf-8').stdout
    tg = sum(c.count('-') for c in cols)
    check(f'{tag}: gap_statistics.py total gaps and gap-free columns', f'Total gaps: {tg}' in gs and f'Gap-free columns: {sum(1 for c in cols if "-" not in c)} ' in gs, f'total {tg} ({tg/(N*L)*100:.1f}%)')
    # --- SP scores
    BL = substitution_matrices.load('BLOSUM62')
    import io, contextlib
    eb = io.StringIO()
    with contextlib.redirect_stderr(eb):
        sp_s = ns['sum_of_pairs'](aln)
    sp_r, skipped = ref.sp_ref(rows, BL)
    check(f'{tag}: sum_of_pairs (BLOSUM62) == reference', abs(sp_s - sp_r) < 1e-9, f'{sp_s} vs {sp_r}; skipped pairs (ref) {skipped}; warning text {eb.getvalue().strip()!r}')
    # independent count-based SP with gap/gap = 0 (column composition; no pair loop)
    asc = ns['alignment_score'](aln)
    tot = 0
    for c in cols:
        cnt = Counter(c); g = cnt.get('-', 0); res_ = [(k2, v) for k2, v in cnt.items() if k2 != '-']
        nres = sum(v for _, v in res_)
        same = sum(v * (v - 1) // 2 for _, v in res_)
        tot += same * 1 + (nres * (nres - 1) // 2 - same) * -1 + g * nres * -2      # gap/gap pairs contribute 0
    check(f'{tag}: alignment_score == count-based textbook SP (gap/gap = 0)', asc == tot == ref.sp_simple_ref(rows, gapgap=0), f'{asc} vs {tot}; if gap/gap were charged -2: {ref.sp_simple_ref(rows, gapgap=-2)}')
    # --- PSSM / Kimura / substitution counts
    ps = PS.pssm_with_pseudocounts(aln); psr = ref.pssm_ref(rows, msa_utils.ROBINSON_BACKGROUND)
    dmax = max(abs(ps[k][r] - psr[k][r]) for k in range(L) for r in msa_utils.ROBINSON_BACKGROUND)
    print(f'   PSSM max diff vs reference (reference counts B/Z in n, Skill drops them): {dmax:.4f}')
    # reference variant that drops B/Z from n as the fixed docstring states
    def pssm_drop(col, bg, pc=1.0):
        c = [x for x in col if x in bg]; n = len(c)
        return {r: math.log2(((c.count(r) + pc * bg[r]) / (n + pc)) / bg[r]) for r in bg}
    d2 = max(abs(ps[k][r] - pssm_drop(cols[k], msa_utils.ROBINSON_BACKGROUND)[r]) for k in range(L) for r in msa_utils.ROBINSON_BACKGROUND)
    check(f'{tag}: PSSM == independent (letters outside background dropped from n)', d2 < 1e-12, f'max diff {d2:.1e}')
    kd = [KP.kimura_protein_distance(rows[a], rows[b]) for a, b in itertools.combinations(range(N), 2)]
    kr = [ref.kimura_ref(rows[a], rows[b]) for a, b in itertools.combinations(range(N), 2)]
    fin = [(x, y) for x, y in zip(kd, kr) if np.isfinite(x) and np.isfinite(y)]
    check(f'{tag}: Kimura == reference on finite pairs', max(abs(x - y) for x, y in fin) < 1e-9, f'{len(fin)} finite, saturated {sum(np.isinf(x) for x in kd)}; any -0.0 printed: {any(str(x)=="-0.0" for x in kd)}')
    subs = SC.substitution_counts(aln)
    brute = sum(sum(1 for x, y in itertools.combinations([z for z in c if z != '-'], 2) if x != y) for c in cols)
    check(f'{tag}: substitution_counts total == brute force', sum(subs.values()) == brute, f'{brute}')
    out = subprocess.run([sys.executable, '-B', 'substitution_counts.py', 'alignment.fasta'], capture_output=True, text=True, encoding='utf-8').stdout
    check(f'{tag}: substitution_counts.py on PROTEIN prints no Ti/Tv', 'Ti/Tv ratio' not in out and 'Transitions' not in out and 'not reported' in out, out.strip().splitlines()[-1])
    # DistanceCalculator block (SKILL.md block 16) now runs on the normalised seed
    blk16 = [l for l in log if l[0] == 16][0]
    check(f'{tag}: SKILL.md DistanceCalculator block runs on normalised seed', blk16[2] == 'OK', blk16[2])
    results[tag].update(mean5=float(mean5), n_used=n_used, sp=float(sp_s), asc=int(asc), ic_max=float(ic_sk.max()))
check('dash vs dot variants give identical statistics', results['dash'] == results['dot'], json.dumps(results))

# examples run on the dotted file through msa_utils (the shipped CLI path: argv[1])
for f, pat in [('identity_matrix.py', 'Average pairwise identity'), ('entropy_analysis.py', 'Average entropy'), ('conservation_profile.py', 'Average conservation')]:
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', f, variants['dot']], capture_output=True, text=True, encoding='utf-8')
    line = [l for l in p.stdout.splitlines() if pat in l]
    check(f'CLI {f} <seed_dot.fasta> rc 0 and prints "{pat}"', p.returncode == 0 and bool(line), f'{line} {round(time.time()-t0,1)}s stderr={p.stderr.strip()[:100]!r}')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b01.json'), 'w'), indent=1)
os.chdir(HERE); shutil.rmtree(WORK, ignore_errors=True)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
