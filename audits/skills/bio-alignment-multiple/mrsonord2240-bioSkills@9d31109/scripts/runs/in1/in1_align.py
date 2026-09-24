# Input 1 (canonical) -- code written by following bio-alignment-multiple SKILL.md
# Env adaptation (Windows): the MAFFT launcher is 'mafft.bat'; everything else is the Skill's pattern verbatim.
import itertools, subprocess
from Bio import AlignIO

MAFFT = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\mafft-win\mafft.bat'

def run_mafft(input_fasta, output_fasta, algorithm='linsi', threads=4):          # SKILL.md "Basic Usage"
    algo_flags = {
        'linsi': ['--localpair', '--maxiterate', '1000'],
        'ginsi': ['--globalpair', '--maxiterate', '1000'],
        'einsi': ['--genafpair', '--maxiterate', '1000'],
        'fftns2': ['--retree', '2'],
        'auto': ['--auto'],
    }
    cmd = [MAFFT, '--thread', str(threads)] + algo_flags[algorithm] + [input_fasta]
    with open(output_fasta, 'w') as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'MAFFT failed (exit {result.returncode}):\n{result.stderr}')

# <200 sequences, single gene family -> MAFFT L-INS-i (Default recommendation)
run_mafft('prot15_unaligned.fa', 'prot15_linsi.fasta', algorithm='linsi')
# Cross-aligner sensitivity check: MUSCLE5 -align (PPP)
subprocess.run(['muscle', '-align', 'prot15_unaligned.fa', '-output', 'prot15_muscle.afa', '-threads', '4'],
               check=True, capture_output=True)
# MUSCLE5 stratified ensemble for per-column confidence (Confidence Assessment table)
subprocess.run(['muscle', '-align', 'prot15_unaligned.fa', '-stratified', '-output', 'prot15_ens.efa'],
               check=True, capture_output=True)

# Post-Alignment Validation Checklist
aln = AlignIO.read('prot15_linsi.fasta', 'fasta')
n, L = len(aln), aln.get_alignment_length()
gappy_cols = sum(1 for i in range(L) if aln[:, i].count('-') / n > 0.5)
cols_with_gaps = sum(1 for i in range(L) if '-' in aln[:, i])
print(f'MAFFT L-INS-i: {n} sequences x {L} columns')
print(f'columns with any gap: {cols_with_gaps} ({cols_with_gaps/L:.1%}); columns >50% gaps: {gappy_cols} ({gappy_cols/L:.1%})')
def pid2(a, b):
    m = sum(x == y and x != '-' for x, y in zip(a, b)); d = sum(x != '-' and y != '-' for x, y in zip(a, b))
    return m / d if d else 0
pids = {}
for r1, r2 in itertools.combinations(aln, 2):
    pids[(r1.id, r2.id)] = pid2(str(r1.seq), str(r2.seq))
mean_pid = sum(pids.values()) / len(pids)
print(f'mean pairwise identity (PID2): {mean_pid:.1%}  min: {min(pids.values()):.1%}  max: {max(pids.values()):.1%}')
print('checklist item 3 (<25% protein identity -> questionable):', 'FLAG' if mean_pid < 0.25 else 'ok')
gaps = {r.id: str(r.seq).count('-') for r in aln}
med = sorted(gaps.values())[n // 2]
print('per-sequence gaps:', ', '.join(f'{k}:{v}' for k, v in gaps.items()))
out = [k for k, v in gaps.items() if v > 2 * med + 10]
print('outlier (gap-heavy) sequences:', out or 'none')
