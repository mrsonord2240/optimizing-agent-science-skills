"""Input 4 report: parse -colnumbering as the Skill describes ("comma-separated list of original column indices on stdout,
e.g. 0, 1, 2, 4, ...") and verify it against the trimmed alignment."""
import re
from Bio import AlignIO

orig = AlignIO.read('input.fasta', 'fasta')
L0 = orig.get_alignment_length()
for trimmed, cols in [('hmm_gappyout2.fasta', 'gappyout_cols.txt'), ('manual.fasta', 'columns.txt'), ('auto1.fasta', 'kept_columns.txt')]:
    t = AlignIO.read(trimmed, 'fasta')
    raw = open(cols).read()
    print(f'--- {cols}: {len(raw)} bytes; first line repr: {raw.splitlines()[0][:80]!r}')
    # naive parse per the Skill's description
    try:
        naive = [int(x) for x in raw.strip().split(',')]
        print('naive comma split parse: OK', len(naive))
    except ValueError as e:
        print('naive comma split parse (as the Skill describes the format): FAILS ->', str(e)[:80])
    body = raw.split('#ColumnsMap', 1)[-1]
    idx = [int(x) for x in re.findall(r'\d+', body)]
    ok = len(idx) == t.get_alignment_length() and all(
        str(orig[i].seq[c]) == str(t[i].seq[k]) for i in range(len(orig)) for k, c in enumerate(idx))
    print(f'robust parse: {len(idx)} indices, trimmed length {t.get_alignment_length()} ({t.get_alignment_length()/L0:.1%} of {L0});'
          f' 0-based={min(idx) == 0 or min(idx) < 1}; residues match original columns: {ok}')
