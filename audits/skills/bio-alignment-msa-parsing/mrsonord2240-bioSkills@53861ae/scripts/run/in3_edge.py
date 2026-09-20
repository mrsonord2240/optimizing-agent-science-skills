"""Input 3 (Edge, regression of first-audit input 3): 'Some of my alignment files are messy: an HMMER/hhsearch A2M with lowercase
inserts and "." gaps, an alignment with an all-gap column, a single-sequence file, a ragged file and a ColabFold A3M. Give me
match-only columns and a consensus without it blowing up.'
SYNTHETIC inputs (syn_*), hand-known answers. Code = SKILL.md blocks exec'd from the file; a2m_a3m_io.py run from the copy."""
import os, subprocess, sys
import numpy as np
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from common import *
import skillns

ns, log = skillns.load()
def write(name, text):
    p = os.path.join(DATA, name); open(p, 'w', newline='\n').write(text); return p
def aln_of(rows):
    return MultipleSeqAlignment([SeqRecord(Seq(s), id=f's{i}', description='') for i, s in enumerate(rows)])

# ---- all-gap column, single sequence, ragged --------------------------------------------------------------------------------
p = write('syn_gaponly.fasta', '>a\nACD-EG\n>b\nACT-EG\n>c\nACD-EG\n')
g = AlignIO.read(p, 'fasta')
check('all-gap column: consensus keeps "-" in that column (ACDEG with - at col 3), column is not reported conserved, gappy-removal drops it',
      ns['consensus_sequence'](g, 0.5) == 'ACD-EG' and 3 not in [c for c, _, _ in ns['find_conserved_positions'](g, 0.5)] and ns['remove_gappy_columns'](g, 0.5).get_alignment_length() == 5)
check('all-gap column: threshold 1.0 consensus gives the alphabet-aware placeholder in the mixed column (col 2 C,T,D -> X for protein)', ns['consensus_sequence'](g, 1.0) == 'ACX-EG', ns['consensus_sequence'](g, 1.0))
p = write('syn_single.fasta', '>only\nACDE-G\n')
s1 = AlignIO.read(p, 'fasta')
check('single-sequence alignment: consensus == the sequence, gap column kept; all residues "100% conserved" (trivial)',
      ns['consensus_sequence'](s1) == 'ACDE-G' and len(ns['find_conserved_positions'](s1, 1.0)) == 5)
try:
    AlignIO.read(write('syn_unequal.fasta', '>a\nACDEFG\n>b\nACDEF\n'), 'fasta'); rag = None
except ValueError as e:
    rag = str(e)
check('ragged file fails loudly with ValueError (Common Errors row: "Unequal sequence lengths")', rag is not None and 'same length' in rag, rag)

# ---- '.' gaps and lowercase: the first audit's P1 --------------------------------------------------------------------------
p = write('syn_dotgaps.fasta', '>a\nAC..GT\n>b\nAC..GT\n>c\nACDEGT\n>d\nAC..GT\n')
d = AlignIO.read(p, 'fasta')
gpc = ns['gaps_per_column'](d)
print("'.'-gapped FASTA: raw col 2 =", d[:, 2], '| gaps_per_column =', gpc)
check("'.'-gapped input: gaps_per_column == [0,0,3,3,0,0] (hand count; was all zeros)", gpc == [0, 0, 3, 3, 0, 0])
r0 = d[0]
s2a, a2s = ns['coordinate_map'](r0)
check("'.'-gapped input: coordinate_map has 4 residues (was 6) and aln_to_seq is -1 at the two '.' columns", len(s2a) == 4 and list(a2s) == [0, 1, -1, -1, 2, 3], f'{list(s2a)} {list(a2s)}')
check("'.'-gapped input: consensus AC-XGT? -> col 2,3 have 3 gap rows of 4 and 1 residue (25% < 50%) so placeholder X; no '.' emitted",
      ns['consensus_sequence'](d, 0.5) == 'ACXXGT' and '.' not in ns['consensus_sequence'](d, 0.5), ns['consensus_sequence'](d, 0.5))
