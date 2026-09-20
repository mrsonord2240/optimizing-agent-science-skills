"""INPUT 2 (Variant A, REAL tool output): alignments as real users get them - MAFFT (upper), hmmalign A2M/AFA (lowercase inserts),
Pfam seed as raw Stockholm/pyhmmer text ('.' gaps). Skill functions vs reference on the case/gap-normalised alignment.
Prompt: "I aligned the 8 globins to the Pfam globin HMM with hmmalign (and separately with MAFFT). Give me per-column conservation,
entropy, information content, PSSM, identity and the BLOSUM62 sum-of-pairs score." Run from run/."""
import os, sys, itertools, json, shutil
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
from Bio.Align import substitution_matrices
import entropy_analysis as EA, pssm as PS, identity_matrix as IM, capra_singh_jsd as CS
import skill_blocks

# real Stockholm text with '.' gaps -> FASTA keeping '.' (what pyhmmer / esl-reformat-free parsing yields)
import pyhmmer
from pyhmmer.easel import MSAFile
with MSAFile(os.path.join(HERE, 'data', 'PF00042_seed.sto')) as f:
    m = f.read()
with open(os.path.join(HERE, 'data', 'seed_dot.fasta'), 'w') as o:
    for name, seq in zip(m.names, m.alignment):
        o.write('>' + str(name).replace('/', '_') + '\n' + seq + '\n')

BL = substitution_matrices.load('BLOSUM62')
OUT = {}

def evaluate(fasta, label, fmt='fasta'):
    wd = os.path.join(HERE, 'work_in2_' + label); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd); os.chdir(wd)
    shutil.copy(fasta, 'alignment.fasta')
    ns, log = skill_blocks.run_all(verbose=False)
    aln = AlignIO.read('alignment.fasta', fmt)
    raw_rows = [str(r.seq) for r in aln]; rows = ref.norm_rows(raw_rows)
    N, L = len(rows), len(rows[0])
    chars = ''.join(sorted(set(''.join(raw_rows))))
    cols_raw = [''.join(c) for c in zip(*raw_rows)]; cols = [''.join(c) for c in zip(*rows)]
    R = dict(label=label, N=N, L=L, alphabet=chars)
    print(f'\n##### {label}: {N} x {L}; alphabet in file: {chars!r}; lowercase={sum(c.islower() for c in "".join(raw_rows))}, dots={"".join(raw_rows).count(".")}')
    cons = np.array([ns['column_conservation'](aln, k) for k in range(L)]); cref = np.array([ref.conservation_ref(c) for c in cols])
    ent = np.array([EA.shannon_entropy(c) for c in cols_raw]); eref = np.array([ref.entropy_ref(c) for c in cols])
    ic = np.array([EA.information_content(c, EA.ROBINSON_BACKGROUND) for c in cols_raw])
    icr = np.array([ref.ic_ref(c, EA.ROBINSON_BACKGROUND)[0] for c in cols])
    js = np.array(CS.capra_singh_score(aln))
    gp = np.array(ns['gap_profile'](aln)); gpr = np.array([c.count('-') / N for c in cols])
    R['cons_maxerr'] = float(np.abs(cons - cref).max()); R['cons_ncols_wrong'] = int((np.abs(cons - cref) > 1e-9).sum())
    R['ent_maxerr'] = float(np.abs(ent - eref).max()); R['ic_maxerr'] = float(np.abs(ic - icr).max()); R['ic_max_skill'] = float(ic.max()); R['ic_max_ref'] = float(icr.max())
    R['gap_ncols_wrong'] = int((np.abs(gp - gpr) > 1e-9).sum())
    print(f'  conservation: {R["cons_ncols_wrong"]}/{L} columns differ from reference, max err {R["cons_maxerr"]:.3f}; avg Skill {cons.mean():.3f} vs ref {cref.mean():.3f}')
    print(f'  entropy: max err {R["ent_maxerr"]:.3f} bits; IC: max err {R["ic_maxerr"]:.2f} bits (Skill max IC {ic.max():.2f} vs ref {icr.max():.2f}; log2(20)=4.32 is the ceiling for a real KL over 20 aa with rare aa <=~6.2)')
    print(f'  gap profile: {R["gap_ncols_wrong"]}/{L} columns differ')
    # PSSM
    ps = PS.pssm_with_pseudocounts(aln); psr = ref.pssm_ref(rows, PS.ROBINSON_BACKGROUND)
    R['pssm_maxerr'] = float(max(abs(ps[k][r] - psr[k][r]) for k in range(L) for r in PS.ROBINSON_BACKGROUND))
    print(f'  PSSM max |Skill - ref| = {R["pssm_maxerr"]:.2f} log2 units')
    # SP
    sp = ns['sum_of_pairs'](aln); spr, skipped = ref.sp_ref(rows, BL)
    R['sp_skill'] = float(sp); R['sp_ref'] = float(spr)
    print(f'  BLOSUM62 sum_of_pairs: Skill {sp} vs ref {spr}')
    # identity
    M = IM.identity_matrix_vectorized(aln)
    Mr = np.array([[ (ref.pid_ref(rows[a], rows[b])['PID1'] if a != b else 1.0) for b in range(N)] for a in range(N)])
    # reference for Skill-definition PID1 ("any residue" denominator) on normalised rows
    def skill_def(a, b):
        A_ = np.array(list(a)); B_ = np.array(list(b)); den = ((A_ != '-') | (B_ != '-')).sum(); mt = ((A_ == B_) & (A_ != '-')).sum()
        return mt / den if den else 0
    Ms = np.array([[skill_def(rows[a], rows[b]) if a != b else 1.0 for b in range(N)] for a in range(N)])
    iu = np.triu_indices(N, 1)
    R['pid_maxerr'] = float(np.abs(M - Ms)[iu].max()); R['pid_meanerr'] = float(np.abs(M - Ms)[iu].mean())
    print(f'  identity matrix (Skill def) vs same def on normalised rows: max err {100*R["pid_maxerr"]:.2f} pts, mean err {100*R["pid_meanerr"]:.2f} pts; mean pair identity Skill {100*M[iu].mean():.1f}% vs {100*Ms[iu].mean():.1f}%')
    print('  SKILL.md block status:', {i: st[:60] for i, _, st, _ in log if st not in ('OK', 'SKIPPED_STUB')} or 'all OK')
    OUT[label] = R
    os.chdir(HERE)

D = os.path.join(HERE, 'data')
evaluate(os.path.join(D, 'globins_mafft_default.fa'), 'mafft_upper')
evaluate(os.path.join(D, 'globins_clustalo.fa'), 'clustalo_upper')
evaluate(os.path.join(D, 'globins_hmmalign.afa'), 'hmmalign_afa_lowercase_inserts')
evaluate(os.path.join(D, 'seed_dot.fasta'), 'pfam_seed_dot_gaps')
json.dump(OUT, open(os.path.join(HERE, 'results_in2.json'), 'w'), indent=1)
