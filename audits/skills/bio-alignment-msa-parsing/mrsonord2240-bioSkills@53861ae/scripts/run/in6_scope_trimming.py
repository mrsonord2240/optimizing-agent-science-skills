"""Input 6 (Scope boundary, regression of first-audit input 6): 'Trim this Pfam globin alignment for tree building AND for
HMM building, keep the original column numbers, and mask unreliable columns (the first audit asked for GUIDANCE2, now replaced
by the MUSCLE5 ensemble route). Then stream the file with pyhmmer weights.'
REAL data: Pfam PF00042 seed; 8 UniProt globins; MUSCLE 5.3 ensembles produced by wsl_tools.sh (muscle_ens8, muscle_ens73).
The MUSCLE5 route is run EXACTLY as SKILL.md writes it, then examples/muscle5_column_confidence.py (from the copy) is run and
its decoded CC is compared with an independent replicate-agreement count computed from the raw .efa file."""
import os, re, subprocess, sys
import numpy as np
from Bio import AlignIO, SeqIO
from common import *
import pyhmmer

skill_md = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
PY = sys.executable

# ---- 1. trimAl -colnumbering / ClipKIT (routing table rows) --------------------------------------------------------
orig = AlignIO.read(os.path.join(DATA, 'pfam_PF00042_seed.fasta'), 'fasta')
arr = np.array([list(str(r.seq)) for r in orig]); L = arr.shape[1]
txt = open(os.path.join(DATA, 'trimal_colnumbering.txt'), encoding='utf-8').read()
m = re.search(r'#ColumnsMap\s*(.*)', txt)
colmap = [int(x) for x in m.group(1).replace('\t', '').split(',') if x.strip()] if m else []
tri = AlignIO.read(os.path.join(DATA, 'trimal_gappyout.fa'), 'fasta')
print(f'trimAl -gappyout: {tri.get_alignment_length()} of {L} columns kept, colmap {len(colmap)}')
check('trimAl -colnumbering: map has one entry per kept column and trimmed rows == original columns at mapped indices (0-based)',
      len(colmap) == tri.get_alignment_length() and all(str(tri[i].seq) == ''.join(arr[i, colmap]) for i in range(len(orig))),
      f'{len(colmap)} map entries')
ck = AlignIO.read(os.path.join(DATA, 'clipkit_kpic.fa'), 'fasta')
def is_subseq(a, b):
    it = iter(b)
    return all(ch in it for ch in a)
check('ClipKIT kpic-smart-gap (routing row for tree input) valid: 73 seqs, 121 of 141 columns, every row a column-subsequence of the original',
      len(ck) == 73 and ck.get_alignment_length() == 121 and all(is_subseq(str(ck[i].seq), ''.join(arr[i])) for i in range(73)),
      f'{ck.get_alignment_length()} columns')
check('SKILL.md tip "aggressive trimming (>20-30% of sites) hurts trees": both routed tools trim <= 30% on this seed',
      (1 - tri.get_alignment_length() / L) <= 0.30 and (1 - ck.get_alignment_length() / L) <= 0.30,
      f'trimAl {(1 - tri.get_alignment_length() / L) * 100:.1f}%, ClipKIT {(1 - ck.get_alignment_length() / L) * 100:.1f}% trimmed')

# ---- 2. GUIDANCE2 is gone from the recommendations -----------------------------------------------------------------
n_g = len(re.findall('GUIDANCE2', skill_md))
print('GUIDANCE2 mentions in SKILL.md:', n_g, '| TCS:', len(re.findall(r'\bTCS\b', skill_md)), '| 0.93:', skill_md.count('0.93'))
check('GUIDANCE2 no longer recommended: both mentions are negative ("not offered", "0.93 does not transfer"); no TCS',
      n_g == 2 and 'GUIDANCE2 is not offered' in skill_md and "GUIDANCE2's 0.93 does not transfer" in skill_md and not re.search(r'TCS', skill_md))

