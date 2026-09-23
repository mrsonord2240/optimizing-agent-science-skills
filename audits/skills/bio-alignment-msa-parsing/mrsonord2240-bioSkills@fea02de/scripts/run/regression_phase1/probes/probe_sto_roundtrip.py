"""Probe: does Biopython 1.88's Stockholm writer round-trip the REAL Pfam GC/GR keys at all (uncleaned alignment)? Separates a Biopython limit from a Skill defect."""
import io, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Bio import AlignIO
from common import *
import skillns
ns, _ = skillns.load()
aln = AlignIO.read(PFAM_STO, 'stockholm')
buf = io.StringIO(); AlignIO.write(aln, buf, 'stockholm'); out = buf.getvalue()
print('ORIGINAL write: lines with #=GC:', [l[:50] for l in out.splitlines() if l.startswith('#=GC')][:3], '| #=GR count:', sum(l.startswith('#=GR') for l in out.splitlines()), '| #=GS count', sum(l.startswith('#=GS') for l in out.splitlines()))
back = AlignIO.read(io.StringIO(out), 'stockholm')
print('ORIGINAL re-read column_annotations:', list(back.column_annotations), '| letter_annotation keys:', {k for r in back for k in r.letter_annotations})
cl = ns['remove_gappy_columns'](aln, 0.5)
buf = io.StringIO(); AlignIO.write(cl, buf, 'stockholm'); out2 = buf.getvalue()
print('CLEANED write: #=GC lines:', [l[:60] for l in out2.splitlines() if l.startswith('#=GC')][:3], '| #=GR count:', sum(l.startswith('#=GR') for l in out2.splitlines()), '| #=GS count', sum(l.startswith('#=GS') for l in out2.splitlines()))
print('column_annotations in memory (raw key names):', list(cl.column_annotations), '| letter_annotations of record with one:', [(r.id, dict(r.letter_annotations).keys()) for r in cl if r.letter_annotations][:1])
print(out2[:600])
