"""Re-audit helpers (auditor code). Parsers marked VERBATIM are copied from the fixed SKILL.md (mrsonord2240/bioSkills@966f838)."""
import os, re, sys
from Bio import AlignIO
import dendropy
from dendropy.calculate import treecompare


def trimming_fraction(input_alignment, trimmed_alignment):  # VERBATIM SKILL.md "Aggressiveness Cap"
    return trimmed_alignment.get_alignment_length() / input_alignment.get_alignment_length()


def clipkit_kept(logpath):  # VERBATIM SKILL.md "Column Mapping" (file name parameterised)
    return [int(row.split()[0]) - 1 for row in open(logpath) if row.split()[1] == 'keep']


def trimal_kept(colpath):  # VERBATIM SKILL.md "Column Mapping" (file name parameterised)
    return [int(x) for x in open(colpath).read().split('\t', 1)[1].split(',')]


def verify_map(orig_fa, trimmed_fa, idx):
    o = AlignIO.read(orig_fa, 'fasta'); t = AlignIO.read(trimmed_fa, 'fasta')
    om = {r.id: str(r.seq) for r in o}
    ok = len(idx) == t.get_alignment_length() and all(
        om[r.id][c] == str(r.seq)[k] for r in t for k, c in enumerate(idx))
    return len(idx), t.get_alignment_length(), ok


def rule(r, mode=''):
    if mode.startswith(('kpi', 'clip_kpi')):
        return 'kpi/kpic: fraction not informative (Skill) -> judge by trees'
    return 'light (<20% removed)' if r > 0.8 else ('>40% removed: too aggressive' if r < 0.6 else '20-40% removed')


def retention_table(inp, names):
    if not os.path.exists(inp):
        inp = inp + '.fasta'
    L0 = AlignIO.read(inp, 'fasta').get_alignment_length()
    print(f'untrimmed columns {L0}')
    for n in names:
        f = n + '.fasta'
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            print(f'{n:<24} NO OUTPUT'); continue
        L = AlignIO.read(f, 'fasta').get_alignment_length(); r = L / L0
        print(f'{n:<24}{L:>6}{r:>9.1%}  {rule(r, n)}')


def tree_table(truth, prefixes, support_from='treefile'):
    tns = dendropy.TaxonNamespace()
    tr = dendropy.Tree.get(path=truth, schema='newick', taxon_namespace=tns, preserve_underscores=True)
    tr.is_rooted = False; tr.encode_bipartitions()
    print(f'{"tree":<26}{"RF":>4}{"wRF":>8}{"TL":>8}{"TL_true":>8}  support<95')
    for p in prefixes:
        t = dendropy.Tree.get(path=p + '.' + support_from, schema='newick', taxon_namespace=tns, preserve_underscores=True)
        t.is_rooted = False; t.encode_bipartitions()
        sup = []
        for nd in t.internal_nodes():
            if nd.label:
                sup.append(float(nd.label.split('/')[-1]))
        print(f'{p:<26}{treecompare.symmetric_difference(tr, t):>4}{treecompare.weighted_robinson_foulds_distance(tr, t):>8.3f}'
              f'{t.length():>8.2f}{tr.length():>8.2f}  {sum(s < 95 for s in sup)}/{len(sup)}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'retention':
        retention_table(sys.argv[2], sys.argv[3:])
    elif cmd == 'trees':
        tree_table(sys.argv[2], sys.argv[3:])
    elif cmd == 'contrees':
        tree_table(sys.argv[2], sys.argv[3:], 'contree')
    elif cmd == 'in1':
        a = AlignIO.read('input.fasta', 'fasta'); t = AlignIO.read('trimmed.fasta', 'fasta')
        f = trimming_fraction(a, t)
        print(f'retention {f:.1%}; {rule(f)}; warn(<0.6): {f < 0.6}')
        print('log exists:', os.path.exists('trimmed.fasta.log'), '| first row:', repr(open('trimmed.fasta.log').readline()))
        print('Skill clipkit log parser -> kept, trimmed_len, residues match:', verify_map('input.fasta', 'trimmed.fasta', clipkit_kept('trimmed.fasta.log')))
    elif cmd == 'in4':
        for fa, cols in [('hmm_gappyout.fasta', 'gappyout_cols.txt'), ('auto1.fasta', 'kept_columns.txt'), ('manual.fasta', 'columns.txt')]:
            try:
                print(cols, 'Skill trimAl parser -> kept, trimmed_len, residues match:', verify_map('input.fasta', fa, trimal_kept(cols)))
            except Exception as e:
                print(cols, 'PARSER FAILED:', type(e).__name__, e)
