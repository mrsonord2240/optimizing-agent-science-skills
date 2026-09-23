"""Assert the completed AutoDock4 tutorial regression produced real output."""
from pathlib import Path
import re

output = Path(__file__).resolve().parent / "ad4_covalent_windows_output" / "adCovalentDockResidue" / "3upo_test" / "output"
maps = sorted(output.glob("3upo_protein_rigid.*.map"))
assert len(maps) == 8, len(maps)
assert all(path.stat().st_size > 1000 for path in maps), [(p.name, p.stat().st_size) for p in maps]
dlg = output / "audit_ligcovalent_3upo_protein.dlg"
assert dlg.is_file() and dlg.stat().st_size > 10000
energies = [float(value) for value in re.findall(r"Estimated Free Energy of Binding\s+=\s+(-?\d+\.\d+)", dlg.read_text(errors="replace"))]
assert len(energies) >= 10, len(energies)
best = min(energies)
assert -11.5 < best < -10.0, best
assert "Successful Completion" in (output / "audit_3upo.glg").read_text(errors="replace")
print(f"grid_maps={len(maps)} dlg_energies={len(energies)} best_binding_kcal_per_mol={best:.2f}")
