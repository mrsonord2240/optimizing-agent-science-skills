"""Input 7 (Adversarial, regression of first-audit input 7): 'Pull the secondary structure and RF annotation out of my Stockholm
alignment and keep it after cleaning; also give me the consensus of my soft-masked (mixed-case) DNA alignment, weight the sequences
before computing conservation, and filter sequences with this regex I typed: "["'
SYNTHETIC inputs (syn_annot.sto written here; the soft-masked DNA and RNA alignments are built in memory), hand-known answers. Code = SKILL.md blocks exec'd from the file (the
Working-with-Annotations block is exec'd verbatim against the synthetic file)."""
import io, os, random, re, warnings
import numpy as np
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment, AlignInfo
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from common import *
import skillns

ns, log = skillns.load()
STO = """# STOCKHOLM 1.0
#=GS seqA AC A0001
#=GS seqA OS Homo sapiens
#=GS seqB AC B0002
#=GS seqB OS Mus musculus
seqA ACDEFGH
#=GR seqA SS HHHEEEC
seqB ACD-FGH
#=GR seqB SS HHH-EEC
#=GC SS_cons HHHEEEC
#=GC RF xxx.xxx
//
"""
p = os.path.join(DATA, 'syn_annot.sto'); open(p, 'w', newline='\n').write(STO)

# ---- the SKILL.md "Working with Annotations" block, verbatim, against the synthetic file -----------------------------------
skill_md = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
blk = [b for b in skillns.blocks(os.path.join(SKILL, 'SKILL.md')) if "AlignIO.read('pfam.sto'" in b][0]
import contextlib
buf = io.StringIO(); loc = dict(ns)
with contextlib.redirect_stdout(buf):
    exec(blk.replace("'pfam.sto'", repr(p)), loc)
print('block output:', buf.getvalue().strip().replace('\n', ' | '), '| ss_cons =', loc['ss_cons'])
check('SKILL.md annotation block, run verbatim on the synthetic Stockholm, prints SS per record and returns SS_cons == HHHEEEC',
      "seqA HHHEEEC" in buf.getvalue() and "seqB HHH-EEC" in buf.getvalue() and loc['ss_cons'] == 'HHHEEEC', buf.getvalue().strip().replace('\n', ' | '))
aln = AlignIO.read(p, 'stockholm')
print('column_annotations:', dict(aln.column_annotations), '| record annotations:', [dict(r.annotations) for r in aln])
check('Biopython key names named in SKILL.md exist: record.letter_annotations["secondary_structure"], column_annotations["secondary_structure"]',
      'secondary_structure' in aln[0].letter_annotations and 'secondary_structure' in aln.column_annotations and 'reference_annotation' in aln.column_annotations)

# ---- keep annotations through cleaning, then write Stockholm -----------------------------------------------------------------
cl = ns['remove_gappy_columns'](aln, 0.5)      # column 3 has 1 gap of 2 rows -> removed
print('after remove_gappy_columns(0.5):', cl.get_alignment_length(), 'columns; column_annotations', dict(cl.column_annotations), '| SS seqA', cl[0].letter_annotations.get('secondary_structure'))
check('cleaning drops column 3 and slices every annotation by hand-computed rule: SS seqA/seqB -> HHHEEC, SS_cons -> HHHEEC, RF -> xxxxxx',
      cl.get_alignment_length() == 6 and cl[0].letter_annotations['secondary_structure'] == 'HHHEEC' and cl[1].letter_annotations['secondary_structure'] == 'HHHEEC'
      and cl.column_annotations['secondary_structure'] == 'HHHEEC' and cl.column_annotations['reference_annotation'] == 'xxxxxx')
out = io.StringIO(); AlignIO.write(cl, out, 'stockholm'); txt = out.getvalue()
back = AlignIO.read(io.StringIO(txt), 'stockholm')
print(txt)
check('cleaned alignment written as Stockholm still carries GR SS, GC SS_cons, GC RF and GS OS lines, and they re-read to the sliced values',
      '#=GR seqA SS' in txt and '#=GC SS_cons' in txt and '#=GC RF' in txt and 'OS Homo sapiens' in txt and back.column_annotations['secondary_structure'] == 'HHHEEC'
      and back[1].letter_annotations['secondary_structure'] == 'HHHEEC' and [r.annotations.get('organism') for r in back] == ['Homo sapiens', 'Mus musculus'])
fa = io.StringIO(); AlignIO.write(cl, fa, 'fasta')
check('FASTA write discards annotations (as SKILL.md says): no # lines, no SS text', '#' not in fa.getvalue() and 'HHH' not in fa.getvalue())
check('SKILL.md says which helpers keep annotations and that hand-built SeqRecord loops do not', 'select_columns`, `remove_gappy_columns` and the filters above keep them' in skill_md)

