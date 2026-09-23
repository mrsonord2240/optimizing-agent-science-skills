"""Input 6c: realistic route for the Skill's coding-sequence advice: translate, align the PROTEINS with MAFFT (the Skill's multiple-alignment
neighbour), back-translate with PAL2NAL. Does a CDS with an internal stop (rabbit NM_001314043.1) break it? REAL RefSeq CDS, WSL env alignment.
Judge by output: record count / bytes of pal2nal stdout."""
import os, subprocess
from Bio import SeqIO
from Bio.Seq import Seq
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); os.chdir(D)
recs = list(SeqIO.parse('hbb_cds_mammals.fasta', 'fasta'))
sel = [recs[0], recs[2], recs[6]]
names = ['human', 'cow', 'rabbit']
with open('pm_nuc.fa', 'w') as f:
    for n, r in zip(names, sel): f.write(f'>{n}\n{r.seq}\n')
with open('pm_prot.fa', 'w') as f:
    for n, r in zip(names, sel): f.write(f'>{n}\n{Seq(str(r.seq)).translate()}\n')
print("proteins with '*':", [(n, str(Seq(str(r.seq)).translate()).count('*')) for n, r in zip(names, sel)])
m = subprocess.run(['mafft', '--quiet', '--auto', 'pm_prot.fa'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
open('pm_prot_aln.fa', 'w').write(m.stdout)
print("mafft rc", m.returncode, "bytes", len(m.stdout), "| stderr", m.stderr.strip()[:100])
aln = {r.id: str(r.seq) for r in SeqIO.parse('pm_prot_aln.fa', 'fasta')}
print("stars after mafft:", {k: v.count('*') for k, v in aln.items()}, "| aln len", len(next(iter(aln.values()))) if aln else None)
p = subprocess.run(['pal2nal.pl', 'pm_prot_aln.fa', 'pm_nuc.fa', '-output', 'fasta'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
n = sum(1 for l in p.stdout.splitlines() if l.startswith('>'))
print(f"pal2nal (3 seqs incl. rabbit): rc={p.returncode} bytes={len(p.stdout)} records={n} stderr={(p.stderr or p.stdout[:0]).strip()[:150]!r}")
# with stops replaced by X in the protein alignment (common practice)
open('pm_prot_aln_X.fa', 'w').write(open('pm_prot_aln.fa').read().replace('*', 'X'))
p2 = subprocess.run(['pal2nal.pl', 'pm_prot_aln_X.fa', 'pm_nuc.fa', '-output', 'fasta'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
n2 = sum(1 for l in p2.stdout.splitlines() if l.startswith('>'))
print(f"pal2nal (stop->X): rc={p2.returncode} bytes={len(p2.stdout)} records={n2} stderr={p2.stderr.strip()[:150]!r}")
# clean pair for control
sel2 = [recs[0], recs[2]]
with open('pm_nuc2.fa', 'w') as f:
    for n_, r in zip(names, sel2): f.write(f'>{n_}\n{r.seq}\n')
a2 = '\n'.join(f'>{k}\n{v}' for k, v in aln.items() if k in ('human', 'cow'))
open('pm_prot_aln2.fa', 'w').write(a2 + '\n')
p3 = subprocess.run(['pal2nal.pl', 'pm_prot_aln2.fa', 'pm_nuc2.fa', '-output', 'fasta'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
n3 = sum(1 for l in p3.stdout.splitlines() if l.startswith('>'))
print(f"pal2nal control (human+cow only, rabbit removed): rc={p3.returncode} bytes={len(p3.stdout)} records={n3}")
print(('PASS  ' if n3 == 2 else 'FAIL  ') + 'control emits 2 records')
print('RABBIT-ROUTE RESULT: records emitted with rabbit (mafft route) =', n, '; stop->X route =', n2)
