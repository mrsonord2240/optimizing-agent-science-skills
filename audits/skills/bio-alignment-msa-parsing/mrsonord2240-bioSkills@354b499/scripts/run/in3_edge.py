"""Input 3 (Edge): 'Some of my columns are all gaps, my HMMER/HHsuite files use '.' and lowercase inserts, one file has a single sequence,
and I have an A3M from ColabFold. Get match-only columns and consensus without it blowing up.'  ALL data SYNTHETIC (labelled syn_*)."""
import os, sys, shutil, subprocess, io
import numpy as np
from Bio import AlignIO, Align
from common import *
import skill_md_funcs as F
D = os.path.join(HERE, 'data')
def w(name, txt): open(os.path.join(D, name), 'w', newline='\n').write(txt)

# SYNTHETIC files
w('syn_gaponly.fasta', '>g1\nAC-G\n>g2\nAC-G\n>g3\nAT-G\n')
w('syn_single.fasta', '>only\nACDE-G\n')
w('syn_unequal.fasta', '>a\nACDEF\n>b\nACDE\n')
w('syn_dotgaps.fasta', '>a\nAC..GT\n>b\nACDEGT\n>c\nAC..GT\n')       # '.' gaps as emitted by hmmalign/A2M
# A2M: query ACDE..FGHIK ; inserts lowercase, '.' pad in insert columns; '-' = deletion in match column
w('hhsearch_output.a2m', '>query\nACDE..FGHIK\n>s2\nAC-EwyFGHIK\n>s3\nACDE.yFG-IK\n')
w('syn_colabfold.a3m', '>query\nACDEFGHIK\n>s2\nAC-EwyFGHIK\n>s3\nACDEyFG-IK\n')   # A3M: NOT padded (9, 11, 10)

# A. all-gap column
g = AlignIO.read(os.path.join(D, 'syn_gaponly.fasta'), 'fasta')
check('SYNTH gap-only col: consensus emits "-" and keeps length 4 (AC-G)', F.consensus_sequence(g, 0.5) == 'AC-G', F.consensus_sequence(g, 0.5))
check('SYNTH gap-only col: not reported as conserved', 2 not in [c for c, _ in F.find_conserved_positions(g, 0.5)])
check('SYNTH gap-only col: remove_gappy_columns drops it => 3 cols', F.remove_gappy_columns(g, 0.5).get_alignment_length() == 3)
check('SYNTH consensus threshold 1.0: col1 (C,C,T) is ambiguous N', F.consensus_sequence(g, 1.0) == 'ANG'.replace('N', 'N')[0:1] + 'N' + '-' + 'G' or F.consensus_sequence(g, 1.0) == 'AN-G', F.consensus_sequence(g, 1.0))

# B. single sequence
s = AlignIO.read(os.path.join(D, 'syn_single.fasta'), 'fasta')
check('SYNTH single-seq alignment loads (1 x 6)', (len(s), s.get_alignment_length()) == (1, 6))
check('SYNTH single-seq consensus == the sequence, gap col kept', F.consensus_sequence(s, 0.5) == 'ACDE-G', F.consensus_sequence(s, 0.5))
check('SYNTH single-seq conserved: all 5 residue cols "100% conserved" (trivial; no warning by skill)', len(F.find_conserved_positions(s, 1.0)) == 5)

# C. unequal lengths -> AlignIO error (SKILL "Common Errors: Unequal sequence lengths -> Invalid MSA")
try:
    AlignIO.read(os.path.join(D, 'syn_unequal.fasta'), 'fasta'); ok = False; msg = 'no error'
except Exception as e:
    ok, msg = True, f'{type(e).__name__}: {e}'
check('SYNTH unequal lengths raises a clear error (Common Errors row)', ok, msg)

# D. '.' gap char
d = AlignIO.read(os.path.join(D, 'syn_dotgaps.fasta'), 'fasta')
gp = F.gaps_per_column(d)
print("gaps_per_column with '.' gaps:", gp)
check("'.'-gapped input: gaps_per_column reports 2 gaps in cols 2,3 (user expectation) [defect if FAIL: only '-' recognised]", gp == [0, 0, 2, 2, 0, 0], str(gp))
seq_to_aln, aln_to_seq = F.coordinate_map(d[0])
check("'.'-gapped input: coordinate_map treats '.' as gap (len(seq_to_aln)==4) [defect if FAIL]", len(seq_to_aln) == 4, f'len={len(seq_to_aln)}')
check("'.'-gapped input: consensus does not emit '.' as a residue [defect if FAIL]", '.' not in F.consensus_sequence(d, 0.5), F.consensus_sequence(d, 0.5))

