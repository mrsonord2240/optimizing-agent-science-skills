"""INPUT 4 (Variant B, REAL DNA): 6 clean mammalian HBB CDS aligned with MAFFT --auto (default output is LOWERCASE for nucleotides).
Prompt: "Here is my MAFFT nucleotide alignment of beta-globin CDS from six mammals. What is the Ti/Tv ratio, the per-column
conservation and information content (DNA), gap statistics and pairwise identity?"  Run from run/."""
import os, sys, itertools, json, shutil, subprocess
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
import entropy_analysis as EA, pssm as PS, substitution_counts as SC, identity_matrix as IM
import skill_blocks
D = os.path.join(HERE, 'data'); RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

def titv_ref(rows):
    ti = tv = amb = 0
    for c in zip(*rows):
        ch = [x for x in c if x != '-']
        for x, y in itertools.combinations(ch, 2):
            if x == y: continue
            if x not in 'ACGT' or y not in 'ACGT': amb += 1; continue
            if {x, y} in ({'A', 'G'}, {'C', 'T'}): ti += 1
            else: tv += 1
    return ti, tv, amb

lower = os.path.join(D, 'hbb6_mafft_default.fa')
# upper-cased copy = what a user gets with --preservecase or after .upper()
upper = os.path.join(D, 'hbb6_mafft_upper.fa')
with open(upper, 'w') as o:
    for l in open(lower):
        o.write(l if l.startswith('>') else l.upper())
for label, path in (('lower(MAFFT default)', lower), ('upper', upper)):
    wd = os.path.join(HERE, 'work_in4_' + label.split('(')[0]); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd); os.chdir(wd)
    shutil.copy(path, 'alignment.fasta')
    for f in os.listdir(os.path.join(HERE, 'skill', 'examples')): shutil.copy(os.path.join(HERE, 'skill', 'examples', f), '.')
    aln = AlignIO.read('alignment.fasta', 'fasta'); N, L = len(aln), aln.get_alignment_length()
    rows = ref.norm_rows([str(r.seq) for r in aln]); cols = [''.join(c) for c in zip(*rows)]; cols_raw = [''.join(c) for c in zip(*[str(r.seq) for r in aln])]
    alph = ''.join(sorted(set(''.join(str(r.seq) for r in aln))))
    print(f'\n##### {label}: {N} x {L}; alphabet {alph!r}')
    # examples as shipped
    outs = {}
    for f in ('substitution_counts.py', 'entropy_analysis.py', 'identity_matrix.py'):
        outs[f] = subprocess.run([sys.executable, '-B', f], capture_output=True, text=True, encoding='utf-8').stdout
    ti, tv, amb = titv_ref(rows)
    sk_line = [l for l in outs['substitution_counts.py'].splitlines() if l.startswith(('Transitions', 'Transversions', 'Ti/Tv'))]
    print(f'  Ti/Tv reference: ti={ti} tv={tv} ratio={ti/tv:.2f} (ambiguous pairs {amb})   Skill prints: {sk_line}')
    sk_ti = int([l for l in sk_line if l.startswith('Transitions')][0].split(':')[1])
    check(f'D1 {label}: Skill Ti/Tv == reference', sk_ti == ti, f'Skill ti={sk_ti} vs ref {ti}')
    # IC with DNA_UNIFORM
    ic_sk = np.array([EA.information_content(c, EA.DNA_UNIFORM) for c in cols_raw]); ic_rf = np.array([ref.ic_ref(c, EA.DNA_UNIFORM)[0] for c in cols])
    print(f'  DNA IC (uniform bg): Skill max {ic_sk.max():.2f} bits, ref max {ic_rf.max():.2f} (theoretical max 2.00)')
    check(f'D2 {label}: DNA IC within [0,2] bits and == reference', np.abs(ic_sk - ic_rf).max() < 1e-6 and ic_sk.max() <= 2.0001, f'max err {np.abs(ic_sk-ic_rf).max():.2f}')
    # entropy_analysis.py as shipped: what does it print in the header and are values sane?
    hdr = outs['entropy_analysis.py'].splitlines()[2:3]
    print('  entropy_analysis.py says:', hdr, '| first data lines:', outs['entropy_analysis.py'].splitlines()[6:8])
    # PSSM DNA with explicit DNA background (as the pssm.py docstring instructs)
    ps = PS.pssm_with_pseudocounts(aln, background=EA.DNA_UNIFORM); psr = ref.pssm_ref(rows, EA.DNA_UNIFORM)
    pe = max(abs(ps[k][r] - psr[k][r]) for k in range(L) for r in EA.DNA_UNIFORM)
    check(f'D3 {label}: DNA PSSM == reference', pe < 1e-9, f'max err {pe:.2f} log2 units')
    # conservation
    ns, log = skill_blocks.run_all(verbose=False)
    cons = np.array([ns['column_conservation'](aln, k) for k in range(L)]); cref = np.array([ref.conservation_ref(c) for c in cols])
    check(f'D4 {label}: conservation == reference', np.abs(cons - cref).max() < 1e-12, f'avg {cons.mean():.3f}')
    M = IM.identity_matrix_vectorized(aln); iu = np.triu_indices(N, 1)
    pid = [ref.pid_ref(rows[a], rows[b]) for a, b in zip(*iu)]
    print(f'  identity: Skill mean {M[iu].mean()*100:.1f}%  reference PID2 mean {np.mean([p["PID2"] for p in pid])*100:.1f}%  PID4 mean {np.mean([p["PID4"] for p in pid])*100:.1f}%')
    check(f'D5 {label}: sum_of_pairs BLOSUM62 not meaningful for DNA (SKILL says use match/mismatch for DNA)', True, f"alignment_score(match=1, mismatch=-1, gap=-2) = {ns['alignment_score'](aln)}")
    os.chdir(HERE)
json.dump(RES, open(os.path.join(HERE, 'results_in4.json'), 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'PASS')
