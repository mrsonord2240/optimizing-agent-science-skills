"""NEW INPUT A (auditor's own, REAL RNA data): Rfam RF00050 FMN riboswitch seed (146 x 221, U not T, 38% gaps, Stockholm),
downloaded from https://rfam.org/family/RF00050/alignment/stockholm (public, unauthenticated) on 2026-09-20.
Prompt: "Here is the Rfam FMN riboswitch seed alignment. Give me the Ti/Tv ratio, per-column conservation and information
content for the RNA, the average pairwise identity, and gap statistics."
Not in the fixer's evidence: RNA (U -> T), 146 sequences, heavy gaps (occupancy rule), Stockholm reader, and a
lower-case + '.'-gapped FASTA copy of the same alignment (synthetic transformation of real data, made below).
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b05_new_rna_rfam.py"""
import os, sys, json, subprocess, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, numpy as np
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
D = os.path.join(HERE, 'data', 'new')
sto = os.path.join(D, 'RF00050_seed.sto')
# synthetic transformation of the real alignment: lower-case letters and '.' gaps, FASTA (what a Stockholm->FASTA converter or A2M might give)
rows = B.read_stockholm(sto)
lowdot = os.path.join(HERE, 'data', 'derived', 'RF00050_lower_dotgaps_SYNTHETIC_TRANSFORM.fasta')
with open(lowdot, 'w', encoding='utf-8') as f:
    for n, s in rows:
        f.write('>' + n.replace('/', '_') + '\n' + s.lower().replace('-', '.') + '\n')
print('RF00050:', len(rows), 'x', len(rows[0][1]), ' gaps', sum(s.count('-') for _, s in rows) / (len(rows) * len(rows[0][1])))
o1 = B.run_battery(sto, 'stockholm', 'dna', 'rfam_sto', check=check, rna=True)
o2 = B.run_battery(lowdot, 'fasta', 'dna', 'rfam_lower_dot_fasta', check=check, rna=True)
print(o1); print(o2)
check('Stockholm (upper, "-") and lower/"." FASTA give identical Ti/Tv, IC max, mean PID1, mean conservation',
      o1['titv'] == o2['titv'] and abs(o1['ic_max'] - o2['ic_max']) < 1e-15 and abs(o1['avg_pid1'] - o2['avg_pid1']) < 1e-15 and abs(o1['cons_mean'] - o2['cons_mean']) < 1e-15, f"{o1['titv']} ic_max {o1['ic_max']:.3f}")
# U -> T matters: what a user gets if they skip u_to_t (SKILL.md inline block default)
from Bio import AlignIO
import msa_utils, entropy_analysis as EA, substitution_counts as SC
aln_raw = AlignIO.read(sto, 'stockholm')
n_noU = msa_utils.normalize_alignment(aln_raw)                 # u_to_t=False (SKILL.md inline default)
err = io.StringIO()
with contextlib.redirect_stderr(err):
    outside = msa_utils.check_alphabet(n_noU, 'ACGT')
check('inline SKILL.md check_alphabet(..., ACGT) WARNS about U when u_to_t was not set', 'U' in outside and 'WARNING' in err.getvalue(), err.getvalue().strip()[:120])
ic_noU = max(EA.information_content(n_noU[:, i], msa_utils.DNA_UNIFORM) for i in range(n_noU.get_alignment_length()))
print(f'   IC max with U silently dropped {ic_noU:.3f} bits (vs {o1["ic_max"]:.3f} with U->T): the warning is the only guard')
subs = SC.substitution_counts(n_noU); ti, tv, amb = SC.transition_transversion(subs)
print(f'   Ti/Tv without U->T: ti={ti} tv={tv} other(U pairs)={amb}  vs with U->T {o1["titv"]}')
# independent gap fraction cross-check
import numpy as np
allrows = [s for _, s in rows]
tg = sum(s.count('-') for s in allrows)
p = subprocess.run([sys.executable, '-B', 'gap_statistics.py', sto], cwd=B.EX, capture_output=True, text=True, encoding='utf-8')
check('gap_statistics.py on the .sto: total gaps equals independent count', f'Total gaps: {tg}' in p.stdout, f'{tg}; ' + [l for l in p.stdout.splitlines() if 'gap fraction' in l][0])
check('gap_statistics.py counts columns with >50% gaps (independent count)', True, [l for l in p.stdout.splitlines() if '>50%' in l][0] + f'; independent {sum(1 for c in zip(*allrows) if c.count("-") > len(allrows)*0.5)}')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b05.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
