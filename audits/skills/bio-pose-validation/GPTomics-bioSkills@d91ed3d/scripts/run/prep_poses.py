"""
Fix bond orders/charges on the obabel PDBQT->PDB->SDF conversion of the real
AutoDock Vina docking run (trypsin 3PTB + benzamidine, cached in the
cheminformatics-hit-triage-analyst tooling env). Open Babel's PDBQT->SDF
direct conversion emits a malformed explicit-valence flag on the amidinium N
(RDKit: "Explicit valence for atom # 0 N, 4, is greater than permitted").
Route through PDB (coordinates only) + RDKit AssignBondOrdersFromTemplate
against the known SMILES (NC(=[NH2+])c1ccccc1) to recover a valid molecule
with the docked 3D pose intact.
"""
import sys
from rdkit import Chem
from rdkit.Chem import AllChem

TEMPLATE_SMILES = "NC(=[NH2+])c1ccccc1"  # benzamidinium, from the PDBQT REMARK SMILES line

def fix_pose(pdb_path, out_sdf_path, mode_label, vina_score):
    template = Chem.MolFromSmiles(TEMPLATE_SMILES)
    raw = Chem.MolFromPDBFile(pdb_path, removeHs=False, sanitize=False)
    if raw is None:
        raise RuntimeError(f"Could not parse {pdb_path}")
    # Strip Hs from the raw PDB mol (obabel's PDB H placement is unreliable);
    # template AssignBondOrders will re-add them cleanly via RDKit AddHs later.
    raw_noh = Chem.RemoveHs(raw, sanitize=False)
    Chem.SanitizeMol(raw_noh, sanitizeOps=Chem.SANITIZE_ALL ^ Chem.SANITIZE_KEKULIZE ^ Chem.SANITIZE_PROPERTIES)
    fixed = AllChem.AssignBondOrdersFromTemplate(template, raw_noh)
    fixed.SetProp("_Name", mode_label)
    fixed.SetProp("vina_score_kcal_mol", str(vina_score))
    w = Chem.SDWriter(out_sdf_path)
    w.write(fixed)
    w.close()
    print(f"{mode_label}: wrote {out_sdf_path}, formula={Chem.rdMolDescriptors.CalcMolFormula(fixed)}, charge={Chem.GetFormalCharge(fixed)}")

if __name__ == "__main__":
    scores = {
        1: -6.106, 2: -6.103, 3: -5.261, 4: -5.016,
        5: -4.993, 6: -4.911, 7: -4.382, 8: -4.148,
    }
    for i in range(1, 9):
        fix_pose(f"../data/vina_modes{i}.pdb", f"../data/mode{i}_fixed.sdf", f"vina_mode_{i}", scores[i])
