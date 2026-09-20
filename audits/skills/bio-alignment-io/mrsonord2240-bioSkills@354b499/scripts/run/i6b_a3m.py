"""Input 6b: A3M/A2M section of SKILL.md on REAL reformat.pl output (i6b_a3m.sh). Checks the SKILL's claims: A3M is ragged; a2m via reformat.pl is rectangular; match-state extraction snippet."""
import pathlib
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
d = pathlib.Path(__file__).parent/'data'
def rows(p):
    out, cur = {}, None
    for l in open(p):
        l = l.rstrip('\n')
        if l.startswith('>'): cur = l[1:]; out[cur] = ''
        else: out[cur] += l
    return out
a3 = rows(d/'pf.a3m'); print('a3m: n', len(a3), 'distinct row lengths', len(set(len(v) for v in a3.values())))
ok(len(set(len(v) for v in a3.values())) > 1, 'A3M is ragged (as SKILL says: not padded)')
try: AlignIO.read(d/'pf.a3m', 'fasta'); ok(False, 'AlignIO.read on raw a3m worked')
except ValueError as e: ok(True, f'AlignIO.read(raw a3m, "fasta") refuses: {e}')
first = list(a3.values())[0]; nmatch = sum(1 for c in first if c.isupper() or c == '-'); print('first-seq match-state columns:', nmatch)
al = AlignIO.read(d/'pf.a2m', 'fasta'); print('a2m via reformat.pl: rectangular', len(al), 'x', al.get_alignment_length())
ok((len(al), al.get_alignment_length()) == (73, al.get_alignment_length()) , 'reformat.pl a3m->a2m output is rectangular and loads with AlignIO fasta (SKILL claim holds)')
match_only_seqs = [''.join(c for c in str(r.seq) if c.isupper() or c == '-') for r in al]     # VERBATIM from SKILL
lens = set(len(s) for s in match_only_seqs)
ok(lens == {nmatch}, f'SKILL match-only snippet: all 73 rows length {lens}, expected {nmatch} match columns')
dots = sum(str(r.seq).count('.') for r in al); ok(dots > 0, f'insert padding present: {dots} dot characters in a2m')
# what does the SKILL's snippet do to '.' ? it drops them (not upper, not '-') -> good
# and lowercase insert residues are dropped
ins = sum(1 for r in al for c in str(r.seq) if c.islower()); print('lowercase insert residues dropped:', ins)
