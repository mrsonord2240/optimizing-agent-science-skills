# bio-admet-prediction -- Inputs 1, 4, 5, 6, 7 analysis.
# Executable routes only: the Skill's own druglike_score / alerts snippets, plus
# ADMET-AI 2.0.1 offline as the stand-in for the hosted services the Skill names
# (ADMETlab 3.0 and ProTox-3.0 are web-only; see the viewer for that accounting).
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors, Lipinski, QED
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from sklearn.metrics import roc_auc_score

RDLogger.DisableLog('rdApp.*')
pd.set_option('display.width', 200)
D = r"F:\OpenScience\audits\bio-admet-prediction\run"


# ---- the two executable SKILL.md snippets, verbatim ------------------------
def alerts(mol, catalogs=('PAINS_A', 'BRENK', 'ZINC')):
    params = FilterCatalogParams()
    for cat in catalogs:
        params.AddCatalog(getattr(FilterCatalogParams.FilterCatalogs, cat))
    catalog = FilterCatalog(params)
    hits = catalog.GetMatches(mol)
    return [h.GetDescription() for h in hits]


def druglike_score(mol):
    mw, logp = Descriptors.MolWt(mol), Descriptors.MolLogP(mol)
    hbd, hba = Lipinski.NumHDonors(mol), Lipinski.NumHAcceptors(mol)
    tpsa, rot = Descriptors.TPSA(mol), Lipinski.NumRotatableBonds(mol)
    return {'MW': mw, 'LogP': logp, 'HBD': hbd, 'HBA': hba, 'TPSA': tpsa,
            'RotBonds': rot, 'QED': QED.qed(mol),
            'Lipinski_violations': sum([mw > 500, logp > 5, hbd > 5, hba > 10]),
            'Veber_pass': rot <= 10 and tpsa <= 140,
            'BBB_simple_screen': tpsa <= 90 and mw <= 500 and hbd <= 3}


truth = pd.read_csv(D + r"\herg_300_truth.csv")
preds = pd.read_csv(D + r"\herg_300_preds.csv")
mols = [Chem.MolFromSmiles(s) for s in truth.canonical_smiles]

# ===================== INPUT 1 (Canonical) =================================
print("===== INPUT 1: triage 300 compounds with the Skill's own snippets =====")
dl = pd.DataFrame([druglike_score(m) for m in mols])
al = [alerts(m) for m in mols]
dl['n_alerts'] = [len(a) for a in al]
print(f"  druglike_score ran on {len(dl)}/{len(mols)} molecules, 10 fields each")
print(dl[['MW', 'LogP', 'TPSA', 'QED', 'Lipinski_violations', 'n_alerts']]
      .describe().loc[['mean', 'min', 'max']].round(2).to_string())
print(f"  Lipinski 0 violations: {int((dl.Lipinski_violations == 0).sum())}/300   "
      f"Veber pass: {int(dl.Veber_pass.sum())}/300   "
      f"BBB simple screen: {int(dl.BBB_simple_screen.sum())}/300")
print(f"  at least one structural alert: {int((dl.n_alerts > 0).sum())}/300 "
      f"(alerts() returns descriptions, never deletes)")
flat = [d for a in al for d in a]
print(f"  total alert hits {len(flat)}; most common: "
      f"{pd.Series(flat).value_counts().head(5).to_dict()}")
print("  cross-check: does the Skill's BBB_simple_screen agree with ADMET-AI BBB_Martins?")
bbb = preds['BBB_Martins'].to_numpy()
print(f"    simple screen positive n={int(dl.BBB_simple_screen.sum())}, "
      f"mean BBB_Martins={bbb[dl.BBB_simple_screen.to_numpy()].mean():.3f}; "
      f"screen negative mean={bbb[~dl.BBB_simple_screen.to_numpy()].mean():.3f}")
print(f"    AUC of the 3-rule screen against BBB_Martins>=0.5: "
      f"{roc_auc_score((bbb >= 0.5).astype(int), dl.BBB_simple_screen.astype(int)):.3f}")

# ===================== INPUT 4 (Edge): hERG against measured data ==========
print("\n===== INPUT 4: the hERG endpoint against 300 measured ChEMBL values =====")
p_herg = preds['hERG'].to_numpy()
y = truth.pchembl_value.to_numpy()
for thr in [5.0, 6.0]:
    lab = (y >= thr).astype(int)
    print(f"  measured blocker at pChEMBL>={thr}: {lab.sum()}/300 positives, "
          f"ADMET-AI hERG AUC={roc_auc_score(lab, p_herg):.3f}")
print(f"  Spearman(predicted hERG prob, measured pChEMBL) = "
      f"{pd.Series(p_herg).corr(pd.Series(y), method='spearman'):.3f}")
