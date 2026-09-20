"""INPUT 4 (variant B, REAL DNA): six mammalian HBB CDS aligned by MAFFT 7.526 - default output is LOWER case.
Prompt: "Here is my MAFFT nucleotide alignment of beta-globin CDS from six mammals. What is the Ti/Tv ratio, the per-column
conservation and information content (DNA), gap statistics and pairwise identity?"
Pre-fix: Ti/Tv 0.00 (ref 428/355=1.21), DNA IC up to 29.9 bits (max 2.0).
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b04_input4_dna_mafft.py"""
import os, sys, shutil, json, subprocess, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks, numpy as np
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
D = os.path.join(HERE, 'data')
out = {}
for tag, fn in [('hbb6_lower', 'hbb6_mafft_default.fa'), ('hbb6_upper', 'hbb6_mafft_upper.fa')]:
    raw = open(os.path.join(D, fn)).read()
    low = sum(c.islower() for l in raw.splitlines() if not l.startswith('>') for c in l)
    print(f'\n######## {tag}: {fn} lowercase letters {low}')
    out[tag] = B.run_battery(os.path.join(D, fn), 'fasta', 'dna', tag, check=check)
    print('   ', out[tag])
check('lower == upper: Ti/Tv, IC max, mean PID1 identical for the two case conventions',
      out['hbb6_lower']['titv'] == out['hbb6_upper']['titv'] and abs(out['hbb6_lower']['ic_max'] - out['hbb6_upper']['ic_max']) < 1e-15 and abs(out['hbb6_lower']['avg_pid1'] - out['hbb6_upper']['avg_pid1']) < 1e-15, f"{out['hbb6_lower']['titv']}")
check('Ti/Tv == 428 / 355 = 1.21 (first-audit independent count)', out['hbb6_lower']['titv'][:2] == (428, 355), str(out['hbb6_lower']['titv']))
check('DNA IC max == 2.000 bits (pre-fix 29.90)', abs(out['hbb6_lower']['ic_max'] - 2.0) < 1e-9, f"{out['hbb6_lower']['ic_max']:.4f}")
# shipped CLI text on the lowercase file: the number a user reads
p = subprocess.run([sys.executable, '-B', 'substitution_counts.py', os.path.join(D, 'hbb6_mafft_default.fa')], cwd=B.EX, capture_output=True, text=True, encoding='utf-8')
print(p.stdout[-330:])
check('substitution_counts.py prints "Ti/Tv ratio: 1.21" on the lower-case MAFFT file', 'Ti/Tv ratio: 1.21' in p.stdout and 'Transitions: 428' in p.stdout, '')
p = subprocess.run([sys.executable, '-B', 'entropy_analysis.py', os.path.join(D, 'hbb6_mafft_default.fa')], cwd=B.EX, capture_output=True, text=True, encoding='utf-8')
check('entropy_analysis.py says DNA (uniform background) and max entropy 2.000', 'Treating as DNA' in p.stdout and 'Maximum possible entropy: 2.000' in p.stdout, p.stdout.splitlines()[1])
# SKILL.md blocks (protein-flavoured) on the DNA alignment: run verbatim, use DNA_UNIFORM for IC
W = os.path.join(HERE, 'work_b04'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(os.path.join(D, 'hbb6_mafft_default.fa'), os.path.join(W, 'alignment.fasta')); cwd = os.getcwd(); os.chdir(W)
ns, log = skill_blocks.run_all(verbose=False)
errs = [(i, st) for i, f, st, o in log if st.startswith('ERROR')]
print('blocks erroring on DNA input:', errs)
aln = ns['alignment']
ic = [ns['information_content'](aln[:, i], ns['DNA_UNIFORM']) for i in range(aln.get_alignment_length())]
check('SKILL.md information_content(col, DNA_UNIFORM) on lowercase MAFFT DNA <= 2 bits', max(ic) <= 2.0 + 1e-9 and abs(max(ic) - 2.0) < 1e-9, f'max {max(ic):.3f}')
# DistanceCalculator block uses blosum62 on DNA -> expected to be the wrong model; record what happens
blk = [l for l in log if l[0] == 16][0]
print('DistanceCalculator(blosum62) block on DNA:', blk[2][:100])
os.chdir(cwd); shutil.rmtree(W, ignore_errors=True)
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b04.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