# ---- soft-masked DNA -------------------------------------------------------------------------------------------------------------
dna = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip('abc', ['ACGTacgt', 'ACGTacgt', 'acgtACGT'])])
c = ns['consensus_sequence'](dna, 0.7)
cons_pos = ns['find_conserved_positions'](dna, 1.0)
print('soft-masked DNA consensus@0.7:', c, '| fully conserved columns:', len(cons_pos))
check('soft-masked DNA: consensus@0.7 == ACGTACGT and 8/8 columns fully conserved (was ACGTNNNN and 0)', c == 'ACGTACGT' and len(cons_pos) == 8)
dna2 = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip('abc', ['ACGTACGT', 'ACGTACGA', 'ACGTACGC'])])
check('DNA alphabet detected: a split column gets the nucleotide placeholder N (not X); protein gets X', ns['consensus_sequence'](dna2, 1.0) == 'ACGTACGN')
rna = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip('ab', ['ACGUacgu', 'ACGUACGA'])])
check('RNA (U) alignment is detected as nucleotide: placeholder N in the split column', ns['consensus_sequence'](rna, 1.0) == 'ACGUACGN')

# ---- typed regex ---------------------------------------------------------------------------------------------------------------------
try:
    ns['filter_by_id'](aln, '['); err = None
except re.error as e:
    err = str(e)
check('malformed user regex "[" raises re.error (clear message), no silent empty alignment', err is not None and 'unterminated character set' in err, err)
check('regex is a regex, not a substring: "seqA|seqB" matches both, "^seqB$" only seqB', len(ns['filter_by_id'](aln, 'seqA|seqB')) == 2 and [r.id for r in ns['filter_by_id'](aln, '^seqB$')] == ['seqB'])

# ---- SummaryInfo statement ---------------------------------------------------------------------------------------------------------
present = [m for m in ('dumb_consensus', 'gap_consensus', 'pos_specific_score_matrix', 'information_content', 'get_column') if hasattr(AlignInfo.SummaryInfo, m)]
try:
    AlignInfo.SummaryInfo(aln).dumb_consensus(); ae = None
except AttributeError as e:
    ae = str(e)
print('SummaryInfo methods present in Biopython 1.88:', present, '| dumb_consensus ->', ae)
check('SKILL.md statement "only get_column remains; others raise AttributeError" is true on Biopython 1.88', present == ['get_column'] and ae is not None)

# ---- weights: actionable now --------------------------------------------------------------------------------------------------------
wal = MultipleSeqAlignment([SeqRecord(Seq(s), id=f's{i}') for i, s in enumerate(['ACDAF', 'ACDAF', 'ACGCF', 'ACDCF'])])
w = [0.1, 0.1, 0.4, 0.4]
cu, cw = ns['consensus_sequence'](wal, 0.5), ns['consensus_sequence'](wal, 0.5, weights=w)
print('unweighted consensus:', cu, '| weighted [.1,.1,.4,.4]:', cw)
# hand: col 3 counts A 2 vs C 2 -> tie (first seen, A); weighted A 0.2 vs C 0.8 -> C. col 2: D 0.6 vs G 0.4 -> D
check('weights= is accepted by consensus_sequence and changes the answer exactly as hand computed (col 3: A -> C)', cu == 'ACDAF' and cw == 'ACDCF')
fw = {(c_, r): round(v, 3) for c_, r, v in ns['find_conserved_positions'](wal, 0.8, weights=w)}
check('weights= on find_conserved_positions: denominator is the weight sum: col 3 C = 0.8, col 2 D = 0.6 (< 0.8, not listed)', fw.get((3, 'C')) == 0.8 and (2, 'D') not in fw, str(fw))
hw = ns['henikoff_weights'](wal)
check('weights from henikoff_weights can be fed straight in (hand: col 3 A 14/30 vs C 16/30 -> C, so ACDCF)', abs(sum(hw) - 1) < 1e-12 and ns['consensus_sequence'](wal, 0.5, weights=hw) == 'ACDCF', ns['consensus_sequence'](wal, 0.5, weights=hw))
# consistency between the two weighted helpers (same tolerance?): fuzz
random.seed(7); mism = []
for t in range(400):
    n = random.randint(3, 8); rows = [''.join(random.choice('AC-') for _ in range(6)) for _ in range(n)]
    ww = [round(random.random(), 2) + 0.01 for _ in range(n)]; th = random.choice([0.5, 0.6, 0.7, 0.8])
    a = MultipleSeqAlignment([SeqRecord(Seq(s), id=f'r{i}') for i, s in enumerate(rows)])
    cons_cols = {c_ for c_, _, _ in ns['find_conserved_positions'](a, th, weights=ww)}
    cs = ns['consensus_sequence'](a, th, weights=ww, ambiguous='?')
    cons_cols2 = {i for i, ch in enumerate(cs) if ch not in '?-'}
    if cons_cols != cons_cols2: mism.append((rows, ww, th))
print('fuzz: find_conserved_positions vs consensus_sequence agreement on 400 random weighted alignments; mismatches:', len(mism))
check('the two weighted helpers agree on which columns pass the threshold (400 random weighted alignments; float tolerance drift check)', not mism, f'{len(mism)} mismatches' + (f'; first: {mism[0]}' if mism else ''))

# ---- "every helper normalises internally": remove_duplicates ------------------------------------------------------------------------
dd = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip('abcd', ['AC-GT', 'AC.GT', 'ac-gt', 'ACAGT'])])
kept = [r.id for r in ns['remove_duplicates'](dd)]
print('remove_duplicates on [AC-GT, AC.GT, ac-gt, ACAGT] keeps', kept)
check('SKILL.md says "every helper normalises its input internally": remove_duplicates should treat AC-GT / AC.GT / ac-gt as duplicates (keep a, d)', kept == ['a', 'd'], f'kept {kept}')
summary()
