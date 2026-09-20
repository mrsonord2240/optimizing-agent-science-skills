"""INPUT 3b (regression of old inputs 1/7): the SKILL's plain read / write / convert / slice / create / batch / Bio.Align code blocks, executed VERBATIM
(extracted from SKILL.md) against the REAL Pfam alignment written as Clustal, with the file names substituted. Asserts on content."""
import io, os, shutil, contextlib
from Bio import AlignIO
from common import *
w = DATA/'blocks'; shutil.rmtree(w, ignore_errors=True); w.mkdir(); os.chdir(w)
ref = AlignIO.read(str(PFAM), 'stockholm')
AlignIO.write(ref, 'alignment.aln', 'clustal'); AlignIO.write(ref, 'multi_alignment.sto', 'stockholm')
rows = [str(r.seq).upper().replace('.', '-') for r in ref]; ids = [r.id for r in ref]
def run(head, subs=None, pre='from Bio import AlignIO\n', ns=None):
    code = pre + block(head)
    for a, b in (subs or {}).items(): code = code.replace(a, b)
    ns = ns if ns is not None else {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(code, ns)
    return buf.getvalue(), ns
o, ns = run('Single Alignment File'); ok('Alignment length: 141' in o and 'Number of sequences: 73' in o, 'Single Alignment File block: ' + o.strip().replace('\n', ' | '))
alignment = ns['alignment']
o, ns2 = run('Multiple Alignments in One File', {"'multi_alignment.sto'": "'multi_alignment.sto'"}); ok('73 sequences, length 141' in o, 'Multiple Alignments block: ' + o.strip())
AlignIO.write(ref, 'alignments.phy', 'phylip-relaxed')
o, ns3 = run('Read as List', {"'phylip')": "'phylip-relaxed')"}); ok(len(ns3['alignments']) == 1, 'Read as List block (with relaxed format string): 1 alignment')
o, _ = run('Write Single Alignment', ns={'alignment': alignment}); ok([str(r.seq).upper() for r in AlignIO.read('output.fasta', 'fasta')] == rows, 'Write Single Alignment: output.fasta re-reads with identical rows')
a1, a2, a3 = alignment, alignment[:30], alignment[30:60]
o, _ = run('Write Multiple Alignments', ns={'alignment1': a1, 'alignment2': a1, 'alignment3': a1}); ok('Wrote 3 alignments' in o, 'Write Multiple: ' + o.strip())
o, _ = run('Write to Handle', ns={'alignment': alignment}); ok(len(AlignIO.read('output.aln', 'clustal')) == 73, 'Write to Handle: output.aln re-reads 73 records')
o, _ = run('Direct Conversion', {"'input.aln'": "'alignment.aln'"}); b = AlignIO.read('output.phy', 'phylip-relaxed'); ok([r.id for r in b] == ids and [str(r.seq).upper() for r in b] == rows, 'Direct Conversion (phylip-relaxed): ids (with /start-end) and rows identical to source')
o, _ = run('NEXUS Output Needs', {"'input.sto', 'stockholm'": f"{str(PFAM)!r}, 'stockholm'", "molecule_type='DNA'": "molecule_type='protein'", "'input.aln'": "'alignment.aln'", "'DNA'": "'protein'"}); nx = AlignIO.read('output.nex', 'nexus'); ok(len(nx) == 73 and nx.get_alignment_length() == 141, f'NEXUS block (both variants, protein): output.nex re-reads {len(nx)}x{nx.get_alignment_length()}')
o, _ = run('Manual Conversion', {"'input.aln'": "'alignment.aln'"}); ok(len(AlignIO.read('output.fasta', 'fasta')) == 73, 'Manual Conversion block ran')
o, ns4 = run('Accessing Alignment Data'); ns4['alignment']
ok(str(ns4['first_seq'].seq).upper() == rows[0] and len(ns4['column_slice']) == 73 and ns4['column_slice'].get_alignment_length() == 10 and len(ns4['column']) == 73 and ns4['region'].get_alignment_length() == 91 and len(ns4['region']) == 5, 'Accessing Alignment Data block: first_seq, [:,10:20] -> 10 cols, column string of 73, region 5 x 91 (cols 50:141 because the alignment has 141)')
sl = alignment[:, 200:300]; ok(sl.get_alignment_length() == 0 and len(sl) == 73, 'SKILL sentence "Column slices past the alignment length silently return 0 columns": confirmed (73 records, 0 columns)')
buf = io.StringIO(); AlignIO.write(sl, buf, 'fasta'); ok(all(l.startswith('>') for l in buf.getvalue().splitlines() if l), 'and the FASTA written from it has 73 headers and empty sequences (0-length records)')
o, ns5 = run('Creating Alignments Programmatically', pre='from Bio import AlignIO\n'); c = AlignIO.read('new_alignment.fasta', 'fasta'); ok((len(c), c.get_alignment_length()) == (3, 12), 'Creating Alignments block: 3x12 written and re-read')
(w/'alignments').mkdir(); shutil.copy('alignment.aln', w/'alignments'/'g1.aln'); shutil.copy('alignment.aln', w/'alignments'/'g2.aln')
o, _ = run('Batch Processing'); ok(sorted(p.name for p in (w/'converted').glob('*.fasta')) == ['g1.fasta', 'g2.fasta'], 'Batch Processing block VERBATIM (converted/ did not exist beforehand: block now has mkdir): converted/ has g1.fasta, g2.fasta')
ok(len(AlignIO.read(w/'converted'/'g1.fasta', 'fasta')) == 73, 'converted/g1.fasta re-reads 73 records')
# MrBayes id-sanitising recipe (second python block under the NEXUS heading), executed verbatim on the real Pfam ids
rec = AlignIO.read(str(PFAM), 'stockholm'); before = [r.id for r in rec]
ns = {'alignment': rec}; exec(block('NEXUS Output Needs', 1), ns)
after = [r.id for r in rec]; print('ids before/after:', before[:2], after[:2])
import re as _re
ok(all(_re.fullmatch(r'[A-Za-z0-9_]+', i) for i in after) and len(set(after)) == 73, 'MrBayes recipe (verbatim): all 73 real Pfam ids now [A-Za-z0-9_]+ and unique')
ok(all(r.name == r.id and r.description == '' for r in rec), 'recipe also resets name/description to the new id')
for r in rec: r.annotations['molecule_type'] = 'protein'
AlignIO.write(rec, 'recipe.nex', 'nexus'); ok("'" not in open('recipe.nex').read(), 'NEXUS written after the recipe contains no single quotes')
orig = AlignIO.read(str(PFAM), 'stockholm')
for r in orig: r.annotations['molecule_type'] = 'protein'
AlignIO.write(orig, 'orig.nex', 'nexus'); ok(open('orig.nex').read().count("'") > 100, 'NEXUS written WITHOUT the recipe has quoted ids (' + str(open('orig.nex').read().count("'")) + ' quote chars), as the SKILL says')
# collision: the recipe's own assertion must fire
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
col = MultipleSeqAlignment([SeqRecord(Seq('ACGT'), id='a-1'), SeqRecord(Seq('ACGT'), id='a+1')])
try: exec(block('NEXUS Output Needs', 1), {'alignment': col}); ok(False, 'recipe did not notice colliding ids a-1 / a+1')
except AssertionError as e: ok('collide' in str(e), f'recipe assertion fires on ids that collide after sanitising: {e}')
shutil.copy(DATA/'ucsc_mm9_chr10.maf', 'blocks.maf')
o, ns6 = run('Alternative: Bio.Align', pre='')
ok('(73, 141)' in o and 'AlignmentCounts' in o and o.count('Alignment with') == 48, 'Bio.Align block verbatim (real Pfam clustal + real UCSC MAF): shape (73, 141), counts() AlignmentCounts, 48 MAF blocks parsed')
a = AlignIO.read('output.fasta', 'fasta'); ok(len(a) == 73, 'Bio.Align block Align.write -> output.fasta re-reads 73 records')
o, _ = run('Required Import', pre=''); ok(True, 'Required Import block runs')
summary()