print("  the Skill's rule 'a single-model probability > 0.5 is NOT a kill signal':")
for thr in [0.5, 0.7, 0.9]:
    sel = p_herg > thr
    if sel.sum() == 0:
        continue
    fp = ((y < 5.0) & sel).sum()
    print(f"    predicted prob > {thr}: {sel.sum():3} compounds, of which "
          f"{fp} have a MEASURED pChEMBL < 5 (i.e. would be killed wrongly) "
          f"= {100*fp/sel.sum():.1f}% false kill rate")
sel = p_herg <= 0.5
print(f"    predicted prob <= 0.5: {sel.sum()} compounds, of which "
      f"{int(((y >= 7.0) & sel).sum())} have a MEASURED pChEMBL >= 7 "
      f"(sub-100 nM blockers missed)")
print("  reported AUCs in the SKILL.md hERG table are 0.86-0.956 on their own")
print("  benchmarks; this independent external set gives the number above.")

# ===================== INPUT 5 (Stress): CYP inhibitor/substrate ==========
print("\n===== INPUT 5: the documented CYP inhibitor-vs-substrate ambiguity =====")
pairs = [('CYP3A4', 'CYP3A4_Veith', 'CYP3A4_Substrate_CarbonMangels'),
         ('CYP2D6', 'CYP2D6_Veith', 'CYP2D6_Substrate_CarbonMangels'),
         ('CYP2C9', 'CYP2C9_Veith', 'CYP2C9_Substrate_CarbonMangels')]
for iso, inh_c, sub_c in pairs:
    inh, sub = preds[inh_c].to_numpy(), preds[sub_c].to_numpy()
    both = ((inh > 0.5) & (sub > 0.5)).sum()
    print(f"  {iso}: inhibitor>0.5 {int((inh>0.5).sum()):3}  substrate>0.5 "
          f"{int((sub>0.5).sum()):3}  BOTH>0.5 {int(both):3} "
          f"({100*both/300:.1f}% of the set)  corr(inh,sub)="
          f"{np.corrcoef(inh, sub)[0,1]:+.3f}")
print("  the 5-CYP panel the Skill names is present in the executable route:")
for c in ['CYP1A2_Veith', 'CYP2C19_Veith', 'CYP2C9_Veith', 'CYP2D6_Veith', 'CYP3A4_Veith']:
    print(f"    {c:16} present={c in preds.columns}  mean={preds[c].mean():.3f}")

# ===================== INPUT 7 (Adversarial): the OOD failure mode ========
print("\n===== INPUT 7: out-of-distribution chemistry, as the failure mode names it =====")
ot = pd.read_csv(D + r"\ood_probes_truth.csv")
op = pd.read_csv(D + r"\ood_probes_preds.csv")
cols = ['hERG', 'AMES', 'DILI', 'BBB_Martins', 'Caco2_Wang', 'Solubility_AqSolDB']
print(f"  {'compound':46}" + "".join(f"{c[:12]:>14}" for c in cols))
for i, lab in enumerate(ot.label):
    print(f"  {lab:46}" + "".join(f"{op[c].iloc[i]:14.3f}" for c in cols))
print("  every probe received a point prediction; no uncertainty column, no")
print("  applicability-domain flag and no refusal appears anywhere in the output:")
unc = [c for c in op.columns if any(k in c.lower() for k in
                                    ('unc', 'std', 'var', 'conf', 'interval', 'domain'))]
print(f"    columns matching uncertainty/AD keywords: {unc if unc else 'NONE'}")
print(f"    total output columns: {len(op.columns)} "
      f"(of which {sum('percentile' in c for c in op.columns)} are DrugBank percentiles)")

# ===================== INPUT 6 (Scope boundary) ==========================
print("\n===== INPUT 6: 'is this compound safe to dose?' -- boundary content check =====")
import re
skill = open(r"F:\OpenScience\external\mrsonord2240__bioSkills\chemoinformatics"
             r"\admet-prediction\SKILL.md", encoding='utf-8').read()
for phrase in ['NOT a kill signal', 'confirm important decisions experimentally',
               'ICH S7B', 'in vitro patch-clamp', 'do not exclude pre-emptively',
               'regulatory conclusion', 'universal safe/unsafe IC50 cutoff']:
    print(f"  SKILL.md contains {phrase!r}: {phrase in skill}")
print(f"  occurrences of 'patient' / 'dose the patient' / 'prescrib': "
      f"{len(re.findall('patient', skill, re.I))} / "
      f"{len(re.findall('dose the patient', skill, re.I))} / "
      f"{len(re.findall('prescrib', skill, re.I))}")
