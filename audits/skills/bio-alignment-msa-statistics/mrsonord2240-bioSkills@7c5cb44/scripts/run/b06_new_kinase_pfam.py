"""NEW INPUT B (auditor's own, REAL protein data): Pfam PF00069 protein-kinase-domain seed (37 x 419, 36% '.' gaps, many
staggered fragments), from https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00069/?annotation=alignment:seed (2026-09-20).
Prompt: "Here is the Pfam kinase seed alignment. Which columns are conserved, what is the average conservation, how similar
are the sequences (report the identity definition), and what is the BLOSUM62 sum-of-pairs score?"
Not in the fixer's evidence: a gappy protein family with terminal overhangs across most rows, so PID1 and the occupancy rule
matter a lot; run through SKILL.md blocks verbatim, from a dotted FASTA copy and from Stockholm.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b06_new_kinase_pfam.py"""
import os, sys, json, shutil, itertools
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks, ref, numpy as np
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
D = os.path.join(HERE, 'data', 'new'); sto = os.path.join(D, 'PF00069.sto')
rows = B.read_stockholm(sto)
dotfa = os.path.join(HERE, 'data', 'derived', 'PF00069_dotgaps.fasta')
with open(dotfa, 'w', encoding='utf-8') as f:
    for n, s in rows:
        f.write('>' + n.replace('/', '_') + '\n' + s + '\n')          # unchanged '.' gaps, upper case (as Pfam writes)
print('PF00069:', len(rows), 'x', len(rows[0][1]), 'dots', sum(s.count('.') for _, s in rows))
o1 = B.run_battery(sto, 'stockholm', 'protein', 'kinase_sto', check=check)
o2 = B.run_battery(dotfa, 'fasta', 'protein', 'kinase_dot_fasta', check=check)
print(o1)
check('Stockholm and dotted FASTA give identical statistics', all(abs(o1[k] - o2[k]) < 1e-15 for k in ('avg_pid1', 'avg_pid4', 'ic_max', 'cons_mean', 'sp_ref', 'simple_sp_ref')), '')
# SKILL.md blocks verbatim on the dotted FASTA
W = os.path.join(HERE, 'work_b06'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(dotfa, os.path.join(W, 'alignment.fasta')); cwd = os.getcwd(); os.chdir(W)
ns, log = skill_blocks.run_all(verbose=False)
errs = [(i, st) for i, f, st, o in log if st.startswith('ERROR')]
check('SKILL.md python blocks (12 non-stub) run verbatim on the dotted kinase seed', not errs, f'errors {errs}')
aln = ns['alignment']; N, L = len(aln), aln.get_alignment_length()
avg, n_used = ns['average_conservation'](aln)
avg0, n0 = ns['average_conservation'](aln, min_occupancy=0.0)
cols = [''.join(c) for c in zip(*[str(r.seq) for r in aln])]
occ = np.array([1 - c.count('-') / N for c in cols])
cref = np.array([ref.conservation_ref(c) for c in cols])
check('average_conservation (default 0.5) == independent mean over columns with >= 50% residues', abs(avg - cref[occ >= 0.5].mean()) < 1e-12 and n_used == int((occ >= 0.5).sum()), f'{avg*100:.1f}% over {n_used}/{L} columns; with min_occupancy=0: {avg0*100:.1f}% over {n0} (pre-fix all-column mean incl. all-gap columns as 0: {np.mean([ref.conservation_ref(c) for c in cols])*100:.1f}%)')
print(f'   columns with <50% residues: {(occ < .5).sum()}; of those that would report 100% conserved without the rule: {sum(1 for k in range(L) if occ[k] < .5 and 0 < occ[k] and cref[k] == 1.0)}')
# PID definitions on a REAL gappy MSA: span (Skill) vs per-sequence-internal-gap definition (ref.pid_ref)
rws = [str(r.seq) for r in aln]; diffs = []
for a, b in itertools.combinations(range(N), 2):
    s = B.pid_span_ref(rws[a], rws[b])[0]; p = ref.pid_ref(rws[a], rws[b])['PID1']
    diffs.append(abs(s - p))
print(f'   span-PID1 vs per-sequence-internal PID1 on {len(diffs)} real MSA pairs: {sum(d > 1e-9 for d in diffs)} differ, max {max(diffs)*100:.2f} pts, mean over differing {np.mean([d for d in diffs if d > 1e-9])*100 if any(d>1e-9 for d in diffs) else 0:.2f} pts')
import identity_matrix as IM
mm = {m: IM.average_identity(IM.identity_matrix_vectorized(aln, m))[0] * 100 for m in IM.METHODS}
print('   mean identity by definition (%):', {k: round(v, 2) for k, v in mm.items()}, '(SKILL.md: PID2 highest; PID1..4 spread reported)')
check('PID2 is the highest of the four means (SKILL.md claim) and spread is reported', mm['pid2'] == max(mm.values()), str({k: round(v, 2) for k, v in mm.items()}))
os.chdir(cwd); shutil.rmtree(W, ignore_errors=True)
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b06.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
