"""INPUT 2 (variant A, REAL tool output): 8 UniProt globins aligned by MAFFT 7.526, Clustal Omega 1.2.4 and hmmalign
(Pfam globin HMM built with hmmbuild) -> AFA with lowercase inserts + '.' padding; plus the 73-sequence Pfam seed re-aligned by MAFFT.
Prompt: "I aligned the 8 globins to the Pfam globin HMM with hmmalign (and separately with MAFFT). Give me per-column
conservation, entropy, information content, PSSM, identity and the BLOSUM62 sum-of-pairs score."
Data made in the first audit (_first_audit_data_provenance/s01_wsl_make_data.sh); reused unchanged here.
Also: does the SKILL.md normalising import + DistanceCalculator block work on each, and how does the A2M path behave?
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b02_input2_real_tool_outputs.py"""
import os, sys, shutil, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
D = os.path.join(HERE, 'data')
sets = [('mafft_default', 'globins_mafft_default.fa'), ('clustalo', 'globins_clustalo.fa'), ('hmmalign_afa', 'globins_hmmalign.afa'), ('seed_mafft_default', 'seed_mafft_default.fa')]
summ = {}
for tag, fn in sets:
    raw = open(os.path.join(D, fn)).read()
    print(f'\n######## {tag}: {fn}  lowercase letters {sum(c.islower() for l in raw.splitlines() if not l.startswith(">") for c in l)}, dots {sum(l.count(".") for l in raw.splitlines() if not l.startswith(">"))}')
    summ[tag] = B.run_battery(os.path.join(D, fn), 'fasta', 'protein', tag, check=check)
    # SKILL.md blocks verbatim on this alignment
    W = os.path.join(HERE, 'work_b02'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
    shutil.copy(os.path.join(D, fn), os.path.join(W, 'alignment.fasta')); cwd = os.getcwd(); os.chdir(W)
    ns, log = skill_blocks.run_all(verbose=False)
    bad = [(i, st) for i, first, st, out in log if st.startswith('ERROR')]
    check(f'{tag}: all 12 non-stub SKILL.md python blocks run verbatim (incl. DistanceCalculator)', not bad, f'errors {bad}; block0 stderr: {[o for i,f,s,o in log if i==0][0].strip()[:80]!r}')
    aln = ns['alignment']
    from Bio.Phylo.TreeConstruction import DistanceCalculator
    # SKILL.md block outputs vs battery numbers
    sp_block = ns['sum_of_pairs'](aln); asc = ns['alignment_score'](aln)
    check(f'{tag}: SKILL.md sum_of_pairs == reference and alignment_score == textbook (gap/gap 0)', abs(sp_block - summ[tag]['sp_ref']) < 1e-9 and asc == summ[tag]['simple_sp_ref'], f'SP {sp_block} vs {summ[tag]["sp_ref"]}; simple {asc} vs {summ[tag]["simple_sp_ref"]}')
    os.chdir(cwd); shutil.rmtree(W, ignore_errors=True)

# hmmalign result vs the same alignment "as a Pfam-compliant person would tidy it": pre-fix numbers are in the archived report
print('\nhmmalign AFA summary:', summ['hmmalign_afa'])
check('hmmalign AFA: IC max within physical bound (pre-fix 29.35 bits)', summ['hmmalign_afa']['ic_max'] < 6.23, f"{summ['hmmalign_afa']['ic_max']:.3f}")

# ---- A2M route: ragged file, what does the Skill say and what happens ----
from Bio import AlignIO
a2m = os.path.join(D, 'globins_hmmalign.a2m')
try:
    AlignIO.read(a2m, 'fasta'); r = 'read OK'
except Exception as e:
    r = f'{type(e).__name__}: {str(e)[:100]}'
check('A2M from hmmalign (insert columns unpadded, ragged) cannot be read by AlignIO fasta; Skill does not claim it can', True, r)
import msa_utils
al = AlignIO.read(os.path.join(D, 'globins_hmmalign.afa'), 'fasta')
keep = msa_utils.normalize_alignment(al, upper=False)
print('upper=False (documented A2M/A3M path) alphabet:', ''.join(sorted(set(''.join(str(x.seq) for x in keep)))))
import identity_matrix as IM
m = IM.identity_matrix_vectorized(keep, 'pid2'); mu = IM.identity_matrix_vectorized(msa_utils.normalize_alignment(al), 'pid2')
print(f'   upper=False mean PID2 {IM.average_identity(m)[0]*100:.2f}%  vs upper-cased {IM.average_identity(mu)[0]*100:.2f}%')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b02.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
