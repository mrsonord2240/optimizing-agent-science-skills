"""SYNTHETIC data for the bio-phylo-tree-manipulation audit (2026-09-15).

All trees are invented; alignments are simulated with IQ-TREE 2.4.0 AliSim from
the known rooted trees below, then an unrooted ML tree is inferred so that
rooting methods can be scored against the TRUE root.

D1  og16   : 14 ingroup + 2 close outgroups (OutA, OutB); one fast ingroup tip (Fast8).
             True root = split {OutA,OutB} | ingroup.  3000 bp GTR+G4.
D2  deep20 : 20 taxa, no outgroup, strong lineage-specific rate shift (clade Y 4x
             faster + one very long tip).  True root = split X | Y.
             Simulated under a NON-REVERSIBLE model (UNREST) so IQ-TREE root tests
             have directional signal.  6000 bp.
D3  far15  : same 14-taxon ingroup + ONE distant outgroup (FarOut, branch 1.8);
             Fast8 has a long tip.  True root = split FarOut | ingroup. 800 bp.
"""
import subprocess, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IQ = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe'

ING = ('((((I1:0.04,I2:0.05):0.03,(I3:0.04,I4:0.05):0.03):0.04,'
       '((I5:0.05,I6:0.04):0.03,(I7:0.05,Fast8:0.55):0.03):0.04):0.05,'
       '(((I9:0.04,I10:0.05):0.03,I11:0.07):0.04,(I12:0.06,(I13:0.04,I14:0.05):0.03):0.04):0.05)')

TREES = {
    'og16': f'((OutA:0.08,OutB:0.09):0.12,{ING}:0.12);',
    'far15': f'(FarOut:1.8,{ING}:0.05);',
    'deep20': ('((((X1:0.10,X2:0.12):0.08,(X3:0.11,X4:0.09):0.08):0.10,'
               '((X5:0.10,X6:0.12):0.07,(X7:0.09,(X8:0.11,X9:0.10):0.06):0.07):0.10):0.25,'
               '((((Y1:0.40,Y2:0.45):0.30,(Y3:0.42,Y4:0.38):0.30):0.35,'
               '((Y5:0.44,Y6:0.40):0.28,(Y7:0.41,(Y8:0.39,Y9:0.43):0.25):0.30):0.35):0.40,'
               'Y10:2.20):0.25);'),
}
SIM = {
    'og16': ('GTR{1.2,3.5,0.9,1.1,4.2}+F{0.3,0.2,0.2,0.3}+G4{0.6}', 3000),
    'far15': ('GTR{1.2,3.5,0.9,1.1,4.2}+F{0.3,0.2,0.2,0.3}+G4{0.6}', 800),
    'deep20': ('UNREST{0.5,2.5,0.4,0.6,0.8,2.2,1.4,0.3,2.8,0.7,0.5}+G4{0.8}', 6000),
}


def run(cmd):
    print('>>', ' '.join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        sys.exit(r.returncode)


for name, nwk in TREES.items():
    with open(os.path.join(HERE, f'{name}_true.nwk'), 'w', encoding='utf-8') as fh:
        fh.write(nwk + '\n')
    model, length = SIM[name]
    run([IQ, '--alisim', f'{name}_aln', '-t', f'{name}_true.nwk', '-m', model,
         '--length', str(length), '--seed', '20260915', '-af', 'fasta', '-redo'])
    # unrooted ML inference with dual support labels (SH-aLRT/UFBoot)
    run([IQ, '-s', f'{name}_aln.fa', '-m', 'MFP', '-B', '1000', '-alrt', '1000',
         '-T', '4', '--seed', '12345', '--prefix', f'{name}_ml', '-redo', '-quiet'])
print('done')
