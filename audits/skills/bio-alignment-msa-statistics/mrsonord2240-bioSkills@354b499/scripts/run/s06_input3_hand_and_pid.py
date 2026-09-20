"""INPUT 3 (edge, SYNTHETIC tiny alignment with HAND-COMPUTED answers) + INPUT 2b (percent identity vs pwalign::pid on REAL globin pairs).
Prompt 3: "For this 3-sequence protein alignment (with terminal gaps, an internal gap and a gap-only column) give PID1-4 for
seq1 vs seq2, per-column conservation and entropy, gap stats, the simple SP score, BLOSUM62 SP score and Kimura distance."
All expected numbers below were computed BY HAND before running (derivations in eval_viewer)."""
import os, sys, math, shutil, csv
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
os.makedirs(os.path.join(HERE, 'work_in3'), exist_ok=True); os.chdir(os.path.join(HERE, 'work_in3'))
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

# SYNTHETIC alignment, 3 x 8 (+ a 9th all-gap column variant)
S = ['AC-DEF--', '-CGDEFHK', 'ACGN-FHR']
open('data_tiny_synthetic.fasta', 'w').write(''.join(f'>s{i+1}\n{s}\n' for i, s in enumerate(S)))
open('alignment.fasta', 'w').write(''.join(f'>s{i+1}\n{s}\n' for i, s in enumerate(S)))
S9 = [s + '-' for s in S]
open('alignment9.fasta', 'w').write(''.join(f'>s{i+1}\n{s}\n' for i, s in enumerate(S9)))
aln = AlignIO.read('alignment.fasta', 'fasta'); aln9 = AlignIO.read('alignment9.fasta', 'fasta')

import skill_blocks
ns, log = skill_blocks.run_all(verbose=False)
print('SKILL.md blocks:', {i: st for i, _, st, _ in log if st != 'OK' and st != 'SKIPPED_STUB'} or 'all non-stub blocks OK')

print('\n--- HAND-COMPUTED (seq1 AC-DEF-- vs seq2 -CGDEFHK): identical=4 (C,D,E,F); both-residue cols=4; internal gap cols=1 (col3);')
print('    columns with any residue = 8; ungapped lengths 5 and 7.  PID1(Doolittle)=4/5=80%  PID1(Skill def: any residue)=4/8=50%  PID2=100%  PID3=4/5=80%  PID4=4/6=66.7%')
s1, s2 = str(aln[0].seq), str(aln[1].seq)
got = {m: ns['pairwise_identity'](s1, s2, m) for m in ('pid1', 'pid2', 'pid3', 'pid4')}
print('Skill:', {k: round(v * 100, 1) for k, v in got.items()})
check('T1 PID2 = 100%', abs(got['pid2'] - 1.0) < 1e-9, f"{got['pid2']*100:.1f}")
check('T2 PID3 = 80%', abs(got['pid3'] - 0.8) < 1e-9, f"{got['pid3']*100:.1f}")
check('T3 PID4 = 66.7%', abs(got['pid4'] - 4 / 6) < 1e-9, f"{got['pid4']*100:.1f}")
check('T4 PID1 = 80% (paper definition: aligned + INTERNAL gap positions; SKILL.md table says "including internal gaps")',
      abs(got['pid1'] - 0.8) < 1e-9, f"Skill {got['pid1']*100:.1f}% (counts 2 terminal-overhang columns each side)")
rr = ref.pid_ref(s1, s2); print('   ref.pid_ref:', {k: round(v, 4) for k, v in rr.items()})
assert abs(rr['PID1'] - 0.8) < 1e-9   # the reference reproduces the hand value

# conservation / entropy hand values: cons = [1,1,1,2/3,1,1,1,1/2]; H = [0,0,0,.9183,0,0,0,1.0]
cons_hand = [1, 1, 1, 2 / 3, 1, 1, 1, .5]; H_hand = [0, 0, 0, 0.9182958, 0, 0, 0, 1.0]
cons = [ns['column_conservation'](aln, i) for i in range(8)]; ent = [ns['shannon_entropy'](aln[:, i]) for i in range(8)]
check('T5 per-column conservation matches hand values', np.allclose(cons, cons_hand), str([round(c, 3) for c in cons]))
check('T6 per-column entropy matches hand values', np.allclose(ent, H_hand, atol=1e-6), str([round(c, 3) for c in ent]))
avg8 = ns['average_conservation'](aln); avg9 = ns['average_conservation'](aln9)
print(f'   average conservation: 8 cols {avg8:.4f} (hand 7.1667/8 = 0.8958); with one added all-gap column {avg9:.4f} (all-gap col scored 0.0, dilutes mean)')
check('T7 average conservation 0.8958', abs(avg8 - 7.1667 / 8) < 1e-4, f'{avg8:.4f}')
check('T8 all-gap column should not dilute the mean (ignored/NaN)', abs(avg9 - avg8) < 1e-9, f'{avg9:.4f} vs {avg8:.4f}')
gp = ns['gap_profile'](aln)
check('T9 gap profile hand [1/3,0,1/3,0,1/3,0,1/3,1/3] (first hand value 2/3 for col 8 was wrong; recounted)', np.allclose(gp, [1/3, 0, 1/3, 0, 1/3, 0, 1/3, 1/3]), str([round(x, 2) for x in gp]))

