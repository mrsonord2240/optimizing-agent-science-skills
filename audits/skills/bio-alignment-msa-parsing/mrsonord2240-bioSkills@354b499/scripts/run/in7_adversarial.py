"""Input 7 (Adversarial / ambiguous): 'Get the secondary structure and RF/consensus annotation out of my Stockholm alignment and keep it when I
clean the alignment; also give me the consensus of my soft-masked (mixed-case) DNA alignment, and filter sequences with the regex I typed.'
Synthetic Stockholm (syn_annot.sto) + synthetic DNA (syn_dna_mixedcase.fasta); real Pfam seed for the real-annotation cross-check.
Usage-guide 'Working with Annotations' snippet is run VERBATIM."""
import os, io, re, inspect, warnings
from collections import Counter
from Bio import AlignIO
import Bio.Align.AlignInfo as AI
from common import *
import skill_md_funcs as F
D = os.path.join(HERE, 'data')

open(os.path.join(D, 'syn_annot.sto'), 'w', newline='\n').write('''# STOCKHOLM 1.0
#=GF ID   syn_annot
#=GS seqA  OS  Homo sapiens
#=GS seqB  OS  Mus musculus
seqA  ACDEFGH
seqB  AC-EFGH
#=GR seqA SS  HHHEEEC
#=GR seqB SS  HHH-EEC
#=GC SS_cons  HHHEEEC
#=GC RF       xxx.xxx
//
''')
open(os.path.join(D, 'syn_dna_mixedcase.fasta'), 'w', newline='\n').write('>s1\nACGTacgt\n>s2\nACGTACGT\n>s3\nacgtACGT\n>s4\nACGTacgt\n')

# 1. usage-guide snippet, verbatim, on synthetic Stockholm with SS / SS_cons
alignment = AlignIO.read(os.path.join(D, 'syn_annot.sto'), 'stockholm')
printed = []
for record in alignment:
    if 'secondary_structure' in record.letter_annotations:
        printed.append((record.id, record.letter_annotations['secondary_structure']))
ss_cons = alignment.column_annotations.get('secondary_structure')
print('letter_annotations keys:', [list(r.letter_annotations) for r in alignment])
print('column_annotations keys:', list(alignment.column_annotations))
print('annotations keys:', [list(r.annotations) for r in alignment])
check("usage-guide snippet: 'secondary_structure' key in record.letter_annotations finds the GR SS line (key name verified correct for Biopython 1.88)", len(printed) == 2, f'printed={printed}; actual keys={[list(r.letter_annotations) for r in alignment]}')
check("usage-guide snippet: alignment.column_annotations.get('secondary_structure') returns SS_cons (key name verified correct)", ss_cons is not None, f'got {ss_cons!r}; actual keys={list(alignment.column_annotations)}')

# 2. real Pfam: does the snippet surface the annotations that are really there?
real = AlignIO.read(PFAM_STO, 'stockholm')
has_ss = sum(1 for r in real if 'secondary_structure' in r.letter_annotations)
keys = Counter(k for r in real for k in r.letter_annotations)
print('REAL Pfam letter_annotation keys:', dict(keys), '| column_annotations:', list(real.column_annotations))
check('REAL Pfam seed carries no GR SS lines, so the snippet correctly prints nothing there (GR keys present are other tags)', has_ss == 0 and 'secondary_structure' not in keys, f'{has_ss} records; keys {dict(keys)}')

