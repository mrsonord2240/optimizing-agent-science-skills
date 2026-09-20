"""INPUT 5c: PAML route on 6 REAL HBB CDS (MAFFT alignment). Writes phylip-sequential AND phylip-relaxed with AlignIO, then run_codeml.sh runs M0 on both."""
import os, sys, re, shutil
from Bio import AlignIO
from common import *
d = DATA/'tools'; os.chdir(d)
aln = AlignIO.read('hbb6_aln.fa', 'fasta'); L = aln.get_alignment_length(); print(len(aln), 'x', L, 'multiple of 3:', L % 3 == 0)
tree = '((human,chimp),macaque,((cow,pig),horse));'
for tag, fmt in [('seq', 'phylip-sequential'), ('rel', 'phylip-relaxed')]:
    w = d/f'codeml_{tag}'; shutil.rmtree(w, ignore_errors=True); w.mkdir()
    AlignIO.write(aln, w/'aln.phy', fmt); (w/'tree.nwk').write_text(tree + '\n')
    (w/'codeml.ctl').write_text('seqfile = aln.phy\ntreefile = tree.nwk\noutfile = mlc\nnoisy = 0\nverbose = 0\nrunmode = 0\nseqtype = 1\nCodonFreq = 2\nmodel = 0\nNSsites = 0\nicode = 0\nfix_kappa = 0\nkappa = 2\nfix_omega = 0\nomega = 0.4\ncleandata = 0\n', encoding='utf-8')
    print(tag, open(w/'aln.phy').read()[:100].replace('\n', ' | '))
