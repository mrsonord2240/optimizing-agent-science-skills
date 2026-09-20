"""Reusable check battery: the fixed Skill (imported from run/skill/examples, never modified) against independent references.
Every check asserts on numeric content, never on exit codes. Used by b02, b04, b06 (new inputs) and b07."""
import os, sys, math, itertools, subprocess, io, contextlib
from collections import Counter
import numpy as np
from scipy.special import rel_entr
from scipy.stats import entropy as sp_entropy
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, 'skill', 'examples')
sys.path.insert(0, EX); sys.path.insert(0, HERE)
import ref, msa_utils
import identity_matrix as IM, entropy_analysis as EA, capra_singh_jsd as CS, pssm as PS
import kimura_protein_distance as KP, substitution_counts as SC, conservation_profile as CP
from Bio.Align import substitution_matrices


def read_fasta(path):
    recs, cur = [], None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('>'):
            cur = [line[1:].split()[0], []]; recs.append(cur)
        elif cur is not None and line.strip():
            cur[1].append(line.strip())
    return [(i, ''.join(s)) for i, s in recs]


def read_stockholm(path):
    d = {}
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#') or line.startswith('//'):
            continue
        name, seq = line.split()
        d[name] = d.get(name, '') + seq
    return list(d.items())


def independent_rows(path, fmt):
    recs = read_stockholm(path) if fmt == 'stockholm' else read_fasta(path)
    return [ref.norm_rows([s])[0] for _, s in recs]


def pid_span_ref(a, b):
    """PID1..4 from numpy alone: PID1 denominator = span between first and last both-residue column, columns with a residue in either row."""
    A = np.array(list(a)); B = np.array(list(b))
    ra, rb = A != '-', B != '-'
    both = ra & rb
    if not ra.any() or not rb.any():
        return [float('nan')] * 4
    idx = np.where(both)[0]
    ident = int(((A == B) & both).sum())
    la, lb = int(ra.sum()), int(rb.sum())
    p1 = ident / int((ra | rb)[idx[0]:idx[-1] + 1].sum()) if idx.size else float('nan')
    p2 = ident / int(both.sum()) if idx.size else float('nan')
    return [p1, p2, ident / min(la, lb), ident / ((la + lb) / 2)]


def titv_ref(rows):
    ti = tv = amb = 0
    for col in zip(*rows):
        c = [x for x in col if x != '-']
        for x, y in itertools.combinations(c, 2):
            if x == y:
                continue
            if x in 'ACGT' and y in 'ACGT':
                if {x, y} in ({'A', 'G'}, {'C', 'T'}):
                    ti += 1
                else:
                    tv += 1
            else:
                amb += 1
    return ti, tv, amb


