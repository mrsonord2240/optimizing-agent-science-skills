"""Input 1 (Canonical, regression of first-audit input 1): 'Here is the Pfam globin seed alignment (PF00042, 73 sequences,
Stockholm). List the sequence IDs, show me the GLB2_LUMTE record, find the fully conserved columns and the ones conserved in at
least 80% of sequences, count gaps per sequence and per column, and give me a 70% consensus.'
REAL data (Pfam PF00042 seed 73 x 141). Code = every python block of SKILL.md exec'd from the file (skillns.py; examples/ is NOT
on the path) + four shipped examples run from the copy. Ground truth = my own parse of the raw Stockholm text, no Biopython."""
import os, subprocess, sys
from collections import Counter
import numpy as np
from common import *
import skillns

ns, log = skillns.load()
check('all 25 python blocks of SKILL.md execute with no examples/ on the path (no NameError/import error)', all(ok for _, ok, _, _ in log),
      f"{sum(ok for _, ok, _, _ in log)}/{len(log)}: " + '; '.join(f'block {i}: {o}' for i, ok, _, o in log if not ok))
from Bio import AlignIO
aln = AlignIO.read(PFAM_STO, 'stockholm')

# ---- independent ground truth from the raw text -------------------------------------------------------------------
raw = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); raw[n] = s
ids_raw = list(raw)
arr = np.array([list(s.upper()) for s in raw.values()])
isgap = np.isin(arr, ['-', '.'])
N, L = arr.shape
print('gap characters in the raw file:', sorted(set(arr[isgap])), '| chars Biopython returns for the same cells:', sorted({c for r in aln for c in str(r.seq) if c in '-.'}))

check('shape 73 x 141', (len(aln), aln.get_alignment_length()) == (73, 141) == (N, L))
check('IDs equal the raw file IDs, in order', [r.id for r in aln] == ids_raw)
t = ns['get_sequence_by_id'](aln, 'GLB2_LUMTE/31-141')
check('get_sequence_by_id returns the GLB2_LUMTE record; missing id returns None', t is not None and t.id == 'GLB2_LUMTE/31-141' and ns['get_sequence_by_id'](aln, 'nope') is None)
check('alignment[:, 5] is a str of length 73 equal to the raw column', isinstance(aln[:, 5], str) and aln[:, 5].upper() == ''.join(arr[:, 5]).replace('.', '-'))

# ---- conserved columns: independent implementation (column majority over non-gap residues, denominator = all rows) --------
def indep_conserved(thr):
    out = []
    for j in range(L):
        c = Counter(arr[~isgap[:, j], j])
        if not c: continue
        top, n = c.most_common(1)[0]
        if n / N >= thr - 1e-12: out.append((j, top, n / N))
    return out
full = ns['find_conserved_positions'](aln, threshold=1.0)
m80 = ns['find_conserved_positions'](aln, threshold=0.8)
print('fully conserved:', full, '| >=80%:', [(a, b) for a, b, _ in m80])
check('find_conserved_positions(1.0) == independent count (cols 17 F, 77 H)', [(a, b) for a, b, _ in full] == [(a, b) for a, b, _ in indep_conserved(1.0)] == [(17, 'F'), (77, 'H')])
check('find_conserved_positions(0.8) == independent (columns, residues and fractions)',
      [(a, b) for a, b, _ in m80] == [(a, b) for a, b, _ in indep_conserved(0.8)] and np.allclose([c for *_, c in m80], [c for *_, c in indep_conserved(0.8)]))
check('conserved tuples are 3-tuples (col, residue, fraction) as documented', all(len(x) == 3 for x in full))

# ---- gaps: 3 independent counts of the same 1943 cells ----------------------------------------------------------------------
per_seq = [(r.id, str(r.seq).count('-') + str(r.seq).count('.')) for r in aln]
gp = ns['gaps_per_column'](aln)
print('sum gaps/seq', sum(g for _, g in per_seq), '| sum gaps/col', sum(gp), '| raw-file count', int(isgap.sum()))
check('gaps per sequence (SKILL snippet, after normalisation) == raw-file count', [ns_g for ns_g in [str(r.seq).count('-') for r in ns['normalize_alignment'](aln)]] == list(isgap.sum(1)))
check('gaps_per_column == raw-file per-column count, total 1943', gp == list(isgap.sum(0)) and sum(gp) == 1943)