check("'.'-gapped input: find_gappy_columns(0.5) == [2,3]; remove_gappy_columns leaves 4 columns without '.'", ns['find_gappy_columns'](d, 0.5) == [2, 3] and '.' not in str(ns['remove_gappy_columns'](d, 0.5)[0].seq))
check("'.'-gapped input: filter_by_gap_content counts '.' (rows a,b,d have 2/6 gaps): threshold 0.3 keeps only c", [r.id for r in ns['filter_by_gap_content'](d, 0.3)] == ['c'])
mixed = write('syn_mixedcase_protein.fasta', '>a\nacDEfg\n>b\nACDEFG\n>c\nAcdEFG\n')
m = AlignIO.read(mixed, 'fasta')
check('mixed-case protein: consensus and conserved are case-insensitive (ACDEFG, all 6 columns 100%)', ns['consensus_sequence'](m, 1.0) == 'ACDEFG' and len(ns['find_conserved_positions'](m, 1.0)) == 6)
# normalize_alignment behaviour, incl. upper=False for A2M (lowercase kept, '.' -> '-')
na = ns['normalize_alignment'](d)
nl = ns['normalize_alignment'](AlignIO.read(write('syn_lower_dot.fasta', '>a\nAc.dE\n>b\nACD.E\n'), 'fasta'), upper=False)
check("normalize_alignment: '.' -> '-' and upper-case by default; upper=False keeps case ('Ac-dE')", str(na[0].seq) == 'AC--GT' and str(nl[0].seq) == 'Ac-dE' and str(nl[1].seq) == 'ACD-E')
check('normalize_alignment does not mutate its input (original still has "." and the input object is a different object)', str(d[0].seq) == 'AC..GT' and na is not d)

# ---- A2M / A3M -----------------------------------------------------------------------------------------------------------------
a2m = write('syn_hhsearch.a2m', '>query\nACDE..FGHIK\n>s2\nAC-EwyFGHIK\n>s3\nACDEy.FG-IK\n')
a3m = write('syn_colabfold.a3m', '>query\nACDEFGHIK\n>s2\nAC-EwyFGHIK\n>s3\nACDEyFG-IK\n')
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}
pr = subprocess.run([sys.executable, os.path.join(EX, 'a2m_a3m_io.py'), a2m], cwd=DATA, capture_output=True, text=True, env=env)
print(pr.stdout, pr.stderr[-200:])
check('a2m_a3m_io.py on the hhsearch-style A2M: rc 0, "3 sequences, 11 columns", 9 match columns, inserts query 0 / s2 2 / s3 1 (hand-known)',
      pr.returncode == 0 and '3 sequences, 11 columns' in pr.stdout and '9 match columns' in pr.stdout and 'query: 9 match, 0 inserts' in pr.stdout and 's2: 9 match, 2 inserts' in pr.stdout and 's3: 9 match, 1 inserts' in pr.stdout)
pr2 = subprocess.run([sys.executable, os.path.join(EX, 'a2m_a3m_io.py')], cwd=DATA, capture_output=True, text=True, env=env)
print(pr2.stdout, pr2.stderr[-200:])
check('a2m_a3m_io.py with NO argument runs on the shipped examples/data/example.a2m (ref/hit_1/hit_2: 9 match columns; inserts 0, 2, 1)',
      pr2.returncode == 0 and 'A2M alignment: 3 sequences, 11 columns' in pr2.stdout and '9 match columns' in pr2.stdout and 'hit_1: 9 match, 2 inserts' in pr2.stdout and 'hit_2: 9 match, 1 inserts' in pr2.stdout)
