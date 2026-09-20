"""INPUT 8 part 2 assertions (MrBayes 3.2.7 output text for the RNA NEXUS files from i8_mb_prep.py)."""
import os
from common import *
d = DATA/'rna_mb'; os.chdir(d)
rd = lambda f: open(f, encoding='utf-8', errors='replace').read()
t = rd('mb_rna_example.out'); ok("Instead found ''' in command 'Matrix'" in t and 'Analysis completed' not in t, "MrBayes rejects the example's NEXUS for Rfam ids ('AB003409.1/96-167' is Biopython-quoted because of '-'): Instead found ''' (the SKILL's MrBayes paragraph)")
t = rd('mb_rna_recipe.out'); ok('Data is Rna' in t and 'Datatype  = RNA' in t and 'Defining new matrix with 12 taxa and 90 characters' in t, 'MrBayes reads the recipe-sanitised NEXUS as datatype=rna: 12 taxa, 90 characters, "Data is Rna"')
ok('Analysis completed' in t, 'and completes a 200-generation run on it')
summary()
