# Input 3 (Edge): small IP-MS peptide map with two INDISTINGUISHABLE isoforms, a subset fragment and a few decoys.
# Following the Skill: its example examples/protein_groups.py with SAMPLE_MAP replaced (as its docstring instructs).
import importlib.util, io, contextlib, sys
import pandas as pd

src = open('example_protein_groups.py', encoding='utf-8').read()
# execute only the function definitions + constants from the shipped example
defs = src.split('selected, protein_peptides = apply_parsimony')[0]
ns = {}
exec(compile(defs, 'protein_groups.py', 'exec'), ns)
apply_parsimony, build_groups, picked_group_fdr = ns['apply_parsimony'], ns['build_groups'], ns['picked_group_fdr']

def run(label, MAP):
    print(f'--- {label} ---')
    selected, protein_peptides = apply_parsimony(MAP)
    print(f'Parsimony kept {len(selected)} proteins out of {len(protein_peptides)} candidates')
    print(f'Dropped (subsumable): {sorted(set(protein_peptides) - set(selected))}')
    groups = build_groups(selected, protein_peptides, MAP)
    report = pd.DataFrame(picked_group_fdr(groups)).sort_values('score', ascending=False)
    passing = report[(~report['is_decoy']) & (report['qvalue'] <= 0.01)]
    print(f'Protein groups passing 1% picked-group FDR: {len(passing)}')
    print(report[['leading_protein', 'accessions', 'n_peptides', 'n_unique_peptides', 'is_decoy', 'qvalue']].to_string(index=False))

# TPM1 canonical (P09493) and isoform 2 (P09493-2): every observed peptide is shared -> indistinguishable.
# Q5VU61 is a TrEMBL fragment whose observed peptides are a subset of TPM1.
MAP_canonical_first = {
    'LVIIESDLERAEER': ['P09493', 'P09493-2'],
    'IQLVEEELDRAQER': ['P09493', 'P09493-2', 'Q5VU61'],
    'KLVIIEGDLER':    ['P09493', 'P09493-2', 'Q5VU61'],
    'SIDDLEDELYAQK':  ['P09493', 'P09493-2'],
    'MEIQEIQLK':      ['P09493', 'P09493-2'],
    'ELDNALNDITSL':   ['P67936'],             # TPM4 unique
    'AEFAERSVTK':     ['P67936'],
    'HIAEDADRK':      ['P07951'],             # TPM2 one-hit
    'KLEETLTAR':      ['DECOY_P09493', 'DECOY_P09493-2'],
    'RTEELQAK':       ['DECOY_Q9Y2B0'],
}
run('canonical listed first', MAP_canonical_first)
MAP_isoform_first = {k: sorted(v, key=lambda a: a != 'P09493-2') for k, v in MAP_canonical_first.items()}
run('same evidence, isoform accession listed first in the search output', MAP_isoform_first)

# Same map through the Skill's PRIMARY path (pyOpenMS BasicProteinInferenceAlgorithm, adapted list type)
import pyopenms as oms
pr = oms.ProteinIdentification(); pr.setIdentifier('ip'); pr.setScoreType('')
accs = sorted({a for v in MAP_canonical_first.values() for a in v})
hits = []
for a in accs:
    h = oms.ProteinHit(); h.setAccession(a); h.setMetaValue('target_decoy', 'decoy' if a.startswith('DECOY_') else 'target'); hits.append(h)
pr.setHits(hits)
peps = oms.PeptideIdentificationList()
pep_scores = [0.001, 0.002, 0.004, 0.01, 0.003, 0.002, 0.02, 0.006, 0.4, 0.5]
for i, ((seq, prots), pepv) in enumerate(zip(MAP_canonical_first.items(), pep_scores)):
    pid = oms.PeptideIdentification(); pid.setIdentifier('ip'); pid.setScoreType('Posterior Error Probability'); pid.setHigherScoreBetter(False)
    pid.setRT(float(i)); pid.setMZ(500.0)
    ph = oms.PeptideHit(); ph.setSequence(oms.AASequence.fromString(seq)); ph.setScore(pepv); ph.setCharge(2)
    evs = []
    for a in prots:
        ev = oms.PeptideEvidence(); ev.setProteinAccession(a); evs.append(ev)
    ph.setPeptideEvidences(evs); pid.setHits([ph]); peps.push_back(pid)
prs = [pr]
inf = oms.BasicProteinInferenceAlgorithm(); p = inf.getParameters(); p.setValue('annotate_indistinguishable_groups', 'true'); inf.setParameters(p)
inf.run(peps, prs)
print('--- pyOpenMS BasicProteinInferenceAlgorithm on the same evidence ---')
for g in prs[0].getIndistinguishableProteins():
    print('  ', [a.decode() for a in g.accessions], round(g.probability, 4))
