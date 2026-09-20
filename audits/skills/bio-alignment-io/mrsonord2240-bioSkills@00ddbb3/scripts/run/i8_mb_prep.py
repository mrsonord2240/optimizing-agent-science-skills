"""INPUT 8 part 2: does the datatype the example INFERS for RNA (datatype=rna) load in MrBayes 3.2.7? REAL Rfam RF00005 tRNA, first 12 sequences (ids like 'AB031211.1/8-80').
Path A: shipped convert_formats.py output.nex as written. Path B: after the SKILL's id-sanitising recipe (verbatim block). Files are consumed by i8_mb.sh, judged by i8_mb_check.py."""
import os, re, shutil, subprocess, sys
from Bio import AlignIO
from common import *
d = DATA/'rna_mb'; shutil.rmtree(d, ignore_errors=True); d.mkdir(); os.chdir(d)
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
rfam = AlignIO.read(DATA/'rfam_RF00005.sto', 'stockholm')[:12]
# drop columns that are all gaps in the 12-row subset so MrBayes sees no empty sites
keep = [i for i in range(rfam.get_alignment_length()) if set(rfam[:, i]) - set('-.')]
sub = rfam[:, keep[0]:keep[0] + 1]
for i in keep[1:]: sub = sub + rfam[:, i:i+1]
print('subset', len(sub), 'x', sub.get_alignment_length(), '| ids', [r.id for r in sub][:3])
AlignIO.write(sub, 'rna12.aln', 'clustal')
w = d/'ex'; shutil.copytree(SKILL/'examples', w); shutil.copy('rna12.aln', w/'rna12.aln')
r = subprocess.run([sys.executable, 'convert_formats.py', 'rna12.aln'], cwd=w, capture_output=True, text=True, env=env, encoding='utf-8'); print(r.stdout.strip(), r.stderr.strip()[-200:])
ok('Molecule type: RNA' in r.stdout and 'datatype=rna' in r.stdout, 'example infers RNA for the real Rfam subset and writes datatype=rna')
shutil.copy(w/'output.nex', 'rna_example.nex'); print('quote chars in example NEXUS:', open('rna_example.nex').read().count("'"))
a = AlignIO.read('rna12.aln', 'clustal'); ns = {'alignment': a}; exec(block('NEXUS Output Needs', 1), ns)
for x in a: x.annotations['molecule_type'] = 'RNA'
AlignIO.write(a, 'rna_recipe.nex', 'nexus'); print('ids after recipe', [x.id for x in a][:3])
ok(all(re.fullmatch(r'[A-Za-z0-9_]+', x.id) for x in a) and len({x.id for x in a}) == 12, 'recipe ids are [A-Za-z0-9_]+ and unique')
summary()
