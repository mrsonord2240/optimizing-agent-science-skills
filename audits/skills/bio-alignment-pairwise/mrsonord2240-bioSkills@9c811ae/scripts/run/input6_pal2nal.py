"""Input 6b: Skill 'Input Checks -> Coding sequences': a CDS with an internal stop (NM_001314043.1) breaks codon-aware tools such as PAL2NAL.
Runs in WSL env alignment. REAL RefSeq CDS. Protein alignment built with the Skill's own protein config; PAL2NAL 14 run on it.
Judge by OUTPUT (pal2nal exits 0 with empty output on inconsistent input)."""
import os, subprocess, sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner, substitution_matrices
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); os.chdir(D)
recs = list(SeqIO.parse('hbb_cds_mammals.fasta', 'fasta'))
def run(a, b, tag):
    pa = PairwiseAligner(mode='global', substitution_matrix=substitution_matrices.load('BLOSUM62'), open_gap_score=-11, extend_gap_score=-1)
    pa_a = str(Seq(str(a.seq)).translate()); pa_b = str(Seq(str(b.seq)).translate())
    A = pa.align(pa_a, pa_b)[0]
    with open(f'pal_{tag}_prot.fa', 'w') as f: f.write(f'>a\n{A[0,:]}\n>b\n{A[1,:]}\n')
    with open(f'pal_{tag}_nuc.fa', 'w') as f: f.write(f'>a\n{a.seq}\n>b\n{b.seq}\n')
    r = subprocess.run(['pal2nal.pl', f'pal_{tag}_prot.fa', f'pal_{tag}_nuc.fa', '-output', 'fasta'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    out = r.stdout
    n = len([l for l in out.splitlines() if l.startswith('>')])
    print(f"{tag}: rc={r.returncode} stdout_bytes={len(out)} records={n} stderr_head={r.stderr.strip()[:110]!r}")
    return n, len(out), r.stderr
human, cow, rabbit = recs[0], recs[2], recs[6]
n1, b1, _ = run(human, cow, 'human_cow')
n2, b2, e2 = run(human, rabbit, 'human_rabbit')
ok1 = n1 == 2 and b1 > 800
ok2 = b2 == 0 or n2 != 2 or 'ERROR' in e2 or 'inconsisten' in e2.lower()
print(('PASS  ' if ok1 else 'FAIL  ') + 'clean human/cow CDS: PAL2NAL emits 2 codon-aligned records', (n1, b1))
print(('PASS  ' if ok2 else 'FAIL  ') + 'rabbit NM_001314043.1 (internal stop): PAL2NAL output empty or error (breaks, as the Skill says)', (n2, b2, e2.strip()[:80]))
print('FAILED:', [] if ok1 and ok2 else 'see above')
