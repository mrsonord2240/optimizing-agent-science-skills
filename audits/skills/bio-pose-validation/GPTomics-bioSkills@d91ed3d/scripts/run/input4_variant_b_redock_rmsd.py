"""
Audit Input 4 (Variant B) — bio-pose-validation
Prompt: "I have a co-crystal reference structure (3PTB, benzamidine) and a
re-docked pose from Vina. Run the redock config, report RMSD vs PB-valid, and
tell me which quadrant of the Skill's reconciliation table it falls in."
"""
from posebusters import PoseBusters
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)

bust = PoseBusters(config='redock')
r = bust.bust(
    mol_pred='../data/mode1_fixed.sdf',
    mol_true='../data/ben_ref.sdf',
    mol_cond='../data/receptor.pdb',
)
check_cols = [c for c in r.select_dtypes(include='bool').columns if not c.lower().startswith('rmsd')]
r['pb_valid'] = r[check_cols].all(axis=1)

rmsd_col = [c for c in r.columns if c.lower().startswith('rmsd')][0]
pb_valid = bool(r['pb_valid'].iloc[0])
rmsd_ok = bool(r[rmsd_col].iloc[0])
print(f"pb_valid: {pb_valid}")
print(f"{rmsd_col}: {rmsd_ok}")
print(f"stereo checks -- double_bond_stereochemistry: {bool(r['double_bond_stereochemistry'].iloc[0])}, "
      f"tetrahedral_chirality: {bool(r['tetrahedral_chirality'].iloc[0])}")

quadrant = {
    (True, True): "RMSD<=2A + PB-valid: physically plausible and close to reference",
    (True, False): "RMSD<=2A but not PB-valid: close to reference but fails a plausibility check",
    (False, True): "RMSD>2A but PB-valid: plausible but different pose, investigate alt binding mode",
    (False, False): "RMSD>2A and not PB-valid: reject or inspect both causes",
}[(rmsd_ok, pb_valid)]
print("Reconciliation table verdict:", quadrant)