# SP scores. hand: simple SP = -12 (8 cols), = -18 with the all-gap col (3 gap/gap pairs x -2); textbook SP ignores gap/gap => -12 both
sp8 = ns['alignment_score'](aln); sp9 = ns['alignment_score'](aln9)
print(f'   alignment_score: 8 cols {sp8} (hand -12), + all-gap col {sp9} (hand textbook: still -12; Skill charges gap/gap pairs)')
check('T10 alignment_score = -12 (hand)', sp8 == -12, str(sp8))
check('T11 all-gap column leaves SP unchanged (gap/gap pairs carry no information)', sp9 == sp8, f'{sp9} vs {sp8}')
bl = ns['sum_of_pairs'](aln)
check('T12 BLOSUM62 sum_of_pairs = 78 (hand: 4+27+6+8+5+18+8+2)', bl == 78, str(bl))
# Kimura for s2 vs s3: both-residue cols 6, identical 4 -> p=1/3, d=-ln(1-1/3-0.2/9)
import kimura_protein_distance as KP
kd = KP.kimura_protein_distance(str(aln[1].seq), str(aln[2].seq)); kh = -math.log(1 - 1/3 - 0.2 / 9)
check('T13 Kimura(s2,s3) = 0.4393 (hand)', abs(kd - kh) < 1e-9 and abs(kd - 0.43933) < 1e-4, f'{kd:.5f}')
import substitution_counts as SC
sc = SC.substitution_counts(aln)
check('T14 substitution counts {D-N:2, K-R:1} (hand)', sc == {('D', 'N'): 2, ('K', 'R'): 1}, str(sc))
# Ti/Tv gate: the protein alignment above contains no A/G/C/T pairs -> transitions=0. Quick DNA-vs-protein gate probe:
import subprocess
out = subprocess.run([sys.executable, '-B', os.path.join(HERE, 'skill', 'examples', 'substitution_counts.py')], capture_output=True, text=True, encoding='utf-8').stdout
print('   substitution_counts.py on this PROTEIN alignment prints:', [l for l in out.splitlines() if 'Ti/Tv' in l or 'Transitions' in l])

# ---- PID vs pwalign::pid on REAL globin pairs (s03_pid_ref.R output) ----
print('\n=== real pairs: Skill PID1-4 vs pwalign::pid (Bioconductor) ===')
rows = list(csv.DictReader(open(os.path.join(HERE, 'data', 'pid_pairs_R.tsv')), delimiter='\t'))
for r in rows:
    a, b = r['a'], r['b']
    if r['name'].endswith('global'):
        A, B = a, b
    else:                       # build the MSA-row view of the pair: overhangs against gaps
        ps, pe, ss, se = int(r['ps']), int(r['pe']), int(r['ss']), int(r['se'])
        pf, sf = r['pfull'], r['sfull']
        pre_p, pre_s, suf_p, suf_s = pf[:ps - 1], sf[:ss - 1], pf[pe:], sf[se:]
        A = pre_p + '-' * len(pre_s) + a + suf_p + '-' * len(suf_s)
        B = '-' * len(pre_p) + pre_s + b + '-' * len(suf_p) + suf_s
        assert A.replace('-', '') == pf and B.replace('-', '') == sf
    sk = {m: ns['pairwise_identity'](A, B, m) * 100 for m in ('pid1', 'pid2', 'pid3', 'pid4')}
    R = {m: float(r[m.upper()]) for m in sk}
    print(f"{r['name']:<28} cols={len(A):3d}  Skill " + ' '.join(f'{m}={sk[m]:.2f}' for m in sk) + '  | R ' + ' '.join(f'{m}={R[m]:.2f}' for m in R))
    for m in ('pid2', 'pid3', 'pid4'):
        check(f"P {r['name']} {m} == pwalign", abs(sk[m] - R[m]) < 0.01, f'{sk[m]:.2f} vs {R[m]:.2f}')
    check(f"P {r['name']} pid1 == pwalign", abs(sk['pid1'] - R['pid1']) < 0.01, f"{sk['pid1']:.2f} vs {R['pid1']:.2f}")

import json
json.dump(RES, open('../results_in3.json', 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'PASS')
