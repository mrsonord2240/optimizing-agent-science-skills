"""INPUT 7: apply the SKILL's MrBayes id recipe VERBATIM (second python block under 'NEXUS Output Needs a Molecule Type') to the real Pfam 12-taxon alignment
and write the NEXUS MrBayes will read (pf12_recipe.nex); pf12.nex (unsanitised, Biopython-quoted ids) was written by i7_prep.py."""
import os
from Bio import AlignIO
from common import *
d = DATA/'tools'; os.chdir(d)
alignment = AlignIO.read('pf12_relaxed.phy', 'phylip-relaxed')
print('ids before:', [r.id for r in alignment][:3])
ns = {'alignment': alignment}; exec(block('NEXUS Output Needs', 1), ns)
print('ids after :', [r.id for r in alignment][:3])
for r in alignment: r.annotations['molecule_type'] = 'protein'
AlignIO.write(alignment, 'pf12_recipe.nex', 'nexus')
txt = open('pf12_recipe.nex').read(); ok("'" not in txt and 'datatype=protein' in txt, 'pf12_recipe.nex has no quotes and says datatype=protein')
txt0 = open('pf12.nex').read(); ok(txt0.count("'") > 0, f'pf12.nex (no recipe) has quoted ids: {txt0.count(chr(39))} quote chars')
summary()