# ---- consensus -------------------------------------------------------------------------------------------------------------
def indep_consensus(thr, amb):
    o = []
    for j in range(L):
        c = Counter(arr[~isgap[:, j], j])
        if not c: o.append('-'); continue
        top, n = c.most_common(1)[0]
        o.append(top if n / N >= thr else amb)
    return ''.join(o)
c70 = ns['consensus_sequence'](aln, threshold=0.7)
c50 = ns['consensus_sequence'](aln, threshold=0.5)
print('consensus 0.7:', c70); print('consensus 0.5:', c50)
check('consensus (default) equals independent consensus with X placeholder at 0.7 and 0.5', c70 == indep_consensus(0.7, 'X') and c50 == indep_consensus(0.5, 'X'))
asn_cols = sum(1 for j in range(L) if Counter(arr[~isgap[:, j], j]).most_common(1)[0][0] == 'N' and Counter(arr[~isgap[:, j], j]).most_common(1)[0][1] / N >= 0.5)
print(f"protein consensus 0.5: {c50.count('X')} X, {c50.count('N')} N; true Asn-majority columns: {asn_cols}")
check("protein consensus placeholder is X: the count of 'N' equals the true Asn-majority columns (was 124 spurious N)", c50.count('N') == asn_cols and c50.count('X') > 100, f"X={c50.count('X')} N={c50.count('N')} asn_cols={asn_cols}")
check("ambiguous='N' can still be forced; nucleotide alphabet auto-detected as False for this protein alignment", ns['consensus_sequence'](aln, 0.5, ambiguous='N').count('N') > 100 and ns['is_nucleotide'](aln) is False)
check('SKILL.md prose states the gap-row denominator', 'gap rows included' in open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read())

# ---- shipped examples, run from the COPY with the real .sto (raw "." gaps) --------------------------------------------------
def run_ex(name, *args):
    p = subprocess.run([sys.executable, os.path.join(EX, name), *args], cwd=DATA, capture_output=True, text=True,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'})
    return p
rcs = {}
for ex in ('analyze_alignment.py', 'find_conserved.py', 'gap_analysis.py', 'consensus_sequence.py'):
    p = run_ex(ex, PFAM_STO)
    rcs[ex] = (p.returncode, p.stderr)
    print(f'--- {ex}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} stderr={p.stderr[-200:]!r}')
    if ex == 'analyze_alignment.py':
        print(p.stdout[:500])
        col0 = Counter(arr[:, 0]); top = col0.most_common(1)[0]
        check('analyze_alignment.py: header 73 x 141 and the Col 0 composition dict equals the raw-file counts', 'Alignment: 73 sequences, 141 columns' in p.stdout and f"Col 0: {dict(Counter(''.join(arr[:, 0])))}" in p.stdout, p.stdout.splitlines()[3][:140])
    if ex == 'find_conserved.py':
        check('find_conserved.py prints Position 17: F and Position 77: H as the fully conserved columns', p.returncode == 0 and 'Position 17: F' in p.stdout and 'Position 77: H' in p.stdout and p.stdout.count('Position') >= 5, p.stdout.replace('\n', ' | ')[:200])
    if ex == 'gap_analysis.py':
        per_col_lines = [l for l in p.stdout.splitlines() if l.startswith('  Column ')]
        tot = sum(int(l.split(':')[1].split()[0]) for l in per_col_lines)
        per_seq_tot = sum(int(l.split(':')[1].split()[0]) for l in p.stdout.splitlines() if l.startswith('  ') and not l.startswith('  Column '))
        check('gap_analysis.py: per-sequence lines and per-column lines each sum to 1943', tot == per_seq_tot == 1943, f'{tot} {per_seq_tot}')
    if ex == 'consensus_sequence.py':
        lines = p.stdout.splitlines()
        got50 = lines[lines.index('Consensus (50% threshold):') + 1]
        check('consensus_sequence.py 50% output equals the independent consensus (X placeholder)', got50 == indep_consensus(0.5, 'X'))
check('all four examples exit 0 with empty stderr on the real seed', all(rc == 0 and not err for rc, err in rcs.values()), str({k: v[0] for k, v in rcs.items()}))
summary()
