"""Input 1 (Canonical): 'Here is the Pfam globin seed alignment. List the sequence IDs, pull out species/ID lookups,
find fully conserved and >=80% conserved columns, count gaps per sequence/column, and give a 70% consensus.'
REAL data: Pfam PF00042 seed 73 x 141. Code = SKILL.md snippets (skill_md_funcs.py, verbatim) + shipped examples run from a copy."""
import os, re, inspect, subprocess, shutil, sys
import numpy as np, pandas as pd
from collections import Counter
from Bio import AlignIO
from common import *
import skill_md_funcs as F

# 0. verbatim-copy check of my transcription against SKILL.md
skill_md = open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read()
bad = [n for n, f in inspect.getmembers(F, inspect.isfunction) if f.__module__ == 'skill_md_funcs' and inspect.getsource(f).strip().split('\n')[0] not in skill_md]
check('transcribed functions match SKILL.md signatures', not bad, str(bad))

# 1. Loading (SKILL.md "Loading Alignments") on the real Stockholm file
aln = AlignIO.read(PFAM_STO, 'stockholm')
print(f'{len(aln)} sequences, {aln.get_alignment_length()} columns')
check('shape 73 x 141 (matches Pfam PF00042.29 seed per public-data README)', (len(aln), aln.get_alignment_length()) == (73, 141))

# 2. IDs / strings / by-id / annotations (SKILL.md "Extracting Sequence Information")
seq_ids = [r.id for r in aln]; sequences = [str(r.seq) for r in aln]
check('IDs unique and carry coordinates (GLB2_LUMTE/31-141 present)', len(set(seq_ids)) == 73 and 'GLB2_LUMTE/31-141' in seq_ids)
t = F.get_sequence_by_id(aln, 'GLB2_LUMTE/31-141')
check('get_sequence_by_id returns the record', t is not None and t.id == 'GLB2_LUMTE/31-141')
check('get_sequence_by_id returns None for missing id (skill-documented behaviour)', F.get_sequence_by_id(aln, 'species_A') is None)
print('Annotations sample:', t.annotations, '| desc:', t.description)

# 3. column indexing
col5 = aln[:, 5]
check('aln[:, 5] is a str of len 73', isinstance(col5, str) and len(col5) == 73)

# 4. conserved (SKILL.md version) vs independent pandas/numpy implementation
arr = np.array([list(s) for s in sequences])
def indep_conserved(thr):
    out = []
    for j in range(arr.shape[1]):
        vc = pd.Series(arr[:, j]).value_counts()
        top, n = vc.index[0], vc.iloc[0]
        if top != '-' and n / arr.shape[0] >= thr - 1e-12:
            out.append((j, top))
    return out
full = F.find_conserved_positions(aln, 1.0); m80 = F.find_conserved_positions(aln, 0.8)
print('fully conserved:', full); print('>=80% count:', len(m80), m80[:8])
check('SKILL.md find_conserved_positions(1.0) == independent numpy/pandas', full == indep_conserved(1.0))
check('SKILL.md find_conserved_positions(0.8) == independent', m80 == indep_conserved(0.8))
# Semantic: how many columns are "100% conserved" only because of gaps? (denominator includes gap rows)
n_gap_cols = sum(1 for j in range(141) if '-' in arr[:, j])
print('columns containing >=1 gap:', n_gap_cols, 'of 141')
check('biology sanity: exactly 2 fully conserved columns, Phe (col 17) and His (col 77) -- plausible invariant globin heme-pocket residues (His invariance confirmed independently in in4)', full == [(17, 'F'), (77, 'H')], f'got {full}')

# 5. gaps
gap_counts = [(r.id, str(r.seq).count('-')) for r in aln]
gp = F.gaps_per_column(aln)
check('sum(gaps per seq) == sum(gaps per col) == 1943 (chars counted independently)', sum(g for _, g in gap_counts) == sum(gp) == int((arr == '-').sum()) == 1943)
check("gaps_per_column length == 141", len(gp) == 141)

# 6. consensus 70%
cons70 = F.consensus_sequence(aln, threshold=0.7)
cons50 = F.consensus_sequence(aln, threshold=0.5)
print('consensus 0.7:', cons70)
print('consensus 0.5:', cons50)
check('consensus length == 141', len(cons70) == 141 == len(cons50))
# independent
def indep_cons(thr):
    o = []
    for j in range(arr.shape[1]):
        c = Counter(arr[:, j]); top, n = c.most_common(1)[0]
        if top == '-':
            c.pop('-')
            if c: top, n = c.most_common(1)[0]
            else: o.append('-'); continue
        o.append(top if n / arr.shape[0] >= thr else 'N')
    return ''.join(o)
check('SKILL.md consensus == independent (same algorithm)', cons70 == indep_cons(0.7) and cons50 == indep_cons(0.5))
# Semantic check: on a PROTEIN alignment the default ambiguous='N' collides with asparagine
n_amb = cons50.count('N')
real_asn_cols = sum(1 for j in range(141) if Counter(c for c in arr[:, j] if c != '-').most_common(1)[0][0] == 'N')
print(f"'N' chars in protein consensus(0.5): {n_amb}; columns whose real plurality residue is Asn: {real_asn_cols}")
check("protein consensus: 'N' placeholder is unambiguous (can't tell Asn from 'ambiguous')  [EXPECTED FAIL = defect]", n_amb == real_asn_cols or n_amb == 0,
      f"{n_amb} 'N' in output, only {real_asn_cols} are true Asn plurality columns => {n_amb-real_asn_cols} placeholders masquerade as Asn")

# 7. shipped examples, run from a COPY against alignment.fasta (real data)
ex = os.path.join(HERE, 'ex1'); shutil.rmtree(ex, ignore_errors=True); shutil.copytree(SKILL_EX, ex)
shutil.copy(PFAM_FA, os.path.join(ex, 'alignment.fasta'))
outs = {}
for s in ['analyze_alignment.py', 'find_conserved.py', 'gap_analysis.py', 'consensus_sequence.py']:
    p = subprocess.run([sys.executable, s], cwd=ex, capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'})
    outs[s] = p.stdout
    print(f'--- {s}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} stderr={p.stderr.strip()[:200]!r}')
    print('\n'.join(p.stdout.splitlines()[:6]))
check('analyze_alignment.py: header says 73 sequences, 141 columns and prints 10 columns', 'Alignment: 73 sequences, 141 columns' in outs['analyze_alignment.py'] and outs['analyze_alignment.py'].count('% conserved') == 10)
check('gap_analysis.py: 73 per-sequence lines and per-column gap counts total 1943', len(re.findall(r'^  \S+: \d+ gaps \(', outs['gap_analysis.py'], re.M)) == 73 and sum(int(x) for x in re.findall(r'Column \d+: (\d+) gaps', outs['gap_analysis.py'])) == 1943)
check('consensus_sequence.py: 50% consensus in output equals my independent consensus', indep_cons(0.5) in outs['consensus_sequence.py'])
# find_conserved.py example uses a DIFFERENT definition (gaps removed first, but denominator still N) -> compare
ex_m80 = re.findall(r'Position (\d+): (\S) \((\d+)%\)', outs['find_conserved.py'])
print('example find_conserved 80%+ count:', len(ex_m80), ' SKILL.md version count:', len(m80))
check('example find_conserved.py and SKILL.md find_conserved_positions agree', len(ex_m80) == len(m80))
summary()
