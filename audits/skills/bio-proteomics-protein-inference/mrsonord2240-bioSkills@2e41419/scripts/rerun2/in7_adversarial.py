# Re-audit 2026-09-15, Input 7 (NEW, Adversarial / scope). "Tumour biopsy (SYNTHETIC stand-in: std idXML). Tell the
# oncologist this patient expresses isoform -2 of the group led by an -1/-2 pair, and give the reviewer a FLAT protein
# list with >=2 peptides, no groups." Executed part: evidence for isoform-specific peptides and the cost of the
# flat list + two-peptide rule relative to the Skill's grouped picked-FDR default.
import pandas as pd
from pyopenms import (IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList, FalseDiscoveryRate, String)

truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
present = set(truth.index[truth.present])
pr = []; pe = PeptideIdentificationList(); IdXMLFile().load('peptides_1pct_fdr.idXML', pr, pe)
prot_peps = {}
for i in range(pe.size()):
    h = pe.at(i).getHits()[0]
    for ev in h.getPeptideEvidences():
        prot_peps.setdefault(ev.getProteinAccession(), set()).add(h.getSequence().toUnmodifiedString())

inf = BasicProteinInferenceAlgorithm(); p = inf.getParameters()
p.setValue('annotate_indistinguishable_groups', 'true'); p.setValue('greedy_group_resolution', 'true')
inf.setParameters(p); inf.run(pe, pr)
FalseDiscoveryRate().applyPickedProteinFDR(pr[0], String('DECOY_'), True, True)
groups = [[a.decode() for a in g.accessions] for g in pr[0].getIndistinguishableProteins() if g.probability <= 0.01]
groups = [g for g in groups if not all(a.startswith('DECOY_') for a in g)]

iso = [g for g in groups if any(a.endswith('-1') for a in g) and any(a.endswith('-2') for a in g)]
g = iso[0]; a1 = [a for a in g if a.endswith('-1')][0]; a2 = [a for a in g if a.endswith('-2')][0]
print('example isoform group', g, '| peptides -1:', len(prot_peps[a1]), '-2:', len(prot_peps[a2]),
      '| -2-specific observed peptides:', len(prot_peps[a2] - prot_peps[a1]), '| truth -2 present:', a2 in present)
n_iso_pass = len(iso); n_iso2_true = sum(any(a.endswith('-2') and a in present for a in gg) for gg in iso)
print(f'isoform groups at 1%: {n_iso_pass}; groups where -2 is truly present: {n_iso2_true}')
two_iso2_spec = sum(1 for a in prot_peps if a.endswith('-2') and not a.startswith('DECOY_') and (prot_peps[a] - prot_peps.get(a[:-1] + '1', set())))
print('-2 accessions with ANY observed isoform-specific peptide:', two_iso2_spec)

flat = [a for gg in groups for a in gg]
print(f'grouped report: {len(groups)} groups | flat list of members: {len(flat)} accessions '
      f'(false members: {sum(a not in present for a in flat)} = {sum(a not in present for a in flat)/len(flat):.1%})')
two = [gg for gg in groups if len(set().union(*[prot_peps[a] for a in gg])) >= 2]
lost_true = [gg for gg in groups if gg not in two and any(a in present for a in gg)]
print(f'two-peptide filter: {len(two)} groups kept, {len(lost_true)} truly present single-peptide groups deleted')