# E. shipped a2m_a3m_io.py from a COPY on synthetic A2M
ex = os.path.join(HERE, 'ex3'); shutil.rmtree(ex, ignore_errors=True); shutil.copytree(SKILL_EX, ex)
shutil.copy(os.path.join(D, 'hhsearch_output.a2m'), os.path.join(ex, 'hhsearch_output.a2m'))
p = subprocess.run([sys.executable, 'a2m_a3m_io.py'], cwd=ex, capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'})
print(p.stdout, p.stderr[-300:])
check('a2m_a3m_io.py: rc=0; "3 sequences, 11 columns"; "9 match columns"', p.returncode == 0 and '3 sequences, 11 columns' in p.stdout and '9 match columns' in p.stdout)
check('a2m_a3m_io.py: insert counts query=0, s2=2, s3=1 (hand-known)', 'query: 9 match, 0 inserts' in p.stdout and 's2: 9 match, 2 inserts' in p.stdout and 's3: 9 match, 1 inserts' in p.stdout)
sys.path.insert(0, ex)
import importlib.util
spec = importlib.util.spec_from_file_location('a2m', os.path.join(ex, 'a2m_a3m_io.py')); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
a2m = AlignIO.read(os.path.join(D, 'hhsearch_output.a2m'), 'fasta')
mo = mod.match_only_columns(a2m)
check('match_only_columns == hand-known ["ACDEFGHIK","AC-EFGHIK","ACDEFG-IK"]', mo == ['ACDEFGHIK', 'AC-EFGHIK', 'ACDEFG-IK'], str(mo))

# F. A3M loaded directly as a rectangular MSA (SKILL says it must be reformatted first)
try:
    AlignIO.read(os.path.join(D, 'syn_colabfold.a3m'), 'fasta'); ok = False; msg = 'loaded'
except Exception as e:
    ok, msg = True, f'{type(e).__name__}: {e}'
check('A3M direct load fails loudly with a length error (SKILL.md warns to reformat)', ok, msg)
# does the SKILL's other suggested path work: pyhmmer MSAFile format a2m / a3m?
import pyhmmer
# NB: pyhmmer MSA.sequences is DEALIGNED; the aligned rows are MSA.alignment (my first probe used .sequences and was wrong).
with pyhmmer.easel.MSAFile(os.path.join(D, 'hhsearch_output.a2m'), format='a2m') as f:
    m = f.read()
check("pyhmmer.easel.MSAFile(format='a2m') on padded A2M: .alignment rows equal the file (3 x 11)", list(m.alignment) == ['ACDE..FGHIK', 'AC-EwyFGHIK', 'ACDEy.FG-IK'] or list(m.alignment) == ['ACDE..FGHIK', 'AC-EwyFGHIK', 'ACDE.yFG-IK'], str(list(m.alignment)))
# alignment-io (pointed at by msa-parsing) says A3M can be read with MSAFile(..., format='a2m'). Check on the unpadded A3M:
with pyhmmer.easel.MSAFile(os.path.join(D, 'syn_colabfold.a3m'), format='a2m') as f:
    m3 = f.read()
rows = list(m3.alignment)
print('MSAFile(format=a2m) on UNPADDED A3M .alignment ->', rows)
check("hand-off claim (alignment-io): MSAFile(format='a2m') pads an A3M to a rectangular MSA; match-only columns == hand-known", len({len(x) for x in rows}) == 1 and mod.match_only_columns([type('R', (), {'seq': x})() for x in rows]) == ['ACDEFGHIK', 'AC-EFGHIK', 'ACDEFG-IK'], str(rows))

# G. API note in SKILL.md: Bio.Align.read returns numpy-backed Alignment; [:, idx]
al = Align.read(os.path.join(D, 'syn_gaponly.fasta'), 'fasta')
print('Bio.Align.read type', type(al).__name__, '| [:,0] ->', type(al[:, 0]).__name__, repr(al[:, 0]))
check('API note: Alignment (Bio.Align.read) has no get_alignment_length (SKILL snippets are for AlignIO objects only)', not hasattr(al, 'get_alignment_length'))
check("API note: alignment[:, idx] on Bio.Align.Alignment returns str as SKILL implies 'verify'", isinstance(al[:, 0], str), type(al[:, 0]).__name__)
summary()
