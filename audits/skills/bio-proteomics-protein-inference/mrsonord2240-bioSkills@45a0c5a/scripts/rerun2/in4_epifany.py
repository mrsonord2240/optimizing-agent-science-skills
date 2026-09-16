# Re-audit 2026-09-15, Input 4 (Variant B, regression). SKILL.md EPIFANY block VERBATIM, then group FDR the way the
# Skill's decision tree directs ("EPIFANY ... + picked-group FDR"): built-in applyPickedProteinFDR. Truth = SYNTHETIC.
import io, contextlib, time
import pandas as pd

BLOCK = r'''
from pyopenms import IdXMLFile, BayesianProteinInferenceAlgorithm, PeptideIdentificationList

protein_ids = []
peptide_ids = PeptideIdentificationList()
IdXMLFile().load('peptides_with_pep.idXML', protein_ids, peptide_ids)

algo = BayesianProteinInferenceAlgorithm()
# EPIFANY expects PSM posteriors as input; the third argument (greedy_group_resolution)
# controls whether shared peptides are razor-resolved after inference
algo.inferPosteriorProbabilities(protein_ids, peptide_ids, False)

for group in protein_ids[0].getIndistinguishableProteins():
    print([a.decode() for a in group.accessions], group.probability)   # higher = more likely present
'''
ns = {}; buf = io.StringIO(); t0 = time.time()
with contextlib.redirect_stdout(buf):
    exec(compile(BLOCK, 'skill_block', 'exec'), ns)
lines = buf.getvalue().strip().splitlines()
print(f'BLOCK ran in {time.time()-t0:.1f}s; printed group lines: {len(lines)}; first: {lines[0]}')
pid = ns['protein_ids'][0]
print('score type:', pid.getScoreType(), '| higher better:', pid.isHigherScoreBetter())

truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
present = set(truth.index[truth.present])
frag = set(truth[(truth.family_type == 'fragment') & truth.index.str.endswith('F') & truth.observed].index)

from pyopenms import FalseDiscoveryRate, String
FalseDiscoveryRate().applyPickedProteinFDR(pid, String('DECOY_'), True, True)
G = [([a.decode() for a in g.accessions], g.probability) for g in pid.getIndistinguishableProteins()]
passing = [a for a, q in G if q <= 0.01 and not all(x.startswith('DECOY_') for x in a)]
fp = [a for a in passing if not any(x in present for x in a)]
print(f'EPIFANY + applyPickedProteinFDR: groups {len(G)}, passing {len(passing)}, true FDP {len(fp)}/{len(passing)} = {len(fp)/max(1,len(passing)):.2%}, fragment groups passing {sum(any(x in frag for x in a) for a in passing)}')

# same with greedy resolution argument True (Skill's third argument)
from pyopenms import IdXMLFile, BayesianProteinInferenceAlgorithm, PeptideIdentificationList
pr = []; pe = PeptideIdentificationList(); IdXMLFile().load('peptides_with_pep.idXML', pr, pe)
BayesianProteinInferenceAlgorithm().inferPosteriorProbabilities(pr, pe, True)
FalseDiscoveryRate().applyPickedProteinFDR(pr[0], String('DECOY_'), True, True)
G2 = [([a.decode() for a in g.accessions], g.probability) for g in pr[0].getIndistinguishableProteins()]
p2 = [a for a, q in G2 if q <= 0.01 and not all(x.startswith('DECOY_') for x in a)]
f2 = [a for a in p2 if not any(x in present for x in a)]
print(f'EPIFANY(greedy=True) + picked: groups {len(G2)}, passing {len(p2)}, true FDP {len(f2)}/{len(p2)} = {len(f2)/max(1,len(p2)):.2%}, fragment groups passing {sum(any(x in frag for x in a) for a in p2)}')