sys.path.insert(0, EX)
import a2m_a3m_io
mo = a2m_a3m_io.match_only_columns(AlignIO.read(a2m, 'fasta'))
check('match_only_columns == hand-known ["ACDEFGHIK","AC-EFGHIK","ACDEFG-IK"]', mo == ['ACDEFGHIK', 'AC-EFGHIK', 'ACDEFG-IK'], str(mo))
try:
    AlignIO.read(a3m, 'fasta'); a3err = None
except ValueError as e:
    a3err = str(e)
check('unpadded A3M through AlignIO fails loudly ("same length"), as SKILL.md warns; user must reformat first', a3err is not None and 'same length' in a3err, a3err)
import pyhmmer
with pyhmmer.easel.MSAFile(a3m, format='a2m') as f:
    padded = f.read()
check('hand-off claim: pyhmmer MSAFile(format="a2m") pads the A3M into a rectangular MSA that gives the same match-only columns',
      a2m_a3m_io.match_only_columns(MultipleSeqAlignment([SeqRecord(Seq(s), id=f'x{i}') for i, s in enumerate(padded.alignment)])) == ['ACDEFGHIK', 'AC-EFGHIK', 'ACDEFG-IK'], str(list(padded.alignment)))

# ---- edge cases beyond the first audit ---------------------------------------------------------------------------------------
# (a) Bio.Align.Alignment (modern) objects: SKILL.md API note says helpers are for AlignIO objects
from Bio import Align
modern = Align.read(os.path.join(DATA, 'syn_gaponly.fasta'), 'fasta')
try:
    ns['gaps_per_column'](modern); e1 = None
except Exception as e:
    e1 = f'{type(e).__name__}: {e}'
print('helper on Bio.Align.Alignment ->', e1)
check('helpers given a modern Bio.Align.Alignment fail loudly with AttributeError (documented API note), not silently', e1 is not None and e1.startswith('AttributeError'), str(e1))
# (b) protein made only of A/C/G/T/N letters is classified as nucleotide by is_nucleotide (heuristic limit; ambiguous= overrides)
pep = MultipleSeqAlignment([SeqRecord(Seq(s), id=f'p{i}') for i, s in enumerate(['GATTACAGG', 'GATTACAGT', 'GCTTACAGG'])])
print('is_nucleotide on a peptide made only of G/A/T/C letters:', ns['is_nucleotide'](pep), '| consensus@1.0:', ns['consensus_sequence'](pep, 1.0), '| forced ambiguous=X:', ns['consensus_sequence'](pep, 1.0, ambiguous='X'))
check('is_nucleotide heuristic limit is real (peptide over A/C/G/T -> True, placeholder N) and ambiguous= overrides it', ns['is_nucleotide'](pep) and ns['consensus_sequence'](pep, 1.0, ambiguous='X') == 'GXTTACAGX')
# (c) weights edge cases
try:
    ns['consensus_sequence'](d, 0.5, weights=[1, 1]); w1 = None
except ValueError as e:
    w1 = str(e)
check('weights of the wrong length raise ValueError', w1 is not None and 'one value per sequence' in w1, w1)
try:
    out = ns['consensus_sequence'](d, 0.5, weights=[0, 0, 0, 0]); w0 = f'returned {out!r}'
except Exception as e:
    w0 = f'{type(e).__name__}: {e}'
print('all-zero weights ->', w0)
check('all-zero weights fail loudly rather than returning a consensus of garbage (ZeroDivisionError or ValueError)', w0.startswith(('ZeroDivisionError', 'ValueError')), w0)
# (d) select_columns with non-string per-column annotation
aa = aln_of(['ACDE', 'ACDF'])
aa.column_annotations['score'] = [0.1, 0.2, 0.3, 0.4]
aa[0].letter_annotations['q'] = [10, 20, 30, 40]
sc = ns['select_columns'](aa, [0, 2])
check('select_columns slices list-valued column and letter annotations (not only strings)', sc.column_annotations['score'] == [0.1, 0.3] and sc[0].letter_annotations['q'] == [10, 30])
summary()
