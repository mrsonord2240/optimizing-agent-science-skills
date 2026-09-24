"""Input 3 report: the Skill's kpic mitigation (outgroup branch length before vs after) plus AUDITOR truth checks."""
from collections import Counter
import dendropy
from dendropy.calculate import treecompare
from Bio import AlignIO

OUT = {'Out1', 'Out2', 'Out3'}
a0 = AlignIO.read('input.fasta', 'fasta')
L0 = a0.get_alignment_length()


def cols_informative_for_outgroup(aln):
    """Columns where the 3 outgroups share a state absent from (almost) all ingroup taxa: outgroup-vs-ingroup signal."""
    n = 0
    single = 0
    ids = [r.id for r in aln]
    seqs = [str(r.seq) for r in aln]
    for j in range(aln.get_alignment_length()):
        col = {i: s[j] for i, s in zip(ids, seqs)}
        out_states = Counter(col[i] for i in OUT if col[i] != '-')
        in_states = Counter(col[i] for i in col if i not in OUT and col[i] != '-')
        for st, c in out_states.items():
            if in_states.get(st, 0) == 0:
                n += 1
                if c == 1:
                    single += 1
                break
    return n, single


print(f'untrimmed: {L0} columns; outgroup-private-state columns / of which single-outgroup: {cols_informative_for_outgroup(a0)}')
for m in ('kpic-smart-gap', 'smart-gap'):
    a = AlignIO.read(f'unbal_{m}.fasta', 'fasta')
    log = [l.split() for l in open(f'unbal_{m}.fasta.log')]
    print(f'{m}: kept {a.get_alignment_length()}/{L0} = {a.get_alignment_length()/L0:.1%};',
          'trimmed classes', Counter(r[2] for r in log if r[1] == 'trim').most_common(),
          '; outgroup-private-state cols kept / single-outgroup:', cols_informative_for_outgroup(a))

tns = dendropy.TaxonNamespace()
def load(p):
    t = dendropy.Tree.get(path=p, schema='newick', taxon_namespace=tns, preserve_underscores=True)
    return t
truth = load('../../data/unbal33_true.nwk')
truth.is_rooted = False; truth.encode_bipartitions()
# true splits with an edge long enough to be recoverable (>= 0.003 subst/site, i.e. >= ~3 changes over 1,000 nt)
strong_true = {b for b, e in truth.bipartition_edge_map.items() if not b.is_trivial() and (e.length or 0) >= 0.003}
print(f'true tree: {len(strong_true)} non-trivial splits with edge length >= 0.003 (the rest of the shallow ingroup is ~unresolvable)')


def outgroup_stem(t):
    """Root on an ingroup leaf; the edge subtending {Out1,Out2,Out3} is the ingroup/outgroup stem (the Skill's check)."""
    t.reroot_at_edge(t.find_node_with_taxon_label('In01').edge, update_bipartitions=True)
    t.is_rooted = True
    mr = t.mrca(taxon_labels=sorted(OUT))
    ok = set(l.taxon.label for l in mr.leaf_iter()) == OUT
    pend = {l.taxon.label: round(l.edge.length, 4) for l in mr.leaf_iter()} if ok else None
    return ok, (mr.edge.length if ok else None), pend


print('TRUE', outgroup_stem(load('../../data/unbal33_true.nwk')))
for name in ('untrimmed', 'kpic', 'smartgap'):
    t = load(f'{name}.treefile')
    out_clade_ok, stem, pend = outgroup_stem(t)
    tl = sum(e.length or 0 for e in t.postorder_edge_iter())
    t.is_rooted = False; t.encode_bipartitions()
    est = set(t.bipartition_edge_map)
    print(f'{name}: outgroup pendant lengths {pend}; recovered strong true splits {len(strong_true & est)}/{len(strong_true)}')
    rf = treecompare.symmetric_difference(truth, t)
    iq = open(f'{name}.iqtree').read()
    model = [l for l in iq.splitlines() if l.startswith('Best-fit model according to BIC')]
    print(f'{name}: outgroup clade monophyletic={out_clade_ok}; ingroup/outgroup stem length={stem}; tree length={tl:.4f};'
          f' AUDITOR RF to true={rf} (max {2*(len(tns)-3)}); {model}')
