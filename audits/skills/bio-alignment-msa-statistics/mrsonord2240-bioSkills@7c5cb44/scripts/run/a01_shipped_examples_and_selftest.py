"""A01. Shipped-means-present + run the shipped examples from a COPY, then MUTATION-TEST selftest.py.

Question 1: do all 9 examples run with no arguments, and does the OUTPUT contain the hand-derived numbers?
Question 2: does selftest.py test anything, or does it pass vacuously?  Each mutation below breaks one
            documented behaviour in a scratch copy; a selftest that tests something must exit non-zero.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python a01_shipped_examples_and_selftest.py
"""
import os, shutil, subprocess, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'skill', 'examples')
WORK = os.path.join(HERE, 'work_a01')
PY = sys.executable
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
res = {}

def run(cmd, cwd, timeout=300):
    p = subprocess.run([PY, '-B'] + cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', env=ENV, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def check(name, ok, detail=''):
    res[name] = (bool(ok), detail)
    print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

shutil.rmtree(WORK, ignore_errors=True)
shutil.copytree(SRC, os.path.join(WORK, 'copy'))
CP = os.path.join(WORK, 'copy')

# ---- shipped-means-present: every file SKILL.md / usage-guide.md name under examples/ ----
md = open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read() + open(os.path.join(HERE, 'skill', 'usage-guide.md'), encoding='utf-8').read()
XREF = {'henikoff_weights.py', 'neff.py', 'mi_apc.py'}  # live in alignment/msa-parsing, checked below
named = sorted(set(re.findall(r'examples/([A-Za-z0-9_./]+\.(?:py|fasta))', md)) - XREF)
missing = [n for n in named if not os.path.exists(os.path.join(SRC, n))]
check('present: every examples/ file named in SKILL.md/usage-guide.md exists', not missing, f'{len(named)} named: {named}; missing {missing}')
for n in ['henikoff_weights.py', 'neff.py', 'mi_apc.py']:
    p = os.path.join('F:/OpenScience/wt/al-msastats/alignment/msa-parsing/examples', n)
    check(f'present: cross-referenced msa-parsing/examples/{n}', os.path.exists(p), p)

# ---- run every example with NO arguments and assert on content ----
print('\n=== A. shipped examples, no arguments (from a copy) ===')
expect = {
    'identity_matrix.py': [r'PID4', r'66\.7%', r'Average pairwise identity: \d+\.\d%  \(0 undefined'],
    'conservation_profile.py': [r'Average conservation: 89\.6% over 8 of 8 columns'],
    'entropy_analysis.py': [r'protein \(Robinson', r'0\.918', r'1\.000'],
    'gap_statistics.py': [r'Total gaps: 5', r'Gap-free columns: 3', r'All-gap columns: 0'],
    'kimura_protein_distance.py': [r'0\.439'],
    'pssm.py': [r'PSSM with 8 positions'],
    'substitution_counts.py': [r'Transitions: 4', r'Transversions: 2', r'Ambiguity-code pairs \(excluded from Ti/Tv\): 2', r'Ti/Tv ratio: 2\.00'],
    'capra_singh_jsd.py': [r'Top 10 most conserved'],
}
for f in sorted(os.listdir(CP)):
    if not f.endswith('.py') or f in ('msa_utils.py', 'selftest.py'):
        continue
    rc, out, err = run([f], CP)
    pats = expect.get(f, [])
    got = [bool(re.search(p, out)) for p in pats]
    check(f'A {f}: rc 0, stderr empty, output contains {pats}', rc == 0 and not err.strip() and all(got), f'rc={rc} lines={len(out.splitlines())} stderr={err.strip()[:150]!r} hits={got}')
    open(os.path.join(WORK, f'out_{f}.txt'), 'w', encoding='utf-8').write(out)

rc, out, err = run(['selftest.py'], CP)
oks = re.findall(r'^OK  (.+)$', out, flags=re.M)
check('A selftest.py exits 0, prints "All checks passed", 11 OK lines', rc == 0 and 'All checks passed' in out and len(oks) == 11, f'rc={rc} n_OK={len(oks)} stderr={err.strip()[:150]!r}')
print(out)

# ---- MUTATION TESTS ----
print('\n=== B. mutation tests: does selftest.py FAIL when a documented behaviour is broken? ===')
MUT = [
    ('PID1 denominator reverted to old any-residue-anywhere (function)', 'identity_matrix.py',
     "        span = range(both[0], both[-1] + 1) if both else range(0)\n        denom = sum(seq1[i] != '-' or seq2[i] != '-' for i in span)",
     "        denom = sum(a != '-' or b != '-' for a, b in zip(seq1, seq2))"),
    ('PID1 vectorized: span mask removed', 'identity_matrix.py',
     "denom = ((residue[i] | residue) & in_span).sum(axis=1) * both.any(axis=1)",
     "denom = (residue[i] | residue).sum(axis=1) * both.any(axis=1)"),
    ('PID4 denominator uses min instead of mean (function)', 'identity_matrix.py',
     "denom = (len(seq1.replace('-', '')) + len(seq2.replace('-', ''))) / 2",
     "denom = min(len(seq1.replace('-', '')), len(seq2.replace('-', '')))"),
    ('undefined identity returns 0 instead of NaN (all-gap row)', 'identity_matrix.py',
     "        return float('nan')  # an all-gap sequence has no identity to anything",
     "        return 0.0"),
    ('information_content back to background.get(r, 1e-9) fallback', 'entropy_analysis.py',
     "    letters = [r for r in column if r in background]\n    if not letters:\n        return 0.0\n    total = len(letters)\n    return sum((c / total) * math.log2((c / total) / background[r]) for r, c in Counter(letters).items())",
     "    letters = [r for r in column if r != '-']\n    if not letters:\n        return 0.0\n    total = len(letters)\n    return sum((c / total) * math.log2((c / total) / background.get(r, 1e-9)) for r, c in Counter(letters).items())"),
    ('Shannon entropy in nats', 'entropy_analysis.py', "entropy -= p * math.log2(p)", "entropy -= p * math.log(p)"),
    ('min_occupancy rule removed from column_conservation', 'conservation_profile.py',
     "    if not column or (ignore_gaps and len(column) / len(full) < min_occupancy):", "    if not column:"),
    ('conservation_profile window uncentred [i-w, i]', 'conservation_profile.py',
     "chunk = scores[max(0, i - half):i + half + 1]", "chunk = scores[max(0, i - 2 * half):i + 1]"),
    ('normalize_alignment stops upper-casing', 'msa_utils.py', "        if upper:\n            seq = seq.upper()", "        if False:\n            seq = seq.upper()"),
    ("normalize_alignment stops mapping '.' to '-'", 'msa_utils.py', ".replace('.', '-').replace('~', '-')", ".replace('~', '-')"),
    ('normalize_alignment U->T dropped', 'msa_utils.py', "seq = seq.replace('U', 'T').replace('u', 't')", "pass"),
    ('is_nucleotide always False', 'msa_utils.py', "    return sum(text.count(c) for c in 'ACGTUN') / len(text) >= min_fraction", "    return False"),
    ('Ti/Tv: transitions set wrong', 'substitution_counts.py', "TRANSITIONS = ({'A', 'G'}, {'C', 'T'})", "TRANSITIONS = ({'A', 'C'}, {'G', 'T'})"),
    ('Ti/Tv: N pairs counted as transversions', 'substitution_counts.py',
     "tv = sum(v for k, v in counts.items() if set(k) <= set('ACGT') and set(k) not in TRANSITIONS)",
     "tv = sum(v for k, v in counts.items() if set(k) not in TRANSITIONS)"),
    ('PSSM: n counts letters outside background', 'pssm.py',
     "        column = [c for c in alignment[:, col_idx] if c in background]",
     "        column = [c for c in alignment[:, col_idx] if c != '-']"),
    ('PSSM: pseudocount not weighted by background', 'pssm.py',
     "(counts.get(residue, 0) + pseudocount * background[residue]) / (n + pseudocount))",
     "(counts.get(residue, 0) + pseudocount / len(background)) / (n + pseudocount))"),
    ('Kimura: 0.2 -> 0.25', 'kimura_protein_distance.py', "1 - p - 0.2 * p ** 2", "1 - p - 0.25 * p ** 2"),
    ('Capra-Singh: gap penalty removed', 'capra_singh_jsd.py',
     "gap_penalty = 1.0 - full_column.count('-') / n_seqs", "gap_penalty = 1.0"),
    ('Capra-Singh: lambda smoothing removed', 'capra_singh_jsd.py',
     "smoothed.append((1 - lambda_window) * score + lambda_window * sum(neighbours) / len(neighbours))", "smoothed.append(score)"),
    ('gap_statistics.py all-gap logic (script only, not imported by selftest)', 'gap_statistics.py',
     "all_gap = sum(1 for g in gaps_per_col if g == num_seqs)", "all_gap = 99"),
]
caught, missed = [], []
for i, (name, fn, old, new) in enumerate(MUT):
    d = os.path.join(WORK, f'mut{i:02d}')
    shutil.copytree(CP, d)
    p = os.path.join(d, fn)
    src = open(p, encoding='utf-8').read()
    assert old in src, f'mutation {i} target not found in {fn}: vacuous mutation'
    open(p, 'w', encoding='utf-8', newline='').write(src.replace(old, new, 1))
    rc, out, err = run(['selftest.py'], d)
    tail = (err.strip().splitlines() or out.strip().splitlines() or [''])[-1][:110]
    status = 'CAUGHT' if rc != 0 else 'SURVIVED'
    (caught if rc != 0 else missed).append(name)
    print(f'  mut{i:02d} [{status}] {name}  ({fn})  -> {tail}')
check('B mutation score', True, f'{len(caught)}/{len(MUT)} caught by selftest.py; survivors: {missed}')
res['mutation'] = (True, json.dumps({'caught': caught, 'survived': missed}))
json.dump({k: list(v) for k, v in res.items()}, open(os.path.join(HERE, 'results_a01.json'), 'w'), indent=1)
shutil.rmtree(WORK, ignore_errors=True)
