"""Input 1 report: Skill's trimming_fraction cap, --log parsing as the Skill describes it, tree sensitivity check."""
import os
from collections import Counter

from Bio import AlignIO, Phylo
import dendropy
from dendropy.calculate import treecompare


def trimming_fraction(input_alignment, trimmed_alignment):          # verbatim from SKILL.md "Aggressiveness Cap"
    return trimmed_alignment.get_alignment_length() / input_alignment.get_alignment_length()


a = AlignIO.read('input.fasta', 'fasta')
t = AlignIO.read('trimmed.fasta', 'fasta')
f = trimming_fraction(a, t)
print(f'retained {t.get_alignment_length()}/{a.get_alignment_length()} columns = {f:.1%}; removed {1-f:.1%}')
print('WARNING: retention < 0.7 -> switch to a less aggressive mode' if f < 0.7 else 'retention >= 0.7 (Skill cap satisfied)')

# SKILL.md: "clipkit --log writes a <output>.log file with one row per original column reporting
#            position\tkeep_or_trim\tsite_classification\tgap_proportion"
print('log files present:', [p for p in os.listdir('.') if p.endswith('.log') and p.startswith(('input', 'trimmed'))])
logp = 'trimmed.fasta.log' if os.path.exists('trimmed.fasta.log') else 'input.fasta.log'
lines = open(logp).read().splitlines()
print('log file used:', logp, '| rows:', len(lines), '| first row repr:', repr(lines[0]))
tab_fields = [l.split('\t') for l in lines]
print('rows with 4 tab-separated fields:', sum(len(x) == 4 for x in tab_fields))
ws = [l.split() for l in lines]
print('rows with 4 whitespace fields:', sum(len(x) == 4 for x in ws), '| max whitespace fields:', max(len(x) for x in ws))
print('keep/trim x class:', Counter((r[1], ' '.join(r[2:-1])) for r in ws).most_common(8))
kept = [int(r[0]) for r in ws if r[1] == 'keep']
print('kept columns in log:', len(kept), '== trimmed length:', len(kept) == t.get_alignment_length(), '| first index:', ws[0][0])

tns = dendropy.TaxonNamespace()
def load(p):
    tr = dendropy.Tree.get(path=p, schema='newick', taxon_namespace=tns, preserve_underscores=True)
    tr.is_rooted = False; tr.encode_bipartitions(); return tr
truth = load('../../data/prot15_true.nwk')
u, s = load('untrimmed.treefile'), load('smartgap.treefile')
print('RF(untrimmed, trimmed) =', treecompare.symmetric_difference(u, s))
print('AUDITOR CHECK RF to TRUE tree: untrimmed', treecompare.symmetric_difference(truth, u),
      '| smart-gap', treecompare.symmetric_difference(truth, s), '| max', 2 * (len(tns) - 3))
for name in ('untrimmed', 'smartgap'):
    txt = open(f'{name}.iqtree').read()
    model = [l for l in txt.splitlines() if l.startswith('Best-fit model according to BIC')]
    lnl = [l for l in txt.splitlines() if l.startswith('Log-likelihood of the tree')]
    tr = Phylo.read(f'{name}.contree', 'newick')
    sup = [c.confidence for c in tr.get_nonterminals() if c.confidence is not None]
    print(name, model, lnl, f'UFBoot mean {sum(sup)/len(sup):.1f}, n<95 = {sum(x < 95 for x in sup)}/{len(sup)}')
