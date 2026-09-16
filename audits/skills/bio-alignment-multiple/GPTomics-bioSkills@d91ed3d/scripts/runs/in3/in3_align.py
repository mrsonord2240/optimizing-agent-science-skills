# Input 3 (edge: strand-unknown Nanopore/Sanger contigs, homology unverified) -- following SKILL.md
# "When NOT to Run MSA": verify homology first; "Beyond MAFFT and MUSCLE": strand-unknown -> mafft --adjustdirection --globalpair
# Env: BLAST+ is not installed here, so the homology gate uses a local Smith-Waterman score vs shuffled controls
# (Biopython PairwiseAligner) in both orientations -- a stand-in for the Skill's 'BLAST E-value < 1e-5' gate.
import random, subprocess
from Bio import SeqIO, AlignIO
from Bio.Align import PairwiseAligner

MAFFT = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\mafft-win\mafft.bat'
recs = list(SeqIO.parse('mixed13.fa', 'fasta'))
al = PairwiseAligner(mode='local', match_score=2, mismatch_score=-3, open_gap_score=-5, extend_gap_score=-2)
rng = random.Random(1)
def best(a, b):
    return max(al.score(a, b), al.score(a, b.reverse_complement()))
ref = recs[0]
print('homology / orientation screen vs', ref.id)
for r in recs[1:]:
    fwd, rev = al.score(ref.seq, r.seq), al.score(ref.seq, r.seq.reverse_complement())
    sh = max(al.score(ref.seq, ''.join(rng.sample(str(r.seq), len(r.seq)))) for _ in range(5))
    status = 'NON-HOMOLOGOUS?' if max(fwd, rev) < 2 * sh else ('reverse strand' if rev > fwd else 'forward')
    print(f'  {r.id:22s} fwd={fwd:7.0f} rev={rev:7.0f} shuffled_max={sh:5.0f} -> {status}')

# strand-aware alignment as the Skill prescribes
with open('mixed_adjdir.fasta', 'w') as out:
    p = subprocess.run([MAFFT, '--adjustdirection', '--globalpair', '--maxiterate', '1000', 'mixed13.fa'],
                       stdout=out, stderr=subprocess.PIPE, text=True)
if p.returncode:
    raise RuntimeError(p.stderr)
aln = AlignIO.read('mixed_adjdir.fasta', 'fasta')
print('reversed by MAFFT:', [r.id for r in aln if r.id.startswith('_R_')])
n, L = len(aln), aln.get_alignment_length()
print(f'{n} x {L}; per-sequence gap fraction:')
for r in aln:
    print(f'  {r.id:24s} {str(r.seq).count("-")/L:.2f}')