# ---- 3. MUSCLE5 ensemble route --------------------------------------------------------------------------------------
def read_efa(path):
    blocks, cur = {}, None
    for line in open(path, encoding='utf-8'):
        if line.startswith('<'):
            cur = line[1:].strip(); blocks[cur] = []
        elif cur is not None:
            blocks[cur].append(line)
    out = {}
    for k, ls in blocks.items():
        recs = []
        name, seq = None, []
        for l in ls:
            l = l.rstrip('\n')
            if l.startswith('>'):
                if name is not None: recs.append((name, ''.join(seq)))
                name, seq = l[1:].split()[0], []
            else:
                seq.append(l)
        recs.append((name, ''.join(seq)))
        out[k] = recs
    return out

def columns(recs):
    """list of frozensets of (sequence NAME, residue index) per column, for a replicate without _conf_ rows.
    Keyed by name because replicates in an .efa list the sequences in different orders."""
    recs = [r for r in recs if not r[0].startswith('_conf_')]
    pos = {n: 0 for n, _ in recs}; cols = []
    for c in range(len(recs[0][1])):
        s = []
        for n, q in recs:
            if q[c] != '-':
                s.append((n, pos[n])); pos[n] += 1
        cols.append(frozenset(s))
    return cols

def run_family(tag, edir, best_expect, n_expect_cols, claim):
    efa_cc = os.path.join(edir, 'ens_cc.efa'); efa = os.path.join(edir, 'ens.efa')
    # (a) the example script exactly as SKILL.md documents it, run from the COPY of the Skill
    p = subprocess.run([PY, os.path.join(EX, 'muscle5_column_confidence.py'), efa_cc, best_expect], cwd=edir, capture_output=True, text=True,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    print(f'--- {tag}: muscle5_column_confidence.py {best_expect} rc={p.returncode}\n{p.stdout}{p.stderr[-300:]}')
    check(f'{tag}: example script runs (rc 0) and prints the survivors per cut-off', p.returncode == 0 and 'CC >= 0.9' in p.stdout)
    surv = {float(a): int(b) for a, b in re.findall(r'CC >= ([0-9.]+): (\d+) columns', p.stdout)}
    # (b) independent ground truth: fraction of the 16 replicates containing the IDENTICAL column
    reps = read_efa(efa)                               # replicates of ens.efa (no _conf_ rows)
    reps_cc = read_efa(efa_cc)
    names = list(reps)
    best_cols = columns(reps[best_expect])
    rep_colsets = [set(columns(reps[n])) for n in names]
    agree = np.array([sum(c in s for s in rep_colsets) / len(names) for c in best_cols])
    # decode CC independently (digits, '+' = 10)
    rows = {n: s for n, s in reps_cc[best_expect] if n.startswith('_conf_')}
    dg = lambda ch: 10 if ch == '+' else int(ch)
    cc = np.array([min(1.0, (10 * dg(a) + dg(b)) / 100) for a, b in zip(rows['_conf_'], rows['_conf_2'])])
    print(f'{tag}: {len(cc)} columns; corr(CC, replicate agreement) = {np.corrcoef(cc, agree)[0, 1]:.3f}; '
          f'max |CC - agreement| = {np.abs(cc - agree).max():.3f}')
    check(f'{tag}: decoded CC has one value per alignment column (best replicate {best_expect}: {n_expect_cols} columns)', len(cc) == n_expect_cols, f'{len(cc)}')
    check(f'{tag}: script survivor counts equal my own decode of the _conf_ rows at 0.5/0.7/0.9/0.99',
          all(surv[c] == int((cc >= c).sum()) for c in (0.5, 0.7, 0.9, 0.99)), str(surv))
    low = cc < 0.9
    disagreeing = agree < 0.9
    # meaningful ground-truth relation: columns that the replicates disagree on must be low-CC columns
    check(f'{tag}: every column present in < 90% of the replicates has CC < 0.9 (CC is a real replicate-agreement measure)',
          bool(np.all(low[disagreeing])), f'{int(disagreeing.sum())} disagreeing cols, {int((low & disagreeing).sum())} of them low CC; total low CC {int(low.sum())}')
    check(f'{tag}: columns the replicates agree on (>= 90%) have higher mean CC than columns they disagree on',
          cc[~disagreeing].mean() > cc[disagreeing].mean(), f'mean CC {cc[~disagreeing].mean():.3f} vs {cc[disagreeing].mean():.3f}')
    # (c) masking: write masked.fa with 0.9, verify columns kept == CC>=0.9 and content == best replicate at those columns
    out = os.path.join(edir, 'masked_0.9.fa')
    p2 = subprocess.run([PY, os.path.join(EX, 'muscle5_column_confidence.py'), efa_cc, best_expect, '0.9', out], cwd=edir, capture_output=True, text=True,
                        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    masked = AlignIO.read(out, 'fasta')
    best_recs = [r for r in reps_cc[best_expect] if not r[0].startswith('_conf_')]
    keep = np.flatnonzero(cc >= 0.9)
    okc = masked.get_alignment_length() == len(keep) and all(masked[i].id == best_recs[i][0] and str(masked[i].seq) == ''.join(best_recs[i][1][k] for k in keep) for i in range(len(best_recs)))
    check(f'{tag}: masked.fa (CC >= 0.9) = exactly the best replicate restricted to CC >= 0.9 columns', okc and len(masked) == len(best_recs),
          f'{masked.get_alignment_length()} columns, {len(masked)} rows')
    check(f'{tag}: SKILL claim reproduced: {claim[0]}', claim[1](int(low.sum()), len(cc), int((cc >= 0.9).sum())), f'CC<0.9: {int(low.sum())}, CC>=0.9: {int((cc >= 0.9).sum())}')
    return cc, agree

cc8, ag8 = run_family('8 globins', os.path.join(DATA, 'ens8'), 'acb.2', 155,
                      ('"On 8 UniProt globins 11 of 155 columns had CC < 0.9"', lambda lo, n, hi: (lo, n) == (11, 155)))
cc73, ag73 = run_family('73 Pfam', os.path.join(DATA, 'ens73'), 'bca.2', 156,
                        ('my own count on 73 Pfam sequences: 60 columns at CC >= 0.9 (SKILL.md makes no 73-sequence claim)', lambda lo, n, hi: hi == 60))
# SKILL.md sentence: "including every column whose residue pairing differed in more than 10% of the 16 replicates"
check('SKILL.md claim: every 8-globin column that differs in >10% of the 16 replicates is CC < 0.9', bool(np.all((cc8 < 0.9)[ag8 < 0.9])))

# the documented stderr claim: 'stderr ends "best <name>"'
part2 = open(os.path.join(HERE, 'wsl_tools_output.txt'), encoding='utf-8').read()
m = re.search(r'CC min .*best (\S+)\n(.*)\n', part2)
print('muscle -maxcc stderr tail:', repr(m.group(0)) if m else None)
check('SKILL.md: "stderr ends \\"best <name>\\"" -- the line "CC min .., best acb.2" exists but is followed by a URL line',
      bool(m) and m.group(1) == 'acb.2' and m.group(2).startswith('https://'), 'name is on the second-to-last line, not the last (cosmetic)')

# ---- 4. pyhmmer streaming (SKILL.md "Streaming Large Alignments") ------------------------------------------------------
multi = os.path.join(DATA, 'syn_multi_stockholm.sto')
sto = open(PFAM_STO, encoding='utf-8').read()
open(multi, 'w', encoding='utf-8', newline='\n').write(sto + sto)
sums = []
with pyhmmer.easel.MSAFile(multi, digital=True) as f:
    for msa in f:
        sums.append((len(msa.sequences), round(float(sum(msa.compute_weights(method='pb'))), 3)))
check('pyhmmer streaming pattern (iterate MSAFile, compute_weights pb) works on a 2-alignment Stockholm file; sums equal N', sums == [(73, 73.0), (73, 73.0)], str(sums))

# ---- 5. version block ---------------------------------------------------------------------------------------------
vb = skill_md.split('# MSA Parsing and Analysis')[0]
check('Version block lists pyhmmer >= 0.11.3, the checked versions and an install line',
      'pyhmmer >= 0.11.3' in vb and 'pyhmmer 0.12.3' in vb and 'pip install biopython numpy pyhmmer' in vb)
print('installed pyhmmer', pyhmmer.__version__)
summary()
