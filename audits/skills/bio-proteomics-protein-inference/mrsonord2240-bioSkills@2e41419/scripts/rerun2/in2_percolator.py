# Re-audit 2026-09-15 (batch C), Input 2 (Variant A, NEW). Percolator 3.09.0 is now installed.
# Tests (a) the SKILL.md Tool-Taxonomy claim that Percolator's protein inference is Fido via `--protein`,
# (b) what Percolator 3.09 actually offers, (c) the SKILL.md default pyOpenMS block on the SAME REAL data
# (PXD070049 DDA Condition_A, Comet 2026.02 -> OpenMS), (d) regression: decoy-prefix handling (rev_ vs DECOY_).
import subprocess, os, sys
import pandas as pd

E = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
PERC = E + '/tools/percolator/percolator.exe'

print('=== (a) SKILL.md Tool Taxonomy: "Fido ... (Percolator `--protein`)" ===')
for flag in ('--protein', '-A'):
    r = subprocess.run([PERC, flag], capture_output=True, text=True)
    err = [l for l in (r.stdout + r.stderr).splitlines() if 'ERROR' in l or 'invalid' in l]
    print(f'  percolator {flag:10s} -> exit {r.returncode} | {err[0] if err else "(no error line)"}')
r = subprocess.run([PERC, '--help'], capture_output=True, text=True)
h = r.stdout + r.stderr
print('  "fido" appears in --help as a positive option:', any(
    l.strip().startswith(('-f ', '--fido')) for l in h.splitlines()))
print('  --picked-protein present in --help:', '--picked-protein' in h)

print('\n=== (b) Percolator 3.09 picked-protein run on real Comet pin (already executed; reading outputs) ===')
W = os.path.dirname(os.path.abspath(__file__))
pt = pd.read_csv(os.path.join(W, 'prot.target.tsv'), sep='\t')
pd_ = pd.read_csv(os.path.join(W, 'prot.decoy.tsv'), sep='\t')
print(f'  target protein rows {len(pt)}, decoy protein rows {len(pd_)}')
print(f'  target groups at q<=0.01: {(pt["q-value"] <= 0.01).sum()}')
print(f'  distinct ProteinGroupId among passing: {pt.loc[pt["q-value"]<=0.01,"ProteinGroupId"].nunique()}')
multi = pt[pt['ProteinId'].str.contains(',')]
print(f'  rows reporting >1 accession (comma-joined group members): {len(multi)}')
print('  decoy rows leaking into the target file:',
      int(pt['ProteinId'].str.startswith('DECOY_').sum()))
print('  first 3 passing rows:')
print(pt.head(3)[['ProteinId', 'ProteinGroupId', 'q-value']].to_string(index=False))

print('\n=== (c) SKILL.md default block on the SAME real data (idXML route) ===')
from pyopenms import (IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList,
                      FalseDiscoveryRate, String)
protein_ids = []
peptide_ids = PeptideIdentificationList()
IdXMLFile().load(os.path.join(W, 'real_q.idXML'), protein_ids, peptide_ids)
inference = BasicProteinInferenceAlgorithm()
params = inference.getParameters()
params.setValue('annotate_indistinguishable_groups', 'true')
params.setValue('greedy_group_resolution', 'true')
inference.setParameters(params)
inference.run(peptide_ids, protein_ids)
FalseDiscoveryRate().applyPickedProteinFDR(protein_ids[0], String('DECOY_'), True, True)
G = [[a.decode() for a in g.accessions] for g in protein_ids[0].getIndistinguishableProteins()]
Q = [g.probability for g in protein_ids[0].getIndistinguishableProteins()]
isdec = [all(a.startswith('DECOY_') for a in acc) for acc in G]
passing = [acc for acc, q, d in zip(G, Q, isdec) if not d and q <= 0.01]
print(f'  PSMs loaded {len(peptide_ids)}; groups {len(G)} (decoy {sum(isdec)}); passing q<=0.01: {len(passing)}')
print(f'  Percolator picked-protein on the same run: {(pt["q-value"]<=0.01).sum()} groups')
print('  NOTE: only', sum(isdec), 'decoy groups -> below the Skill\'s own min-decoy guidance;'
      ' the Skill\'s picked_group_fdr sketch would WARN here, applyPickedProteinFDR does not.')

print('\n=== (d) regression: decoy prefix handling (synthetic std idXML) ===')
os.chdir(W)
for prefix, path in (('DECOY_', 'peptides_1pct_fdr.idXML'), ('rev_', 'rev_prefix.idXML')):
    pr, pe = [], PeptideIdentificationList()
    IdXMLFile().load(path, pr, pe)
    inf = BasicProteinInferenceAlgorithm(); p = inf.getParameters()
    p.setValue('annotate_indistinguishable_groups', 'true'); p.setValue('greedy_group_resolution', 'true')
    inf.setParameters(p); inf.run(pe, pr)
    try:
        FalseDiscoveryRate().applyPickedProteinFDR(pr[0], String(prefix), True, True)
        gg = [([a.decode() for a in g.accessions], g.probability) for g in pr[0].getIndistinguishableProteins()]
        keep = [a for a, q in gg if q <= 0.01 and not all(x.startswith(prefix) for x in a)]
        print(f'  {path} with prefix {prefix!r}: {len(keep)} groups at 1%')
    except Exception as ex:
        print(f'  {path} with prefix {prefix!r}: {type(ex).__name__}: {ex}')
    # deliberately wrong prefix
    pr2, pe2 = [], PeptideIdentificationList()
    IdXMLFile().load(path, pr2, pe2)
    inf.run(pe2, pr2)
    wrong = 'rev_' if prefix == 'DECOY_' else 'DECOY_'
    try:
        FalseDiscoveryRate().applyPickedProteinFDR(pr2[0], String(wrong), True, True)
        print(f'  {path} with WRONG prefix {wrong!r}: returned without raising (silent)')
    except Exception as ex:
        print(f'  {path} with WRONG prefix {wrong!r}: {type(ex).__name__}: {ex}')