def run_battery(path, fmt, kind, tag, max_pairs=3000, check=None, out_cli=True, rna=False):
    """kind = 'protein' | 'dna'. Returns dict of results; `check(name, ok, detail)` records each one."""
    from Bio import AlignIO
    aln = msa_utils.load_alignment(path, fmt)
    rows = [str(r.seq) for r in aln]
    N, L = len(aln), aln.get_alignment_length()
    bg = msa_utils.ROBINSON_BACKGROUND if kind == 'protein' else msa_utils.DNA_UNIFORM
    exp_rows = independent_rows(path, fmt)
    if rna:
        exp_rows = [r.replace('U', 'T') for r in exp_rows]
    check(f'{tag}: load_alignment == independent normalisation (own parser)', rows == exp_rows, f'{N}x{L}; alphabet {"".join(sorted(set("".join(rows))))}')
    check(f'{tag}: is_nucleotide() == {kind == "dna"}', msa_utils.is_nucleotide(aln) == (kind == 'dna'), f'pick_background -> {msa_utils.pick_background(aln)[1]}')
    cols = [''.join(c) for c in zip(*rows)]
    # identity
    rng = np.random.default_rng(20260920)
    pairs = list(itertools.combinations(range(N), 2))
    if len(pairs) > max_pairs:
        pairs = [pairs[k] for k in rng.choice(len(pairs), max_pairs, replace=False)]
    Ms = {m: IM.identity_matrix_vectorized(aln, m) for m in IM.METHODS}
    worst = 0.0
    for a, b in pairs:
        r = pid_span_ref(rows[a], rows[b])
        for k, m in enumerate(IM.METHODS):
            for got in (Ms[m][a, b], IM.pairwise_identity(rows[a], rows[b], m)):
                if not (math.isnan(got) and math.isnan(r[k])):
                    worst = max(worst, abs(got - r[k]))
    check(f'{tag}: identity PID1-4 (vectorized + function) == numpy reference on {len(pairs)} pairs', worst < 1e-12, f'max diff {worst:.1e}')
    avg1, und = IM.average_identity(Ms['pid1']); avg4, _ = IM.average_identity(Ms['pid4'])
    # conservation
    occ = np.array([1 - c.count('-') / N for c in cols])
    cons0 = np.array([CP.column_conservation(aln, k, min_occupancy=0.0) for k in range(L)])
    cons5 = np.array([CP.column_conservation(aln, k) for k in range(L)])
    cref = np.array([ref.conservation_ref(c) for c in cols])
    check(f'{tag}: conservation == reference (occupied columns); NaN exactly where occupancy < 0.5', np.abs(np.where(occ > 0, cons0 - cref, 0)).max() < 1e-12 and np.array_equal(np.isnan(cons5), occ < 0.5), f'{int(np.isnan(cons5).sum())} NaN columns of {L}; mean {np.nanmean(cons5)*100 if (~np.isnan(cons5)).any() else float("nan"):.1f}% (all-occupied mean {cref[occ>0].mean()*100:.1f}%)')
    # entropy / IC
    ent = np.array([EA.shannon_entropy(c) for c in cols]); entr = np.array([ref.entropy_ref(c) for c in cols])
    check(f'{tag}: Shannon entropy == scipy', np.abs(ent - entr).max() < 1e-12, '')
    def ic_scipy(col):
        c = [x for x in col if x in bg]
        if not c:
            return 0.0
        keys = sorted(bg); cnt = Counter(c); p = np.array([cnt[k] for k in keys], float); p /= p.sum()
        return float(rel_entr(p, np.array([bg[k] for k in keys])).sum() / math.log(2))
    ic = np.array([EA.information_content(c, bg) for c in cols]); icr = np.array([ic_scipy(c) for c in cols])
    bound = -math.log2(min(bg.values()))
    check(f'{tag}: information_content == scipy rel_entr KL and <= {bound:.2f} bits', np.abs(ic - icr).max() < 1e-12 and ic.max() <= bound + 1e-9, f'max {ic.max():.3f}; letters outside background: {sum(1 for c in cols for x in c if x != "-" and x not in bg)}')
    # PSSM
    ps = PS.pssm_with_pseudocounts(aln, bg)
    def pdrop(col):
        c = [x for x in col if x in bg]; n = len(c)
        return {r: math.log2(((c.count(r) + bg[r]) / (n + 1.0)) / bg[r]) for r in bg}
    d = max(abs(ps[k][r] - pdrop(cols[k])[r]) for k in range(L) for r in bg)
    check(f'{tag}: PSSM == independent (default background picked by alphabet too)', d < 1e-12 and all(abs(PS.pssm_with_pseudocounts(aln)[k][r] - ps[k][r]) < 1e-15 for k in range(min(L, 5)) for r in bg), f'max diff {d:.1e}')
    out = {'N': N, 'L': L, 'avg_pid1': avg1, 'avg_pid4': avg4, 'ic_max': float(ic.max()), 'cons_mean': float(np.nanmean(cons5)) if (~np.isnan(cons5)).any() else float('nan')}
    # alignment_score (SKILL.md block semantics, gap/gap 0) vs count-based
    tot = 0
    for c in cols:
        cnt = Counter(c); g = cnt.get('-', 0); rs = [(k2, v) for k2, v in cnt.items() if k2 != '-']
        nres = sum(v for _, v in rs); same = sum(v * (v - 1) // 2 for _, v in rs)
        tot += same - (nres * (nres - 1) // 2 - same) - 2 * g * nres
    out['simple_sp_ref'] = tot
    if kind == 'protein':
        jsd = np.array([ref.jsd_ref(c, bg) * occ[k] for k, c in enumerate(cols)])
        sm = CS.capra_singh_score(aln, bg)
        rsm = [0.5 * jsd[k] + 0.5 * np.mean(list(jsd[max(0, k - 3):k]) + list(jsd[k + 1:k + 4])) for k in range(L)]
        check(f'{tag}: capra_singh_score == scipy JSD x occupancy + smoothing', np.abs(np.array(sm) - np.array(rsm)).max() < 1e-9, f'{np.abs(np.array(sm)-np.array(rsm)).max():.1e}')
        BL = substitution_matrices.load('BLOSUM62')
        spr, _ = ref.sp_ref(rows, BL)
        out['sp_ref'] = spr
        kd = [KP.kimura_protein_distance(rows[a], rows[b]) for a, b in pairs]
        kr = [ref.kimura_ref(rows[a], rows[b]) for a, b in pairs]
        fin = [(x, y) for x, y in zip(kd, kr) if np.isfinite(x) and np.isfinite(y)]
        edge = 0
        for (a, b), x, y in zip(pairs, kd, kr):
            if np.isinf(x) != np.isinf(y):
                both = [(u, v) for u, v in zip(rows[a], rows[b]) if u != '-' and v != '-']
                pp = 1 - sum(u == v for u, v in both) / len(both)
                edge += (0.85 <= pp < 0.8542 and np.isinf(x) and np.isfinite(y))   # Skill's documented 0.85 cut-off vs formula's 0.854 pole
                assert 0.85 <= pp < 0.8542, (pp, x, y)
        check(f'{tag}: Kimura == reference on finite pairs (inf only at the documented p>=0.85 cut-off)', all(abs(x - y) < 1e-9 for x, y in fin), f'{len(fin)} finite of {len(pairs)}; {edge} pairs in the 0.85 <= p < 0.854 band (Skill inf, formula finite)')
    else:
        subs = SC.substitution_counts(aln)
        ti, tv, amb = SC.transition_transversion(subs)
        rti, rtv, ramb = titv_ref(rows)
        check(f'{tag}: Ti/Tv (ACGT pairs; N/ambiguity separate) == independent count', (ti, tv, amb) == (rti, rtv, ramb), f'ti={ti} tv={tv} other={amb} ratio {ti/tv if tv else float("nan"):.3f}')
        out['titv'] = (ti, tv, amb)
    check(f'{tag}: all-numeric outputs finite where defined (no inf/NaN leak in IC/entropy/PSSM)', np.isfinite(ic).all() and np.isfinite(ent).all() and all(np.isfinite(list(ps[k].values())).all() for k in range(L)), '')
    if out_cli:
        for f in ['identity_matrix.py', 'entropy_analysis.py', 'conservation_profile.py', 'gap_statistics.py', 'pssm.py', 'substitution_counts.py', 'kimura_protein_distance.py', 'capra_singh_jsd.py']:
            if kind == 'dna' and f in ('kimura_protein_distance.py', 'capra_singh_jsd.py'):
                continue
            p = subprocess.run([sys.executable, '-B', f, path] + (['pid4'] if f == 'identity_matrix.py' else []), cwd=EX, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'), timeout=900)
            ok = p.returncode == 0 and len(p.stdout.splitlines()) > 3
            check(f'{tag}: CLI {f} rc 0 with output', ok, f'{len(p.stdout.splitlines())} lines; stderr: {p.stderr.strip()[:110]!r}')
    return out
