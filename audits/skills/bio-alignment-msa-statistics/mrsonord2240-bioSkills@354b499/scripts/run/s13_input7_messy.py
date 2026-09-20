"""INPUT 7 (Adversarial / ambiguous, SYNTHETIC small alignments): messy real-world content the Skill does not screen for.
Prompt: "Here's the alignment my collaborator sent (mixed case, dots, X/B/Z/U, one empty-looking sequence). What is the percent
identity, conservation and information content?"  Also degenerate inputs (1 sequence, 2 identical, unequal lengths) and two
factual claims in SKILL.md about the BLOSUM Array API. Run from run/."""
import os, sys, math, shutil, json, itertools, traceback
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
from Bio.Align import substitution_matrices
import entropy_analysis as EA, pssm as PS, identity_matrix as IM, capra_singh_jsd as CS, kimura_protein_distance as KP
import skill_blocks
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
wd = os.path.join(HERE, 'work_in7'); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd); os.chdir(wd)

def write(name, rows):
    open(name, 'w').write(''.join(f'>r{i}\n{s}\n' for i, s in enumerate(rows)))

# --- (a) messy SYNTHETIC alignment ---
rows = ['MKV.LAAGXW', 'mkvALAAGVw', 'MKVBLAZGVW', 'MKVULAA*VW', '----------', 'MKV-LAAGVW']
write('alignment.fasta', rows)
shutil.copy('alignment.fasta', 'messy.fasta')
aln = AlignIO.read('alignment.fasta', 'fasta'); N, L = len(aln), aln.get_alignment_length()
ns, log = skill_blocks.run_all(verbose=False)
print('SKILL.md blocks on messy alignment:', {i: st[:70] for i, _, st, _ in log if st not in ('OK', 'SKIPPED_STUB')} or 'all OK')
norm = ref.norm_rows(rows)
print('normalised rows for the reference:', norm)
# identities: row0 vs row1 differ only by case and '.' vs 'A' at col 3 -> after normalising, hand: cols with both residues=... compute
p_sk = ns['pairwise_identity'](rows[0], rows[1], 'pid2'); p_rf = ref.pid_ref(norm[0], norm[1])['PID2']
print(f'  row0 vs row1 PID2: Skill {p_sk*100:.1f}%  reference (case/gap normalised) {p_rf*100:.1f}%')
check('M1 case-insensitive identity (mkv... vs MKV...)', abs(p_sk - p_rf) < 1e-9, f'{p_sk:.3f} vs {p_rf:.3f}')
# all-gap sequence
r_sk = {m: ns['pairwise_identity'](rows[4], rows[0], m) for m in ('pid1', 'pid2', 'pid3', 'pid4')}
print('  all-gap row vs row0:', r_sk, '-> silently 0.0 (undefined); no warning')
check('M2 all-gap sequence flagged (NaN/warning), not reported as 0% identity', any(math.isnan(v) for v in r_sk.values()), str(r_sk))
Mx = IM.identity_matrix_vectorized(aln); print('  identity matrix diagonal:', np.diag(Mx).round(2).tolist())
check('M3 identity matrix diagonal all 1.0 (self-identity)', np.allclose(np.diag(Mx), 1.0), f'all-gap row diagonal = {Mx[4,4]}; avg-identity formula assumes diagonal 1 -> biased')
# unknown residues in IC / JSD / PSSM
cols_raw = [''.join(c) for c in zip(*rows)]; cols = [''.join(c) for c in zip(*norm)]
ic = [EA.information_content(c, EA.ROBINSON_BACKGROUND) for c in cols_raw]; icr = [ref.ic_ref(c, EA.ROBINSON_BACKGROUND)[0] for c in cols]
print('  IC per col Skill:', [round(x, 2) for x in ic]); print('  IC per col ref  :', [round(x, 2) for x in icr])
check('M4 IC stays <= log2(1/min bg)=6.2 bits with X/B/Z/U/*/lowercase present', max(ic) <= 6.3, f'max Skill IC {max(ic):.1f} bits (reference {max(icr):.1f})')
try:
    ps = PS.pssm_with_pseudocounts(aln)
    print('  PSSM ran; col 3 top:', sorted(ps[3].items(), key=lambda kv: -kv[1])[:3])