# 3. Stockholm round trip: SKILL says GC SS_cons, RF, GS survive read/write in 'stockholm' and are lost in FASTA/PHYLIP/NEXUS
buf = io.StringIO(); AlignIO.write(alignment, buf, 'stockholm')
back = AlignIO.read(io.StringIO(buf.getvalue()), 'stockholm')
print('after stockholm round trip: col keys', list(back.column_annotations), '| rec keys', [list(r.letter_annotations) for r in back], [list(r.annotations) for r in back])
rt_ok = (set(back.column_annotations) == set(alignment.column_annotations) and [dict(r.letter_annotations) for r in back] == [dict(r.letter_annotations) for r in alignment])
check("stockholm round-trip preserves GC (SS_cons, RF) and GR SS  (SKILL.md/usage-guide claim)", rt_ok, buf.getvalue().replace('\n', ' | ')[:300])
gs_kept = all('Homo sapiens' in str(r.annotations) or 'Mus musculus' in str(r.annotations) for r in back)
check("stockholm round-trip preserves GS metadata (organism) (usage-guide claim)", gs_kept or ('#=GS' in buf.getvalue()), str([r.annotations for r in back]))
fa = io.StringIO(); AlignIO.write(alignment, fa, 'fasta')
check("FASTA write discards annotations (claim: 'silently discarded')", '#' not in fa.getvalue() and 'HHH' not in fa.getvalue())
# cleaning function then write stockholm: annotations lost silently
cleaned = F.remove_gappy_columns(alignment, 0.5)
b2 = io.StringIO(); AlignIO.write(cleaned, b2, 'stockholm')
print('cleaned -> stockholm text has GR/GC lines:', '#=GR' in b2.getvalue(), '#=GC' in b2.getvalue())
check("skill cleaning (remove_gappy_columns) then write('stockholm') keeps SS_cons/RF [FAIL = annotations silently dropped; usage-guide says 'keep a Stockholm master copy']", '#=GC' in b2.getvalue())

# 4. mixed-case DNA (soft-masked) consensus
dna = AlignIO.read(os.path.join(D, 'syn_dna_mixedcase.fasta'), 'fasta')
cons = F.consensus_sequence(dna, 0.7)
print('mixed-case DNA consensus @0.7:', cons)
check("case-insensitive consensus @0.7: every column is one base in either case -> 'ACGTACGT' [FAIL = Counter is case-sensitive, split votes fall below threshold and give N]", cons.upper() == 'ACGTACGT', cons)
fc = F.find_conserved_positions(dna, 1.0)
check("case-insensitive conservation: all 8 columns fully conserved [FAIL = 0 columns reported for cols 4-7 due to case split]", len(fc) == 8, f'{len(fc)} reported')

# 5. user-supplied regex
try:
    F.filter_by_id(alignment, '[')
    ok, msg = False, 'no error'
except re.error as e:
    ok, msg = True, f're.error: {e}'
except Exception as e:
    ok, msg = False, f'{type(e).__name__}: {e}'
check('filter_by_id with a malformed user regex fails with a clear re.error (no silent empty result)', ok, msg)
check("filter_by_id treats pattern as regex: 'seqA|seqB' matches both", [r.id for r in F.filter_by_id(alignment, 'seqA|seqB')] == ['seqA', 'seqB'])

# 6. SummaryInfo note (SKILL: 'deprecated ... when deprecation warnings appear')
have = [m for m in ('dumb_consensus', 'gap_consensus', 'pos_specific_score_matrix', 'information_content') if hasattr(AI.SummaryInfo, m)]
print('SummaryInfo methods still present on Biopython 1.88:', have)
check("SKILL note says AlignInfo.SummaryInfo is 'deprecated' (emits warnings); on the tested 1.88 the methods are REMOVED (AttributeError) [FAIL = doc understates]", len(have) > 0, f'present: {have}')

# 7. weighting guidance vs shipped functions
weighted = [n for n, f in inspect.getmembers(F, inspect.isfunction) if f.__module__ == 'skill_md_funcs' and 'weight' in ' '.join(inspect.signature(f).parameters)]
print('functions accepting a weights argument:', weighted)
check("SKILL says 'compute sequence weights before any column-wise statistic', yet no column-wise function (conserved/consensus/gaps) accepts weights [FAIL = guidance not actionable]", len(weighted) > 0, 'none of find_conserved_positions / consensus_sequence / gaps_per_column takes weights')
summary()
