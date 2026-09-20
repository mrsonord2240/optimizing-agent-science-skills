"""Input 8 (NEW, real data not used by the fixer): distant protein pair PKA catalytic subunit (1ATP chain E, 350 aa) vs CDK2 (1HCK chain A),
PDB SEQRES from audit-envs public-data. Question: 'align these two kinases, score with BLOSUM62 and tell me if the alignment means anything'.
Verifies the Skill's NEW gap-convention section on a pair it was never tuned on: Biopython -12/-1 == BLASTP 11/1, -11/-1 == EMBOSS 11/1, plus BLOSUM choice,
percent identity, 'when NOT appropriate' identity bands and the empirical p-value. Ground truth: own Gotoh DP + EMBOSS + BLAST+ (WSL, input8_ground_truth.sh) + pwalign (R)."""
import math, sys
from common import *
from ref_gotoh import load_matrix, gotoh_score
import empirical_pvalue_copy as ep
STR = r'F:\OpenScience\audit-envs\alignment\public-data\structures'
recs = {}
for pdb in ('1ATP', '1HCK'):
    for r in SeqIO.parse(STR + chr(92) + pdb + '.pdb', 'pdb-seqres'):
        recs.setdefault(pdb, r)
pka, cdk = recs['1ATP'], recs['1HCK']
print(pka.id, len(pka.seq), cdk.id, len(cdk.seq))
SeqIO.write([pka, cdk], r'F:\OpenScience\audits\bio-alignment-pairwise\run\data\kin.fasta', 'fasta')
B62 = substitution_matrices.load('BLOSUM62'); Bd = load_matrix('BLOSUM62')
def al(mode, o, e, m=B62): return PairwiseAligner(mode=mode, substitution_matrix=m, open_gap_score=-o, extend_gap_score=-e)
res = {}
for mode, o, e in [('global', 11, 1), ('global', 10, 0.5), ('local', 11, 1), ('local', 12, 1), ('global', 12, 1)]:
    A = al(mode, o, e).align(pka.seq, cdk.seq)[0]
    ref = gotoh_score(str(pka.seq), str(cdk.seq), Bd, o, e, mode)
    check(f"{mode} -{o}/-{e}: Biopython == independent Gotoh", abs(A.score - ref) < 1e-9, (A.score, ref))
    res[(mode, o, e)] = A
    if mode == 'local': print(f"   local {o}/{e}: score {A.score} q {A.aligned[0][0][0]+1}-{A.aligned[0][-1][1]}  s {A.aligned[1][0][0]+1}-{A.aligned[1][-1][1]}")
import json
json.dump({f'{k[0]}_{k[1]}_{k[2]}': float(v.score) for k, v in res.items()} | {'loc12_coords': [int(res[('local', 12, 1)].aligned[0][0][0]) + 1, int(res[('local', 12, 1)].aligned[0][-1][1]), int(res[('local', 12, 1)].aligned[1][0][0]) + 1, int(res[('local', 12, 1)].aligned[1][-1][1])]}, open(r'F:\OpenScience\audits\bio-alignment-pairwise\run\data\kin_biopython.json', 'w'))
# BLOSUM choice on a distant pair (Skill: distant -> BLOSUM45/50; check the ranking of alignments by identity of homologous core is not the point; just record scores + counts)
for nm in ('BLOSUM45', 'BLOSUM62', 'BLOSUM80'):
    A = PairwiseAligner(mode='local', substitution_matrix=substitution_matrices.load(nm), open_gap_score=-12, extend_gap_score=-1).align(pka.seq, cdk.seq)[0]
    c = A.counts(); print(f"   {nm} local: score {A.score} aligned residues {c.identities + c.mismatches} identities {c.identities}")
# identity: global PID
G = res[('global', 11, 1)]; c = G.counts(); pid2 = 100 * c.identities / (c.identities + c.mismatches); print(f"global pid2 {pid2:.1f}%  gaps {c.gaps}")
check("Skill band: 25-40% identity -> 'use sensitive iterative methods' (real pair sits in or near this band: 25 <= pid2 <= 45)", 25 <= pid2 <= 45, round(pid2, 1))
# significance with the Skill's example script (local, BLASTP-equivalent params -12/-1, i.e. the Skill's own recommended BLASTP config)
loc = al('local', 12, 1)
obs, p, null = ep.empirical_pvalue(str(pka.seq), str(cdk.seq), loc, n_shuffles=1000, seed=42)
bits = (0.267 * obs - math.log(0.041)) / math.log(2)
print(f"local raw {obs} K-A bits {bits:.1f} empirical p {p:.4f}")
check("Skill: bit score > 50 = 'likely homology'; true homologs (PKA/CDK2, same fold) reach empirical p at the floor", bits > 50 and p < 0.01, (round(bits, 1), p))
summary()
