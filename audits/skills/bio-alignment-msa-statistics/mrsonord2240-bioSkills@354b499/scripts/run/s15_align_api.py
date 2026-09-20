"""Frontmatter says primary_tool: Bio.Align, but every snippet uses Bio.AlignIO + MultipleSeqAlignment methods.
Probe: do the Skill's functions work when the user (per alignment-io Skill) reads with the modern Bio.Align.read?"""
import sys, warnings, os
sys.dont_write_bytecode = True
warnings.simplefilter('always')
sys.path.insert(0, 'skill/examples')
from Bio import Align, AlignIO
import skill_blocks
os.makedirs('work_in8', exist_ok=True); os.chdir('work_in8')
import shutil; shutil.copy('../data/seed_norm.fasta', 'alignment.fasta')
ns, log = skill_blocks.run_all(verbose=False)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); old = AlignIO.read('alignment.fasta', 'fasta')
    print('AlignIO.read warnings:', [str(x.message)[:100] for x in w] or 'none')
new = Align.read('alignment.fasta', 'fasta')
print('modern Alignment:', type(new).__name__, 'len', len(new), 'shape', new.shape)
for nm, fn in [('get_alignment_length', lambda: new.get_alignment_length()),
               ('column_conservation', lambda: ns['column_conservation'](new, 3)),
               ('gap_profile', lambda: ns['gap_profile'](new)[:2]),
               ('sum_of_pairs', lambda: ns['sum_of_pairs'](new)),
               ('pairwise_identity(rows)', lambda: ns['pairwise_identity'](str(new[0]), str(new[1]), 'pid2')),
               ('new[:,3]', lambda: new[:, 3])]:
    try: print(f'  {nm}:', repr(fn())[:90])
    except Exception as e: print(f'  {nm}: {type(e).__name__}: {str(e)[:90]}')
# what does str(new[0]) give? (row of an Alignment is the aligned sequence with gaps?)
print('  str(new[0])[:40]:', str(new[0])[:40], '| new[0].__class__:', type(new[0]).__name__)