except Exception as e:
    print('  PSSM raised', type(e).__name__, e)
js = CS.capra_singh_score(aln); print('  JSD scores:', [round(x, 3) for x in js])
# SP with U / * / lowercase: BLOSUM Array behaviour in Biopython 1.88
BL = substitution_matrices.load('BLOSUM62')
for pair in [('U', 'A'), ('a', 'A'), ('J', 'L'), ('X', 'A'), ('*', 'A'), ('.', 'A')]:
    try: v = BL[pair]; print(f'  BLOSUM62{pair} ->', v)
    except Exception as e: print(f'  BLOSUM62{pair} raises {type(e).__name__}: {e}')
print('  Array has .get ?', hasattr(BL, 'get'), '| alphabet:', BL.alphabet)
sp = ns['sum_of_pairs'](aln); spr, sk = ref.sp_ref(norm, BL)
print(f'  sum_of_pairs Skill {sp} vs reference(normalised, U/J skipped) {spr}; reference skipped pairs {sk}')
check('M5 sum_of_pairs silent on case: lowercase pairs not scored', abs(sp - spr) < 1e-9, f'Skill {sp} vs {spr}  (lowercase/U/./* pairs are dropped without a message)')
# claim in SKILL.md: ".get((c1, c2), 0) on an Array silently always returns 0"
gv = BL.get(('A', 'A'), 0)
check('M6 SKILL claim ".get((c1,c2),0) on Array silently always returns 0" is accurate for Biopython 1.88', gv == 0, f'in 1.88 BL.get((A,A),0) = {gv} (correct score is returned; claim is stale)')
# --- (b) degenerate inputs ---
def try_all(label, rows_):
    write('alignment.fasta', rows_)
    out = {}
    try:
        a = AlignIO.read('alignment.fasta', 'fasta')
    except Exception as e:
        print(f'  [{label}] AlignIO.read -> {type(e).__name__}: {str(e)[:90]}'); return
    ns_, _ = skill_blocks.run_all(verbose=False)
    for nm, fn in [('avg_conservation', lambda: ns_['average_conservation'](a)), ('gap_profile', lambda: ns_['gap_profile'](a)),
                   ('alignment_score', lambda: ns_['alignment_score'](a)), ('sum_of_pairs', lambda: ns_['sum_of_pairs'](a)),
                   ('identity_matrix', lambda: IM.identity_matrix_vectorized(a).tolist()), ('avg_identity_formula', lambda: (IM.identity_matrix_vectorized(a).sum() - len(a)) / (len(a) * (len(a) - 1))),
                   ('capra_singh', lambda: CS.capra_singh_score(a)), ('kimura(0,1)', lambda: KP.kimura_protein_distance(str(a[0].seq), str(a[-1].seq)))]:
        try: out[nm] = fn()
        except Exception as e: out[nm] = f'{type(e).__name__}: {str(e)[:50]}'
    print(f'  [{label}]', out)
try_all('single sequence', ['MKVLAAGVW'])
try_all('two identical', ['MKVLAAGVW', 'MKVLAAGVW'])
try_all('unequal lengths (unaligned FASTA)', ['MKVLAAGVW', 'MKVLAAG'])
try_all('all-gap columns only', ['---', '---'])
# entropy_analysis.py protein/DNA guess on a protein alignment whose first sequence lacks E,F,I,L,P,Q,Y,W
write('alignment.fasta', ['MKVAAGVGDS', 'MKVAAGVGDS', 'MKVCAGVGDT']); a = AlignIO.read('alignment.fasta', 'fasta')
g = any(c in str(a[0].seq).upper() for c in 'EFILPQYW')
print(f'  entropy_analysis.py guesses protein={g} for a valid protein alignment lacking E/F/I/L/P/Q/Y/W in row 0 -> would use DNA_UNIFORM background')
check('M7 alphabet guess on protein seq lacking EFILPQYW', g, 'guess = DNA (IC uses 4-letter uniform bg on protein)')
json.dump({k: v for k, v in RES.items()}, open(os.path.join(HERE, 'results_in7.json'), 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES))
