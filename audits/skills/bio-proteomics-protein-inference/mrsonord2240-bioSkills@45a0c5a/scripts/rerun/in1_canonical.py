# Re-audit 2026-09-15, Input 1 (Canonical, regression). SKILL.md "Group Proteins with pyOpenMS" block VERBATIM
# (fork 575ab94), stdout of its print loop captured; then audit checks vs SYNTHETIC truth (data/truth_std.csv).
import io, contextlib
import pandas as pd

BLOCK = r'''
from pyopenms import (IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList,
                      FalseDiscoveryRate, String)

protein_ids = []
peptide_ids = PeptideIdentificationList()   # pyOpenMS 3.5+: a plain [] fails
# protein_ids is FIRST in both load() and store() for IdXMLFile
IdXMLFile().load('peptides_1pct_fdr.idXML', protein_ids, peptide_ids)

inference = BasicProteinInferenceAlgorithm()
params = inference.getParameters()
# annotate_indistinguishable_groups reports indistinguishable proteins as ONE group
params.setValue('annotate_indistinguishable_groups', 'true')
# greedy_group_resolution assigns shared peptides to the best group, so subsumable proteins drop out
params.setValue('greedy_group_resolution', 'true')
inference.setParameters(params)
inference.run(peptide_ids, protein_ids)

# picked protein-group FDR: (decoy string, is prefix, groups too); group.probability becomes a q-value
FalseDiscoveryRate().applyPickedProteinFDR(protein_ids[0], String('DECOY_'), True, True)

for group in protein_ids[0].getIndistinguishableProteins():
    accs = [a.decode() for a in group.accessions]   # bytes; pyOpenMS sorts them alphabetically
    if all(a.startswith('DECOY_') for a in accs) or group.probability > 0.01:
        continue
    # members share the same evidence; choose the lead explicitly: canonical (no -N isoform suffix) first
    leading = sorted(accs, key=lambda a: ('-' in a, a))[0]
    print(leading, group.probability, accs)
'''
ns = {}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(BLOCK, 'skill_block', 'exec'), ns)
lines = buf.getvalue().strip().splitlines()
print('BLOCK ran, exit OK. printed lines (passing groups):', len(lines))
print('first 4 printed lines:'); [print('  ', l) for l in lines[:4]]

truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
present = set(truth.index[truth.present])
pid = ns['protein_ids'][0]
print('score type after FDR:', pid.getScoreType(), '| higher better:', pid.isHigherScoreBetter())
G = [[a.decode() for a in g.accessions] for g in pid.getIndistinguishableProteins()]
Q = [g.probability for g in pid.getIndistinguishableProteins()]
isdec = [all(a.startswith('DECOY_') for a in acc) for acc in G]
passing = [acc for acc, q, d in zip(G, Q, isdec) if not d and q <= 0.01]
fp = [acc for acc in passing if not any(a in present for a in acc)]
print(f'groups {len(G)} (target {len(G)-sum(isdec)}, decoy {sum(isdec)}); passing q<=0.01: {len(passing)}; '
      f'true FDP {len(fp)}/{len(passing)} = {len(fp)/max(1,len(passing)):.2%}')

# independent recomputation of picked group q-values from the pre-FDR group scores (second method)
from pyopenms import IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList
pr = []; pe = PeptideIdentificationList(); IdXMLFile().load('peptides_1pct_fdr.idXML', pr, pe)
inf = BasicProteinInferenceAlgorithm(); p = inf.getParameters()
p.setValue('annotate_indistinguishable_groups', 'true'); p.setValue('greedy_group_resolution', 'true')
inf.setParameters(p); inf.run(pe, pr)
raw = [([a.decode() for a in g.accessions], g.probability) for g in pr[0].getIndistinguishableProteins()]
print('pre-FDR group score type:', pr[0].getScoreType(), 'higher better:', pr[0].isHigherScoreBetter())
by = {}
for acc, s in raw:
    base = frozenset(a.replace('DECOY_', '') for a in acc)
    if base not in by or s > by[base][1]:
        by[base] = (acc, s)
pk = sorted(by.values(), key=lambda x: -x[1])
t = d = 0; fd = []
for acc, s in pk:
    dd = all(a.startswith('DECOY_') for a in acc); d += dd; t += not dd; fd.append(d / max(t, 1))
m = 1.0; q = [0] * len(fd)
for i in range(len(fd) - 1, -1, -1):
    m = min(m, fd[i]); q[i] = m
mine = [acc for (acc, s), qq in zip(pk, q) if qq <= 0.01 and not all(a.startswith('DECOY_') for a in acc)]
print('independent picked-group recount (exact-set pairing) passing:', len(mine))

# structure checks
frag = set(truth[(truth.family_type == 'fragment') & truth.index.str.endswith('F') & truth.observed].index)
print('fragment (subsumable) groups passing:', sum(any(a in frag for a in acc) for acc in passing))
iso2 = [acc for acc in passing if any(a.endswith('-2') for a in acc)]
print('passing groups containing an -2 isoform:', len(iso2), '| of which also contain -1:', sum(any(a.endswith('-1') for a in acc) for acc in iso2))
leads = [l.split()[0] for l in lines]
print('leads ending in -2 while a -1 member exists (lead rule check):',
      sum(1 for l, acc in zip(leads, passing) if l.endswith('-2') and any(a.endswith('-1') for a in acc)))
